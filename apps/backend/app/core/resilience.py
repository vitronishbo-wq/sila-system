"""Core Resilience - Circuit Breaker, Retry, Timeout"""
import asyncio
import logging
import time
from typing import TypeVar, Callable, Any
from functools import wraps
from datetime import datetime

T = TypeVar('T')

logger = logging.getLogger(__name__)

class CircuitBreaker:
    """Circuit Breaker pattern implementation"""
    
    def __init__(self, 
                 failure_threshold: int = 5,
                 recovery_timeout: float = 60.0,
                 name: str = "default"):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.name = name
        
        self.failure_count = 0
        self.last_failure_time = None
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN
    
    async def call(self, func: Callable[..., T], *args, **kwargs) -> T:
        """Execute function with circuit breaker"""
        
        if self.state == "OPEN":
            if time.time() - (self.last_failure_time or 0) > self.recovery_timeout:
                self.state = "HALF_OPEN"
                logger.info(f"Circuit {self.name} half-open")
            else:
                raise Exception(f"Circuit {self.name} is OPEN")
        
        try:
            result = await func(*args, **kwargs) if asyncio.iscoroutinefunction(func) else func(*args, **kwargs)
            
            if self.state == "HALF_OPEN":
                self.state = "CLOSED"
                self.failure_count = 0
                logger.info(f"Circuit {self.name} closed")
            
            return result
            
        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = time.time()
            
            if self.failure_count >= self.failure_threshold:
                self.state = "OPEN"
                logger.warning(f"Circuit {self.name} opened after {self.failure_count} failures")
            
            raise e

class Retry:
    """Retry pattern with exponential backoff"""
    
    def __init__(self, 
                 max_retries: int = 3,
                 base_delay: float = 1.0,
                 max_delay: float = 30.0,
                 exponential_base: float = 2.0):
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.exponential_base = exponential_base
    
    async def execute(self, func: Callable[..., T], *args, **kwargs) -> T:
        """Execute with retries"""
        last_exception = None
        
        for attempt in range(self.max_retries):
            try:
                return await func(*args, **kwargs) if asyncio.iscoroutinefunction(func) else func(*args, **kwargs)
            except Exception as e:
                last_exception = e
                
                if attempt < self.max_retries - 1:
                    delay = min(self.base_delay * (self.exponential_base ** attempt), self.max_delay)
                    logger.warning(f"Retry {attempt + 1}/{self.max_retries} after {delay}s: {e}")
                    await asyncio.sleep(delay)
        
        raise last_exception

class Timeout:
    """Timeout pattern"""
    
    def __init__(self, seconds: float):
        self.seconds = seconds
    
    async def execute(self, func: Callable[..., T], *args, **kwargs) -> T:
        """Execute with timeout"""
        try:
            if asyncio.iscoroutinefunction(func):
                return await asyncio.wait_for(func(*args, **kwargs), timeout=self.seconds)
            else:
                return await asyncio.wait_for(asyncio.to_thread(func, *args, **kwargs), timeout=self.seconds)
        except asyncio.TimeoutError:
            raise Exception(f"Timeout after {self.seconds}s")

# Decorators
def with_circuit_breaker(name: str = None, failure_threshold: int = 5, recovery_timeout: float = 60.0):
    """Circuit breaker decorator"""
    breakers = {}
    
    def decorator(func: Callable) -> Callable:
        breaker_name = name or func.__name__
        if breaker_name not in breakers:
            breakers[breaker_name] = CircuitBreaker(failure_threshold, recovery_timeout, breaker_name)
        
        @wraps(func)
        async def wrapper(*args, **kwargs):
            return await breakers[breaker_name].call(func, *args, **kwargs)
        
        return wrapper
    return decorator

def with_retry(max_retries: int = 3, base_delay: float = 1.0):
    """Retry decorator"""
    retry = Retry(max_retries, base_delay)
    
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            return await retry.execute(func, *args, **kwargs)
        return wrapper
    return decorator

def with_timeout(seconds: float):
    """Timeout decorator"""
    timeout = Timeout(seconds)
    
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            return await timeout.execute(func, *args, **kwargs)
        return wrapper
    return decorator

__all__ = [
    "CircuitBreaker", "Retry", "Timeout",
    "with_circuit_breaker", "with_retry", "with_timeout"
]
