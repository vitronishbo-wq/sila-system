import json
import os
import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from apps.backend.app.modules.educacao.foundation.observability.logging import (
    configure_logging,  # noqa: E402
)
from apps.backend.app.modules.educacao.foundation.observability.middleware import (
    ASGIMetricsMiddleware,
    ObservabilityMiddleware,
)  # noqa: E402  # noqa: E402
from apps.backend.app.modules.educacao.foundation.observability.tracing import (
    configure_tracing,
)  # noqa: E402

_REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
if _REPO_ROOT not in sys.path:
    sys.path.append(_REPO_ROOT)

# NOTE: sys.path adjustment is required before these imports.
from apps.backend.app.core.settings import settings  # noqa: E402
from apps.backend.app.platform.observability.logger import get_sila_logger  # noqa: E402
from apps.backend.app.platform.integration.provider_registry import (  # noqa: E402
    register_default_providers,
)
from apps.backend.app.platform.integration.provider_router import (  # noqa: E402
    router as provider_router,
)
from apps.backend.app.platform.runtime.compat_router import router as compat_router  # noqa: E402
from apps.backend.app.platform.runtime.health_router import router as health_router  # noqa: E402
from apps.backend.app.platform.runtime.loader import discover_and_register_routers  # noqa: E402

from apps.backend.app.core.events.bridge.event_bus_bridge import EventBusBridge  # noqa: E402
from apps.backend.app.core.events.workers.projection_worker import ProjectionWorker  # noqa: E402
from apps.backend.app.modules.identity.middleware.trust_middleware import (  # noqa: E402
    TrustEvaluationMiddleware,
)

try:
    from apps.backend.core.audit import (  # noqa: E402
        DatabaseAuditAdapter,
        InMemoryAuditAdapter,
        initialize_audit,
        setup_audit_middleware,
    )

    AUDIT_ENABLED = True
    AUDIT_USE_DATABASE = os.getenv("AUDIT_USE_DATABASE", "false").lower() == "true"
except ImportError:
    AUDIT_ENABLED = False
    AUDIT_USE_DATABASE = False
logger = get_sila_logger("sila-core")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan management for event sourcing infrastructure.

    Startup:
      1. Create event bus bridge (Outbox + EventStore atomic publisher)
      2. Create projection worker (Redis XREADGROUP consumer for CQRS)
      3. Start worker listening to event stream

    Shutdown:
      1. Stop projection worker gracefully
      2. Clean up connections
    """
    try:
        EventBusBridge()
        worker = ProjectionWorker()
        await worker.start()
        if AUDIT_ENABLED:
            if AUDIT_USE_DATABASE:
                audit_adapter = DatabaseAuditAdapter()
                await initialize_audit(audit_adapter)
                logger.info("✓ Core audit engine initialized (Week 2+ - PostgreSQL)")
            else:
                audit_adapter = InMemoryAuditAdapter()
                await initialize_audit(audit_adapter)
                logger.info("✓ Core audit engine initialized (Week 1 - In-Memory)")
        logger.info("✓ Event bus bridge initialized (EventBusBridge)")
        logger.info("✓ Projection worker started (listening to event_stream in Redis)")
        logger.info("✓ CQRS denormalization pipeline active")
    except Exception as e:
        logger.error(f"✗ Failed to initialize event sourcing: {e}")
        raise
    yield
    try:
        await worker.stop()
        logger.info("✓ Projection worker stopped gracefully")
    except Exception as e:
        logger.error(f"✗ Error stopping projection worker: {e}")


def create_app():
    """
    Create and configure FastAPI application with sovereign trust engine.

    Architecture:
    - DDD-compliant singleton entry point
    - Event sourcing enabled (EventBusBridge + ProjectionWorker)
    - Sovereign trust evaluation middleware (40/40/20 model)
    - Auto-discovered routers from modules/*/api/router.py
    - CORS middleware for cross-origin requests
    """
    settings.require_runtime_bootstrap()
    register_default_providers()
    # configure structured logging and correlation before app startup
    try:
        configure_logging()
    except Exception:
        # avoid blocking bootstrap if logging libs missing in some environments
        pass
    # configure tracing and optional instrumentations (OTLP when configured)
    try:
        configure_tracing(settings.OTEL_SERVICE_NAME)
    except Exception:
        # do not block startup if tracing setup fails
        logger.exception("Failed to initialize tracing")
    app = FastAPI(
        title="SILA Sovereign Platform - Event Sourcing Enabled",
        version="20.2",
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan,
    )
    logger.info("Booting SILA platform")
    cors_origins = (
        os.getenv("CORS_ORIGINS")
        or os.getenv("BACKEND_CORS_ORIGINS")
        or "http://localhost:3000,http://127.0.0.1:3000,http://host.docker.internal:3000,http://localhost:3001,http://127.0.0.1:3001,http://host.docker.internal:3001,http://localhost:5173,http://127.0.0.1:5173,http://host.docker.internal:5173"
    )
    allow_origins = [origin.strip() for origin in cors_origins.split(",") if origin.strip()]
    cors_origin_regex = os.getenv(
        "CORS_ORIGIN_REGEX",
        r"^https?://(localhost|127\.0\.0\.1|host\.docker\.internal)(:3000|:3001|:5173)?$",
    )
    app.add_middleware(TrustEvaluationMiddleware)
    # Observability middleware: correlation id + request context
    app.add_middleware(ObservabilityMiddleware)
    # collect HTTP metrics (Prometheus)
    app.add_middleware(ASGIMetricsMiddleware)
    # Idempotency enforcement middleware for critical operations
    try:
        from apps.backend.app.core.middleware.idempotency_middleware import IdempotencyMiddleware

        app.add_middleware(IdempotencyMiddleware)
    except Exception:
        logger.warning("Idempotency middleware not loaded; proceeding without enforcement")
    app.include_router(health_router)
    app.include_router(provider_router)
    if AUDIT_ENABLED:
        setup_audit_middleware(app)
        logger.info("✓ Audit middleware initialized (Week 1)")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allow_origins,
        allow_origin_regex=cors_origin_regex,
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True,
    )
    app.include_router(compat_router)
    try:
        from apps.backend.app.api.router import api_router

        app.include_router(api_router)
        logger.info("✓ Core API router loaded (events, etc.)")
    except Exception as e:
        logger.warning(f"Failed to load core API router: {e}")
    report = discover_and_register_routers(app)
    logger.info(
        f"Router discovery summary: loaded={len(report['loaded'])} skipped={len(report['skipped'])} failed={len(report['failed'])}"
    )
    if report["failed"]:
        logger.warning(
            json.dumps(
                {"event": "router_load_failures", "failures": report["failed"]}, ensure_ascii=False
            )
        )
    logger.info("✓ SILA platform initialized (Clean State)")
    return app


app = create_app()
