"""Cliente HTTP resiliente com retry, circuit breaker e timeout"""

import asyncio
import logging
from typing import Optional
from functools import wraps
import httpx
from datetime import datetime, timedelta

logger = logging.getLogger("sila.resilience")


class CircuitBreaker:
    """Implementação simples de Circuit Breaker"""
    
    def __init__(self, failure_threshold: int = 5, timeout: int = 60):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failure_count = 0
        self.last_failure_time: Optional[datetime] = None
        self.state = "closed"  # closed, open, half-open
    
    def record_success(self):
        """Registrar sucesso"""
        self.failure_count = 0
        self.state = "closed"
    
    def record_failure(self):
        """Registrar falha"""
        self.failure_count += 1
        self.last_failure_time = datetime.now()
        
        if self.failure_count >= self.failure_threshold:
            self.state = "open"
            logger.warning(
                "circuit_breaker.opened",
                extra={"failure_count": self.failure_count}
            )
    
    def can_attempt(self) -> bool:
        """Verificar se pode tentar"""
        if self.state == "closed":
            return True
        
        if self.state == "open":
            if self.last_failure_time and \
               datetime.now() >= self.last_failure_time + timedelta(seconds=self.timeout):
                self.state = "half-open"
                logger.info("circuit_breaker.half_open")
                return True
            return False
        
        return True  # half-open


def with_retry(max_retries: int = 3, backoff_factor: float = 0.5):
    """Decorator para retry com backoff exponencial"""
    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(max_retries):
                try:
                    return await func(*args, **kwargs)
                except (httpx.RequestError, httpx.TimeoutException) as e:
                    last_exception = e
                    
                    if attempt < max_retries - 1:
                        wait_time = backoff_factor * (2 ** attempt)
                        logger.warning(
                            "request.retry",
                            extra={
                                "attempt": attempt + 1,
                                "max_retries": max_retries,
                                "wait_time": wait_time,
                                "error": str(e)
                            }
                        )
                        await asyncio.sleep(wait_time)
                    else:
                        logger.error(
                            "request.failed_after_retries",
                            extra={"attempts": max_retries, "error": str(e)},
                            exc_info=True
                        )
            
            raise last_exception
        
        return async_wrapper
    return decorator


def with_circuit_breaker(breaker: Optional[CircuitBreaker] = None):
    """Decorator para circuit breaker"""
    def decorator(func):
        nonlocal breaker
        if breaker is None:
            breaker = CircuitBreaker()
        
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            if not breaker.can_attempt():
                raise Exception("Circuit breaker is open")
            
            try:
                result = await func(*args, **kwargs)
                breaker.record_success()
                return result
            except Exception as e:
                breaker.record_failure()
                raise
        
        return async_wrapper
    return decorator


def with_timeout(timeout: float = 30.0):
    """Decorator para timeout"""
    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            try:
                return await asyncio.wait_for(
                    func(*args, **kwargs),
                    timeout=timeout
                )
            except asyncio.TimeoutError:
                logger.error(
                    "request.timeout",
                    extra={"timeout": timeout}
                )
                raise
        
        return async_wrapper
    return decorator


class ResilientClient:
    """Cliente HTTP com resiliência embutida"""
    
    def __init__(
        self,
        base_url: str,
        timeout: float = 30.0,
        max_retries: int = 3,
        circuit_breaker: Optional[CircuitBreaker] = None
    ):
        self.base_url = base_url
        self.timeout = timeout
        self.max_retries = max_retries
        self.circuit_breaker = circuit_breaker or CircuitBreaker()
        self.client = httpx.AsyncClient(timeout=timeout)
    
    @with_retry(max_retries=3)
    @with_circuit_breaker()
    @with_timeout(30.0)
    async def get(self, path: str, **kwargs) -> httpx.Response:
        """GET com resiliência"""
        url = f"{self.base_url}{path}"
        logger.debug("request.get", extra={"url": url})
        return await self.client.get(url, **kwargs)
    
    @with_retry(max_retries=3)
    @with_circuit_breaker()
    @with_timeout(30.0)
    async def post(self, path: str, **kwargs) -> httpx.Response:
        """POST com resiliência"""
        url = f"{self.base_url}{path}"
        logger.debug("request.post", extra={"url": url})
        return await self.client.post(url, **kwargs)
    
    @with_retry(max_retries=3)
    @with_circuit_breaker()
    @with_timeout(30.0)
    async def put(self, path: str, **kwargs) -> httpx.Response:
        """PUT com resiliência"""
        url = f"{self.base_url}{path}"
        logger.debug("request.put", extra={"url": url})
        return await self.client.put(url, **kwargs)
    
    @with_retry(max_retries=3)
    @with_circuit_breaker()
    @with_timeout(30.0)
    async def delete(self, path: str, **kwargs) -> httpx.Response:
        """DELETE com resiliência"""
        url = f"{self.base_url}{path}"
        logger.debug("request.delete", extra={"url": url})
        return await self.client.delete(url, **kwargs)
    
    async def close(self):
        """Fechar cliente"""
        await self.client.aclose()
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
