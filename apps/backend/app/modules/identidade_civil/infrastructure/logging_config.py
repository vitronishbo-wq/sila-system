"""
Logging Estruturado - Módulo Identidade Civil

Configuração centralizada de logging com contexto de auditoria,
rastreamento distribuído e integração com sistemas de observabilidade.
"""
import logging
from datetime import datetime
from contextlib import contextmanager
from typing import Dict, Any


class StructuredLogger:
    """Logger estruturado com contexto de auditoria para Identidade Civil."""

    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        self.context: Dict[str, Any] = {}

    def set_context(self, **kwargs):
        """Define o contexto do logger (cidadão, operador, requisição, etc)."""
        self.context.update(kwargs)

    def clear_context(self):
        """Limpa o contexto."""
        self.context.clear()

    @contextmanager
    def audit_context(self, operation: str, **kwargs):
        """Context manager para auditoria de operações."""
        audit_id = kwargs.pop("audit_id", None)
        citizen_fuc_id = kwargs.pop("citizen_fuc_id", None)
        operator_id = kwargs.pop("operator_id", None)

        audit_log = {
            "audit_id": audit_id,
            "operation": operation,
            "citizen_fuc_id": citizen_fuc_id,
            "operator_id": operator_id,
            "timestamp": datetime.utcnow().isoformat(),
            "extra": kwargs,
        }

        self.logger.info(
            f"AUDIT_START: {operation}",
            extra={"audit": audit_log},
        )

        try:
            yield audit_log
            self.logger.info(
                f"AUDIT_SUCCESS: {operation}",
                extra={"audit": audit_log},
            )
        except Exception as e:
            audit_log["error"] = str(e)
            audit_log["error_type"] = type(e).__name__
            self.logger.error(
                f"AUDIT_FAILURE: {operation}",
                extra={"audit": audit_log},
                exc_info=True,
            )
            raise

    def info(self, message: str, **kwargs):
        """Log com nível INFO."""
        self.logger.info(message, extra={"context": self.context, **kwargs})

    def warning(self, message: str, **kwargs):
        """Log com nível WARNING."""
        self.logger.warning(message, extra={"context": self.context, **kwargs})

    def error(self, message: str, **kwargs):
        """Log com nível ERROR."""
        self.logger.error(message, extra={"context": self.context, **kwargs})

    def debug(self, message: str, **kwargs):
        """Log com nível DEBUG."""
        self.logger.debug(message, extra={"context": self.context, **kwargs})

    def critical(self, message: str, **kwargs):
        """Log com nível CRITICAL."""
        self.logger.critical(message, extra={"context": self.context, **kwargs})


# Factory para criar loggers estruturados
def get_structured_logger(name: str) -> StructuredLogger:
    """Cria ou retorna um logger estruturado."""
    return StructuredLogger(name)


# Loggers centralizados por componente
logger_emission = get_structured_logger("identidade_civil.emission")
logger_query = get_structured_logger("identidade_civil.query")
logger_alter = get_structured_logger("identidade_civil.alter")
logger_repository = get_structured_logger("identidade_civil.repository")
logger_integration = get_structured_logger("identidade_civil.integration")
