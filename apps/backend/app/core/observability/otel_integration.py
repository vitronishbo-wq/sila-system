"""
SILA OpenTelemetry Integration - Distributed Tracing Pronto

Fornece integração com OpenTelemetry (OTel) para rastreamento distribuído.
Com 900+ serviços, é crítico saber: "Quanto tempo levou de Educação até Saúde?"

Suporta exporters para:
- Jaeger (self-hosted)
- Tempo (compatível com Grafana)
- OTLP (Open Telemetry Protocol → backend qualquer)

Uso:
    from app.core.observability.otel_integration import setup_otel_tracing
    
    setup_otel_tracing(
        service_name="sila-educacao",
        environment="production"
    )
    
    # OTel automáticamente instrumenta FastAPI, SQLAlchemy, requests, etc
"""
from __future__ import annotations

import os
from typing import Optional
try:
    from opentelemetry import trace, metrics
    from opentelemetry.exporter.jaeger.thrift import JaegerExporter
    from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor
    from opentelemetry.sdk.resources import SERVICE_NAME, Resource
    from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
    from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
    from opentelemetry.instrumentation.requests import RequestsInstrumentor
    from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
    OTEL_AVAILABLE = True
except ImportError:
    OTEL_AVAILABLE = False
    trace = None
    metrics = None

def setup_otel_tracing(service_name: str='sila-service', environment: str='production', exporter_type: str='jaeger', jaeger_host: str='localhost', jaeger_port: int=6831, otlp_endpoint: Optional[str]=None) -> Optional[trace.Tracer]:
    """
    Configura OpenTelemetry para rastreamento distribuído.
    
    Args:
        service_name: Nome do serviço
        environment: Ambiente (production, staging, dev)
        exporter_type: Tipo de exporter ("jaeger", "otlp", "none")
        jaeger_host: Host do Jaeger (se exporter_type="jaeger")
        jaeger_port: Porta do Jaeger (padrão: 6831 para UDP)
        otlp_endpoint: Endpoint do OTLP (ex: "localhost:4317")
    
    Returns:
        Tracer provider, ou None se OTel não disponível
    
    Exemplo:
        setup_otel_tracing(
            service_name="educacao-api",
            environment="production",
            exporter_type="otlp",
            otlp_endpoint="otel-collector:4317"
        )
    """
    if not OTEL_AVAILABLE or trace is None:
        print('⚠️  OpenTelemetry não está instalado. Tracing desabilitado.')
        print('   Instale com: pip install opentelemetry-api opentelemetry-sdk')
        print('   E instrumentadores: pip install opentelemetry-instrumentation-fastapi')
        return None
    resource = Resource.create({SERVICE_NAME: service_name, 'service.version': os.getenv('SILA_VERSION', '3.0.0'), 'deployment.environment': environment})
    exporter = None
    if exporter_type == 'jaeger':
        exporter = JaegerExporter(agent_host_name=jaeger_host, agent_port=jaeger_port)
        print(f'✅ OTel exportador: Jaeger ({jaeger_host}:{jaeger_port})')
    elif exporter_type == 'otlp':
        endpoint = otlp_endpoint or os.getenv('OTEL_EXPORTER_OTLP_ENDPOINT', 'localhost:4317')
        exporter = OTLPSpanExporter(endpoint=endpoint)
        print(f'✅ OTel exportador: OTLP ({endpoint})')
    else:
        print("ℹ️  OTel tracing desabilitado (exporter_type='none')")
        return trace.get_tracer(__name__)
    tracer_provider = TracerProvider(resource=resource)
    tracer_provider.add_span_processor(BatchSpanProcessor(exporter))
    trace.set_tracer_provider(tracer_provider)
    try:
        FastAPIInstrumentor.instrument()
        print('✅ Instrumentado: FastAPI')
    except Exception as e:
        print(f'⚠️  FastAPI instrumentation: {e}')
    try:
        SQLAlchemyInstrumentor().instrument()
        print('✅ Instrumentado: SQLAlchemy')
    except Exception as e:
        print(f'⚠️  SQLAlchemy instrumentation: {e}')
    try:
        RequestsInstrumentor().instrument()
        print('✅ Instrumentado: requests')
    except Exception as e:
        print(f'⚠️  requests instrumentation: {e}')
    try:
        HTTPXClientInstrumentor().instrument()
        print('✅ Instrumentado: httpx')
    except Exception as e:
        print(f'⚠️  httpx instrumentation: {e}')
    return trace.get_tracer(__name__)

def get_tracer(name: str) -> Optional[trace.Tracer]:
    """
    Obtém um tracer para a aplicação.
    
    Uso:
        tracer = get_tracer(__name__)
        with tracer.start_as_current_span("process_matricula"):
            # lógica aqui
    """
    if not OTEL_AVAILABLE or trace is None:
        return None
    return trace.get_tracer(name)

def create_span_with_context(name: str, attributes: Optional[dict]=None) -> Optional[trace.Span]:
    """
    Cria um span com atributos do contexto SILA.
    
    Uso:
        with create_span_with_context("criar_matricula", 
                                      {"matricula_id": "123"}) as span:
            # lógica aqui
    """
    tracer = get_tracer(__name__)
    if tracer is None:
        return None
    span = tracer.start_span(name)
    if attributes:
        for key, value in attributes.items():
            span.set_attribute(key, value)
    return span
__all__ = ['setup_otel_tracing', 'get_tracer', 'create_span_with_context', 'OTEL_AVAILABLE']
