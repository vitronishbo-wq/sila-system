import json
import logging
import sys
from datetime import datetime


class SilaJSONFormatter(logging.Formatter):
    def format(self, record):
        log_obj = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "domain": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
        }
        return json.dumps(log_obj)


def get_sila_logger(domain: str):
    logger = logging.getLogger(domain.lower())
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(SilaJSONFormatter())
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger
