"""
SILA Enterprise JSON Formatter - Logs Estruturados para Loki/ElasticSearch

Transforma logs de Python em JSON estruturado com metadados governamentais:
- request_id para correlação de requisições
- user_id, territory_id para auditoria
- duration_ms, status_code para performance
- version, environment para rastreamento de versão

Pronto para integração com observabilidade de nível gouvernamental.
"""
import json
import logging
import os
import traceback
from datetime import datetime
from typing import Dict, Any, Optional
from .context import get_context_dict

class SilaEnterpriseJSONFormatter(logging.Formatter):
    """
    Formatter JSON estruturado para logs do SILA.
    
    Cada log produz um JSON minimizado (sem quebras):
        {"timestamp":"...", "level":"INFO", "message":"...", "request_id":"..."}
    
    Benefícios:
    - Indexação immediate em Loki/ELK
    - Filtro por request_id: {request_id="abc-123"}
    - Agregação por level, user_id, territory_id
    - Correlação com traces distribuídos (OpenTelemetry)
    """

    def __init__(self, include_context: bool=True, include_traceback: bool=True):
        super().__init__()
        self.include_context = include_context
        self.include_traceback = include_traceback

    def format(self, record: logging.LogRecord) -> str:
        """Formata um LogRecord como JSON."""
        log_data: Dict[str, Any] = {'timestamp': datetime.utcnow().isoformat() + 'Z', 'level': record.levelname, 'logger': record.name, 'message': record.getMessage()}
        log_data['location'] = {'file': record.filename, 'function': record.funcName, 'line': record.lineno}
        if self.include_context:
            context = get_context_dict()
            log_data.update(context)
        if hasattr(record, 'extra') and isinstance(record.extra, dict):
            log_data.update(record.extra)
        for key, value in record.__dict__.items():
            if key not in ['name', 'msg', 'args', 'created', 'filename', 'funcName', 'levelname', 'levelno', 'lineno', 'module', 'msecs', 'message', 'pathname', 'process', 'processName', 'relativeCreated', 'thread', 'threadName', 'extra']:
                if not key.startswith('_'):
                    log_data[key] = value
        if record.exc_info and record.exc_info[0] is not None:
            log_data['error'] = {'type': record.exc_info[0].__name__, 'message': str(record.exc_info[1])}
            if self.include_traceback:
                log_data['error']['traceback'] = traceback.format_exception(*record.exc_info)
        log_data['platform'] = {'environment': os.getenv('SILA_ENV', 'production'), 'version': os.getenv('SILA_VERSION', '3.0.0'), 'service': os.getenv('SILA_SERVICE_NAME', 'unknown')}
        return json.dumps(log_data, ensure_ascii=False, separators=(',', ':'))

class SilaStructuredLogFilter(logging.Filter):
    """
    Filtro que automaticamente injeta context vars em todo LogRecord.
    
    Uso:
        logger.addFilter(SilaStructuredLogFilter())
    """

    def filter(self, record: logging.LogRecord) -> bool:
        """Injeta contexto no record antes de serializar."""
        context = get_context_dict()
        for key, value in context.items():
            if not hasattr(record, key):
                setattr(record, key, value)
        return True

def setup_json_logging(logger: Optional[logging.Logger]=None, level: int=logging.INFO, include_context: bool=True, include_traceback: bool=True) -> logging.Logger:
    """
    Configura um logger para usar o formatter JSON estruturado.
    
    Args:
        logger: Logger a configurar (default: root logger)
        level: Nível mínimo de log
        include_context: Incluir ContextVars nos logs
        include_traceback: Incluir stack traces em logs de erro
    
    Returns:
        O logger configurado
    
    Exemplo:
        logger = setup_json_logging(logging.getLogger("app"))
        logger.info("Serviço iniciado")
    """
    if logger is None:
        logger = logging.getLogger()
    logger.setLevel(level)
    logger.handlers = []
    handler = logging.StreamHandler()
    formatter = SilaEnterpriseJSONFormatter(include_context=include_context, include_traceback=include_traceback)
    handler.setFormatter(formatter)
    handler.setLevel(level)
    handler.addFilter(SilaStructuredLogFilter())
    logger.addHandler(handler)
    return logger
__all__ = ['SilaEnterpriseJSONFormatter', 'SilaStructuredLogFilter', 'setup_json_logging']