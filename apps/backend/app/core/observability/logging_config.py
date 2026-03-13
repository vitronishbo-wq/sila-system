"""Configuração central de logging alinhada ao pacote de observabilidade."""
import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path
LOG_FORMAT = '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s'
LOG_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

def setup_logging(level: str='INFO', log_file: str | None=None, max_bytes: int=10 * 1024 * 1024, backup_count: int=5) -> None:
    """Inicializa logging global com console + arquivo opcional."""
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    formatter = logging.Formatter(LOG_FORMAT, datefmt=LOG_DATE_FORMAT)
    root_logger.handlers.clear()
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        file_handler = RotatingFileHandler(log_file, maxBytes=max_bytes, backupCount=backup_count)
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)
    _suppress_verbose_loggers()
    root_logger.info('logging.setup.complete', extra={'level': level})

def _suppress_verbose_loggers() -> None:
    noisy = {'sqlalchemy.engine': logging.WARNING, 'sqlalchemy.pool': logging.WARNING, 'alembic': logging.WARNING, 'urllib3.connectionpool': logging.WARNING, 'httpx': logging.WARNING, 'asyncio': logging.WARNING}
    for logger_name, log_level in noisy.items():
        logging.getLogger(logger_name).setLevel(log_level)