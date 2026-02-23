import time
from typing import Dict, Tuple, Optional
from collections import defaultdict
import logging

from core.config import settings


class RateLimiter:
    """Rate limiter para endpoints"""
    
    def __init__(self):
        self.use_redis = settings.REDIS_ENABLED if hasattr(settings, 'REDIS_ENABLED') else False
        self.default_limit = getattr(settings, 'RATE_LIMIT_REQUESTS', 100)
        self.default_window = getattr(settings, 'RATE_LIMIT_WINDOW', 60)  # segundos
        self.logger = logging.getLogger(__name__)
        
        # Configurações específicas por endpoint
        self.endpoint_limits = {
            "/api/v1/taxpayer/register": (5, 3600),  # 5 por hora
            "/api/v1/taxpayer/login": (10, 300),     # 10 por 5 minutos
            "/api/v1/taxpayer/search": (30, 60),     # 30 por minuto
            "/api/v1/taxpayer/webhook": (100, 60),   # 100 por minuto (AGT)
        }
        
        # Fallback para armazenamento em memória
        self.requests: Dict[str, list] = defaultdict(list)
    
    async def check(self, key: str, limit: int = None, window: int = None) -> bool:
        """
        Verifica se requisição pode prosseguir
        Retorna True se permitido, False se bloqueado
        """
        # Extrair endpoint da key
        endpoint = key.split(':')[-1] if ':' in key else key
        endpoint_limit, endpoint_window = self.endpoint_limits.get(
            endpoint, (self.default_limit, self.default_window)
        )
        
        limit = limit or endpoint_limit
        window = window or endpoint_window
        
        now = time.time()
        window_start = now - window
        
        return self._check_memory(key, limit, window_start, now)
    
    def _check_memory(self, key: str, limit: int, window_start: float, now: float) -> bool:
        """Verifica usando memória (fallback)"""
        timestamps = self.requests[key]
        
        # Limpar timestamps antigos
        timestamps = [ts for ts in timestamps if ts > window_start]
        self.requests[key] = timestamps
        
        # Adicionar timestamp atual
        timestamps.append(now)
        
        return len(timestamps) <= limit
    
    async def get_remaining(self, key: str) -> Tuple[int, int]:
        """Retorna limite restante e tempo para reset"""
        endpoint = key.split(':')[-1] if ':' in key else key
        limit, window = self.endpoint_limits.get(
            endpoint, (self.default_limit, self.default_window)
        )
        
        count = len([ts for ts in self.requests[key] 
                    if ts > time.time() - window])
        
        remaining = max(0, limit - count)
        reset = int(time.time() + window)
        
        return remaining, reset
