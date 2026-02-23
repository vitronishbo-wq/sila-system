import time
from typing import Dict, Tuple, Optional
from collections import defaultdict


class RateLimiter:
    """Rate limiter para endpoints"""
    
    def __init__(self):
        self.default_limit = 100
        self.default_window = 60
        
        self.endpoint_limits = {
            "/api/v1/taxpayer/register": (5, 3600),
            "/api/v1/taxpayer/login": (10, 300),
            "/api/v1/taxpayer/search": (30, 60),
            "/api/v1/taxpayer/webhook": (100, 60),
        }
        
        self.requests: Dict[str, list] = defaultdict(list)
    
    async def check(self, key: str, limit: int = None, window: int = None) -> bool:
        """Verifica se requisição pode prosseguir"""
        endpoint = key.split(':')[-1] if ':' in key else key
        endpoint_limit, endpoint_window = self.endpoint_limits.get(
            endpoint, (self.default_limit, self.default_window)
        )
        
        limit = limit or endpoint_limit
        window = window or endpoint_window
        
        now = time.time()
        window_start = now - window
        
        timestamps = self.requests[key]
        timestamps = [ts for ts in timestamps if ts > window_start]
        self.requests[key] = timestamps
        
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
