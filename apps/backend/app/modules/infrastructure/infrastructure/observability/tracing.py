from __future__ import annotations

import os
from collections.abc import Iterator
from contextlib import contextmanager

_tracer = None
_fastapi_instrumented = False
_sqlalchemy_instrumented = False


def setup_tracing() -> None:
    """Initialize OTel if available; no-op when dependency/env is absent."""
    global _tracer
    if _tracer is not None:
        return
    try:
        from opentelemetry import trace
        from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
        from opentelemetry.sdk.resources import Resource
        from opentelemetry.sdk.trace import TracerProvider
        from opentelemetry.sdk.trace.export import BatchSpanProcessor
    except Exception:
        _tracer = False
        return
    endpoint = os.environ.get("OP_OTEL_EXPORTER_ENDPOINT", "").strip()
    service_name = os.environ.get("OP_OTEL_SERVICE_NAME", "obras_publicas")
    provider = TracerProvider(resource=Resource.create({"service.name": service_name}))
    trace.set_tracer_provider(provider)
    if endpoint:
        exporter = OTLPSpanExporter(endpoint=endpoint, insecure=True)
        provider.add_span_processor(BatchSpanProcessor(exporter))
    _tracer = trace.get_tracer("apps.backend.app.modules.infrastructure.domain_publicas")


def instrument_fastapi(app) -> None:
    global _fastapi_instrumented
    if _fastapi_instrumented:
        return
    setup_tracing()
    if not _tracer:
        return
    try:
        from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
    except Exception:
        return
    FastAPIInstrumentor.instrument_app(app)
    _fastapi_instrumented = True


def instrument_sqlalchemy(engine) -> None:
    global _sqlalchemy_instrumented
    if _sqlalchemy_instrumented:
        return
    setup_tracing()
    if not _tracer:
        return
    try:
        from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
    except Exception:
        return
    sync_engine = getattr(engine, "sync_engine", engine)
    SQLAlchemyInstrumentor().instrument(engine=sync_engine)
    _sqlalchemy_instrumented = True


@contextmanager
def start_span(name: str, attributes: dict | None = None) -> Iterator[None]:
    setup_tracing()
    if not _tracer:
        yield
        return
    with _tracer.start_as_current_span(name) as span:
        if attributes:
            for key, value in attributes.items():
                span.set_attribute(key, str(value))
        yield
