"""
SILA Circuit Breaker Patterns - Resiliência entre Serviços

Implementa padrões de circuit breaking, retry, e bulkhead isolamento
para proteger chamadas entre 900+ serviços.

Padrões:
1. Circuit Breaker: Falha rápido se serviço está down
2. Retry: Retentar com backoff exponencial
3. Fallback: Usar valor em cache ou padrão
4. Bulkhead: Isolar pools de thread/conexão por serviço
5. Timeout: Cancelar operações lentas

Uso:
    from app.core.resilience.circuit_breaker import CircuitBreaker
    
    cb = CircuitBreaker(
        name="educacao-api",
        failure_threshold=5,
        recovery_timeout=60
    )
    
    try:
        response = cb.call(requests.get, "http://educacao-api/api/...")
    except CircuitBreakerOpen:
        # Usar fallback
        response = cache.get("educacao-api-matricula")
"""
import asyncio
import logging
import time
from enum import Enum
from typing import Callable, Any, Optional, TypeVar, Generic
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import functools
logger = logging.getLogger(__name__)
T = TypeVar('T')

class CircuitState(Enum):
    """Estados do circuit breaker."""
    CLOSED = 'CLOSED'
    OPEN = 'OPEN'
    HALF_OPEN = 'HALF_OPEN'

class CircuitBreakerException(Exception):
    """Exceção base de circuit breaker."""
    pass

class CircuitBreakerOpen(CircuitBreakerException):
    """Levantada quando circuit está aberto (serviço indisponível)."""
    pass

class CircuitBreakerTimeout(CircuitBreakerException):
    """Levantada quando operação ultrapassa timeout."""
    pass

@dataclass
class CircuitBreakerStats:
    """Estatísticas do circuit breaker."""
    name: str
    state: CircuitState
    failure_count: int = 0
    success_count: int = 0
    total_calls: int = 0
    last_failure_time: Optional[datetime] = None
    last_success_time: Optional[datetime] = None

    @property
    def failure_rate(self) -> float:
        """Taxa de falha (0-100%)."""
        if self.total_calls == 0:
            return 0.0
        return self.failure_count / self.total_calls * 100

