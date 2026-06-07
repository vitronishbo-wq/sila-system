import logging

from pythonjsonlogger import jsonlogger

from .correlation import get_correlation_id


class CorrelationFilter(logging.Filter):

    def filter(self, record):
        try:
            record.correlation_id = get_correlation_id()
        except Exception:
            record.correlation_id = ""
        return True


def configure_logging():

    handler = logging.StreamHandler()

    formatter = jsonlogger.JsonFormatter(
        "%(asctime)s %(levelname)s %(name)s %(message)s %(correlation_id)s"
    )

    handler.setFormatter(formatter)

    root = logging.getLogger()

    root.setLevel(logging.INFO)
    # avoid duplicate handlers
    if not any(isinstance(h, logging.StreamHandler) for h in root.handlers):
        root.addHandler(handler)
    root.addFilter(CorrelationFilter())
