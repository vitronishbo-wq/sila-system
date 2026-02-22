import logging
import sys
from apps.backend.core.config import settings


def setup_logging() -> None:
    logging.basicConfig(
        level=settings.LOG_LEVEL,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )

    # Create a logger instance for the application
    logger = logging.getLogger("backend")
    logger.setLevel(settings.LOG_LEVEL)

    return logger