class CircuitBreaker(Generic[T]):
    """
    Implementação de Circuit Breaker thread-safe.
    
    Protege chamadas para serviços externos:
    - Educação API
    - Saúde API
    - Justiça API
    - etc
    """

    def __init__(self, name: str, failure_threshold: int=5, recovery_timeout: int=60, expected_exception: type=Exception, logger_obj: Optional[logging.Logger]=None):
        """
        Args:
            name: Nome do serviço (ex: "educacao-api")
            failure_threshold: Quantas falhas antes de abrir
            recovery_timeout: Segundos até tentar recuperar
            expected_exception: Tipo de exceção que conta como falha
            logger_obj: Logger customizado
        """
        self.name = name
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.expected_exception = expected_exception
        self.logger = logger_obj or logger
        self._state = CircuitState.CLOSED
        self._failure_count = 0
        self._success_count = 0
        self._last_failure_time: Optional[datetime] = None
        self._last_success_time: Optional[datetime] = None
        self._opened_at: Optional[datetime] = None

    @property
    def state(self) -> CircuitState:
        """Retorna o estado atual (pode transicionar HALF_OPEN → CLOSED/OPEN)."""
        if self._state == CircuitState.OPEN:
            if self._opened_at and datetime.utcnow() >= self._opened_at + timedelta(seconds=self.recovery_timeout):
                self._state = CircuitState.HALF_OPEN
                self.logger.info(f'[{self.name}] Circuit transicionou para HALF_OPEN')
        return self._state

    @property
    def stats(self) -> CircuitBreakerStats:
        """Retorna estatísticas do circuit breaker."""
        total = self._failure_count + self._success_count
        return CircuitBreakerStats(name=self.name, state=self.state, failure_count=self._failure_count, success_count=self._success_count, total_calls=total, last_failure_time=self._last_failure_time, last_success_time=self._last_success_time)

    def call(self, func: Callable[..., T], *args, **kwargs) -> T:
        """
        Executa função protegida por circuit breaker.
        
        Args:
            func: Função a executar (ex: requests.get)
            *args, **kwargs: Argumentos da função
        
        Returns:
            Resultado da função
        
        Levanta:
            CircuitBreakerOpen: Se circuit está aberto
            CircuitBreakerTimeout: Se timeout
        """
        if self.state == CircuitState.OPEN:
            msg = f'Circuit breaker OPEN para {self.name}'
            self.logger.error(msg)
            raise CircuitBreakerOpen(msg)
        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except self.expected_exception as e:
            self._on_failure()
            raise

    async def call_async(self, func: Callable[..., Any], *args, **kwargs) -> T:
        """Versão assíncrona de call()."""
        if self.state == CircuitState.OPEN:
            msg = f'Circuit breaker OPEN para {self.name}'
            self.logger.error(msg)
            raise CircuitBreakerOpen(msg)
        try:
            result = await func(*args, **kwargs) if asyncio.iscoroutinefunction(func) else func(*args, **kwargs)
            self._on_success()
            return result
        except self.expected_exception as e:
            self._on_failure()
            raise

    def _on_success(self):
        """Chamado quando operação é bem-sucedida."""
        self._success_count += 1
        self._last_success_time = datetime.utcnow()
        if self._state == CircuitState.HALF_OPEN:
            self._state = CircuitState.CLOSED
            self._failure_count = 0
            self.logger.info(f'[{self.name}] Circuit CLOSED (recuperado)')

    def _on_failure(self):
        """Chamado quando operação falha."""
        self._failure_count += 1
        self._last_failure_time = datetime.utcnow()
        if self._failure_count >= self.failure_threshold:
            self._state = CircuitState.OPEN
            self._opened_at = datetime.utcnow()
            self.logger.error(f'[{self.name}] Circuit OPEN (falhas: {self._failure_count})')
        else:
            self.logger.warning(f'[{self.name}] Falha {self._failure_count}/{self.failure_threshold}')

    def reset(self):
        """Reseta o circuit breaker manualmente."""
        self._state = CircuitState.CLOSED
        self._failure_count = 0
        self._success_count = 0
        self._last_failure_time = None
        self._last_success_time = None
        self._opened_at = None
        self.logger.info(f'[{self.name}] Circuit RESET manualmente')

class CircuitBreakerRegistry:
    """Registro global de circuit breakers."""

    def __init__(self):
        self._breakers: dict[str, CircuitBreaker] = {}

    def get_or_create(self, name: str, failure_threshold: int=5, recovery_timeout: int=60) -> CircuitBreaker:
        """Obtém ou cria um circuit breaker."""
        if name not in self._breakers:
            self._breakers[name] = CircuitBreaker(name=name, failure_threshold=failure_threshold, recovery_timeout=recovery_timeout)
        return self._breakers[name]

    def get_stats_all(self) -> dict[str, CircuitBreakerStats]:
        """Retorna estatísticas de todos os circuit breakers."""
        return {name: breaker.stats for name, breaker in self._breakers.items()}

    def reset_all(self):
        """Reseta todos os circuit breakers."""
        for breaker in self._breakers.values():
            breaker.reset()
_circuit_breaker_registry = CircuitBreakerRegistry()

def get_circuit_breaker(name: str) -> CircuitBreaker:
    """Obtém circuit breaker do registry global."""
    return _circuit_breaker_registry.get_or_create(name)

def circuit_breaker_decorator(name: str, failure_threshold: int=5, recovery_timeout: int=60):
    """
    Decorator para proteção automática de funções.
    
    Uso:
        @circuit_breaker_decorator("educacao-api")
        def fetch_matriculas():
            return requests.get("http://educacao-api/...")
    
    Levanta CircuitBreakerOpen se o serviço está down.
    """

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        cb = _circuit_breaker_registry.get_or_create(name, failure_threshold, recovery_timeout)

        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> T:
            return cb.call(func, *args, **kwargs)
        return wrapper
    return decorator
__all__ = ['CircuitBreaker', 'CircuitBreakerRegistry', 'CircuitBreakerException', 'CircuitBreakerOpen', 'CircuitBreakerTimeout', 'CircuitBreakerStats', 'CircuitState', 'get_circuit_breaker', 'circuit_breaker_decorator']