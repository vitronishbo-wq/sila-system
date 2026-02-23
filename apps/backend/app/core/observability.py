"""Core Observability - Logs, Metrics, Tracing"""
import logging
import time
import json
from typing import Callable
from functools import wraps
from datetime import datetime
import os
import asyncio

# Structured logging
class StructuredLogger:
    """Logger estruturado para produção"""
    
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        self.service = os.getenv("SERVICE_NAME", "sila-api")
        self.environment = os.getenv("ENVIRONMENT", "development")
    
    def _log(self, level: str, message: str, **kwargs):
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": level,
            "service": self.service,
            "environment": self.environment,
            "message": message,
            **kwargs
        }
        getattr(self.logger, level.lower())(json.dumps(log_entry))
    
    def info(self, message: str, **kwargs):
        self._log("INFO", message, **kwargs)
    
    def error(self, message: str, **kwargs):
        self._log("ERROR", message, **kwargs)
    
    def warning(self, message: str, **kwargs):
        self._log("WARNING", message, **kwargs)
    
    def debug(self, message: str, **kwargs):
        self._log("DEBUG", message, **kwargs)

# Metrics
class Metrics:
    """Coleta de métricas"""
    _metrics = {}
    
    @classmethod
    def increment(cls, metric: str, value: float = 1, tags: dict = None):
        if metric not in cls._metrics:
            cls._metrics[metric] = []
        cls._metrics[metric].append({
            "value": value,
            "timestamp": time.time(),
            "tags": tags or {}
        })
    
    @classmethod
    def timing(cls, metric: str, duration: float, tags: dict = None):
        cls.increment(f"{metric}_duration", duration, tags)
    
    @classmethod
    def get_metrics(cls):
        return cls._metrics

# Tracing
class Trace:
    """Tracing contextual"""
    def __init__(self, name: str, **tags):
        self.name = name
        self.tags = tags
        self.start_time = None
    
    def __enter__(self):
        self.start_time = time.time()
        return self
    
    def __exit__(self, *args):
        duration = time.time() - self.start_time
        Metrics.timing(self.name, duration, self.tags)

# Decorator para tracing automático
def trace(name: str = None, **default_tags):
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            trace_name = name or func.__name__
            with Trace(trace_name, **default_tags):
                return await func(*args, **kwargs)
        
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            trace_name = name or func.__name__
            with Trace(trace_name, **default_tags):
                return func(*args, **kwargs)
        
        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper
    return decorator

# Logger global
logger = StructuredLogger("sila")

__all__ = ["logger", "Metrics", "Trace", "trace", "StructuredLogger"]
