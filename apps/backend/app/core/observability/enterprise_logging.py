"""
SILA Enterprise Logging Setup - Configuração Global de Observabilidade

Centraliza a configuração de logging para toda a plataforma, silenciando
logs verbosos de bibliotecas externas e ativando logs estruturados em JSON.

Uso:
    from apps.backend.app.core.observability.enterprise_logging import setup_enterprise_logging

    # No startup da aplicação
    setup_enterprise_logging(
        service_name="sila-api",
        environment="production",
        log_level="INFO"
    )
"""

import logging
import os
import sys

from .context import set_request_context
from .enterprise_formatter import SilaStructuredLogFilter, setup_json_logging


def silence_verbose_loggers():
    """
    Silencia logs verbosos de bibliotecas externas que poluem stdout.
    Preserva logs importantes do SILA e suas dependências críticas.
    """
    logging.getLogger("uvicorn").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.access").setLevel(logging.CRITICAL)
    logging.getLogger("uvicorn.error").setLevel(logging.INFO)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.pool").setLevel(logging.WARNING)
    logging.getLogger("alembic").setLevel(logging.WARNING)
    logging.getLogger("asyncpg").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("aiohttp").setLevel(logging.WARNING)
    logging.getLogger("redis").setLevel(logging.WARNING)
    logging.getLogger("celery").setLevel(logging.WARNING)


def setup_enterprise_logging(
    service_name: str | None = None,
    environment: str | None = None,
    log_level: str = "INFO",
    include_context: bool = True,
    include_traceback: bool = True,
) -> logging.Logger:
    """
    Configura o sistema global de logging para SILA com suporte a:
    - JSON estruturado para indexação em Loki/ELK
    - ContextVars para correlação de requisições
    - Integração com OpenTelemetry (pronta)
    - Silenciamento de libs verbosas

    Args:
        service_name: Nome do serviço (ex: "educacao-api", "saude-api")
        environment: Ambiente (ex: "production", "staging", "development")
        log_level: Nível mínimo de logging
        include_context: Incluir request_id, user_id, etc nos logs
        include_traceback: Incluir stack traces em logs de erro

    Returns:
        O root logger configurado

    Exemplo:
        setup_enterprise_logging(
            service_name="sila-educacao",
            environment="production",
            log_level="INFO"
        )

        logger = logging.getLogger("apps.backend.app.services")
        logger.info("Matricula criada", extra={"matricula_id": "123"})
    """
    if service_name:
        os.environ["SILA_SERVICE_NAME"] = service_name
    if environment:
        os.environ["SILA_ENV"] = environment
    set_request_context(service_name=service_name or os.getenv("SILA_SERVICE_NAME"))
    log_level_int = getattr(logging, log_level.upper(), logging.INFO)
    silence_verbose_loggers()
    root_logger = setup_json_logging(
        logger=logging.getLogger(),
        level=log_level_int,
        include_context=include_context,
        include_traceback=include_traceback,
    )
    if not any(isinstance(h, logging.StreamHandler) for h in root_logger.handlers):
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(log_level_int)
        root_logger.addHandler(handler)
    return root_logger


def get_logger(name: str) -> logging.Logger:
    """
    Obtém um logger configurado para o SILA.

    Uso:
        logger = get_logger(__name__)
        logger.info("Operação concluída")

    Args:
        name: Nome do logger (tipicamente __name__)

    Returns:
        Logger configurado com JSON formatter e contexto
    """
    logger = logging.getLogger(name)
    if not any(
        isinstance(h.formatter, type(None))
        or (
            hasattr(h.formatter, "__class__")
            and "SilaEnterpriseJSONFormatter" in str(h.formatter.__class__)
        )
        for h in logging.root.handlers
    ):
        setup_enterprise_logging()
    if not any(isinstance(f, SilaStructuredLogFilter) for f in logger.filters):
        logger.addFilter(SilaStructuredLogFilter())
    return logger


def setup_global_logging():
    """Alias para setup_enterprise_logging (compatibilidade)."""
    return setup_enterprise_logging()


__all__ = [
    "setup_enterprise_logging",
    "setup_global_logging",
    "get_logger",
    "silence_verbose_loggers",
]
