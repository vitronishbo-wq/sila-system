"""Middleware global de observabilidade para SILA"""

import time
import logging
from typing import Callable
from fastapi import Request, Response
from functools import wraps

logger = logging.getLogger("sila.observability")


class Metrics:
    """Singleton para registro de métricas"""
    
    _metrics = {}
    
    @classmethod
    def increment(cls, metric_name: str, value: int = 1, tags: dict = None):
        """Incrementar métrica"""
        key = f"{metric_name}:{tags}" if tags else metric_name
        cls._metrics[key] = cls._metrics.get(key, 0) + value
        logger.info(f"metric.increment", extra={"metric": metric_name, "value": value, "tags": tags})
    
    @classmethod
    def timing(cls, metric_name: str, duration: float, tags: dict = None):
        """Registrar timing de operação"""
        key = f"{metric_name}:{tags}" if tags else metric_name
        logger.info(f"metric.timing", extra={"metric": metric_name, "duration": f"{duration:.3f}s", "tags": tags})
    
    @classmethod
    def gauge(cls, metric_name: str, value: float, tags: dict = None):
        """Registrar gauge"""
        logger.info(f"metric.gauge", extra={"metric": metric_name, "value": value, "tags": tags})


async def observability_middleware(request: Request, call_next: Callable) -> Response:
    """Middleware de observabilidade para todas as requisições"""
    
    start_time = time.time()
    path = request.url.path
    method = request.method
    
    # Log de entrada
    logger.info(
        "request.start",
        extra={
            "method": method,
            "path": path,
            "client": request.client.host if request.client else "unknown",
        }
    )
    
    try:
        response = await call_next(request)
        status_code = response.status_code
        
    except Exception as e:
        duration = time.time() - start_time
        logger.error(
            "request.error",
            extra={
                "method": method,
                "path": path,
                "error": str(e),
                "duration": f"{duration:.3f}s"
            },
            exc_info=True
        )
        Metrics.increment("request.error", tags={"path": path, "method": method})
        raise
    
    finally:
        duration = time.time() - start_time
        
        # Registrar métricas
        Metrics.timing("request.duration", duration, tags={"path": path, "method": method})
        Metrics.increment("request.total", tags={"path": path, "method": method})
        
        if 'status_code' in locals():
            Metrics.increment(
                "request.status",
                tags={"path": path, "method": method, "status": status_code}
            )
            
            log_level = "info" if status_code < 400 else "warning" if status_code < 500 else "error"
            logger.log(
                getattr(logging, log_level.upper()),
                "request.complete",
                extra={
                    "method": method,
                    "path": path,
                    "status": status_code,
                    "duration": f"{duration:.3f}s"
                }
            )
    
    return response


def trace(operation_name: str = None):
    """Decorator para tracing de operações"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            op_name = operation_name or func.__name__
            start_time = time.time()
            
            logger.info(f"operation.start", extra={"operation": op_name})
            
            try:
                result = await func(*args, **kwargs)
                duration = time.time() - start_time
                logger.info(
                    "operation.complete",
                    extra={"operation": op_name, "duration": f"{duration:.3f}s"}
                )
                Metrics.timing(f"operation.{op_name}", duration)
                return result
            except Exception as e:
                duration = time.time() - start_time
                logger.error(
                    "operation.error",
                    extra={
                        "operation": op_name,
                        "error": str(e),
                        "duration": f"{duration:.3f}s"
                    },
                    exc_info=True
                )
                Metrics.increment(f"operation.{op_name}.error")
                raise
        
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            op_name = operation_name or func.__name__
            start_time = time.time()
            
            logger.info(f"operation.start", extra={"operation": op_name})
            
            try:
                result = func(*args, **kwargs)
                duration = time.time() - start_time
                logger.info(
                    "operation.complete",
                    extra={"operation": op_name, "duration": f"{duration:.3f}s"}
                )
                Metrics.timing(f"operation.{op_name}", duration)
                return result
            except Exception as e:
                duration = time.time() - start_time
                logger.error(
                    "operation.error",
                    extra={
                        "operation": op_name,
                        "error": str(e),
                        "duration": f"{duration:.3f}s"
                    },
                    exc_info=True
                )
                Metrics.increment(f"operation.{op_name}.error")
                raise
        
        # Return appropriate wrapper
        import inspect
        if inspect.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper
    
    return decorator
