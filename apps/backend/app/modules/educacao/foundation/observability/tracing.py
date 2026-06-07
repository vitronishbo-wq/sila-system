import logging

from apps.backend.app.core.settings import settings
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider as SDKTracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter

logger = logging.getLogger(__name__)


def _try_create_otlp_exporter(endpoint: str) -> object | None:
    """Try to instantiate an OTLP exporter (gRPC or HTTP) if available.
    Returns exporter instance or None.
    """
    if not endpoint:
        return None
    # Try gRPC exporter first
    try:
        from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import (
            OTLPSpanExporter,
        )

        return OTLPSpanExporter(endpoint=endpoint)
    except Exception:
        pass
    # Try HTTP exporter
    try:
        from opentelemetry.exporter.otlp.proto.http.trace_exporter import (
            OTLPSpanExporter,
        )

        return OTLPSpanExporter(endpoint=endpoint)
    except Exception:
        logger.warning("OTLP exporter not available, falling back to ConsoleSpanExporter")
        return None


def configure_tracing(service_name: str | None = None):
    """Configure OpenTelemetry tracing.

    - If `settings.OTEL_EXPORTER_OTLP_ENDPOINT` is set and an OTLP exporter is available,
      use it. Otherwise fall back to `ConsoleSpanExporter`.
    - Also instruments SQLAlchemy and Redis if toggles enabled and instrumentors available.
    """
    svc = service_name or getattr(settings, "OTEL_SERVICE_NAME", "sila-backend")

    resource = Resource.create({"service.name": svc})
    provider = SDKTracerProvider(resource=resource)

    exporter = _try_create_otlp_exporter(getattr(settings, "OTEL_EXPORTER_OTLP_ENDPOINT", ""))
    if exporter:
        provider.add_span_processor(BatchSpanProcessor(exporter))
        logger.info("Tracing configured with OTLP exporter")
    else:
        provider.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))
        logger.info("Tracing configured with ConsoleSpanExporter (no OTLP exporter available)")

    trace.set_tracer_provider(provider)

    # Optional: instrument SQLAlchemy and Redis if enabled
    try:
        if getattr(settings, "OBS_INSTRUMENT_SQL", False):
            try:
                from apps.backend.app.core.db import engine as async_engine
                from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor

                sync_engine = getattr(async_engine, "sync_engine", None)
                if sync_engine is not None:
                    SQLAlchemyInstrumentor().instrument(engine=sync_engine)
                    logger.info("SQLAlchemy instrumentation enabled")
            except Exception as e:
                logger.warning(f"SQLAlchemy instrumentation unavailable: {e}")

        if getattr(settings, "OBS_INSTRUMENT_REDIS", False):
            try:
                from opentelemetry.instrumentation.redis import RedisInstrumentor

                RedisInstrumentor().instrument()
                logger.info("Redis instrumentation enabled")
            except Exception as e:
                logger.warning(f"Redis instrumentation unavailable: {e}")
    except Exception:
        logger.exception("Error during optional instrumentations")


def get_tracer(name: str = __name__):
    return trace.get_tracer(name)
