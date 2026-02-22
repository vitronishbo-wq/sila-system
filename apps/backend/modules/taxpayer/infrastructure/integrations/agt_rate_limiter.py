"""AGT Rate Limiter"""

import asyncio
import time
from typing import Dict
from collections import defaultdict


class AGTRateLimiter:
    """Rate limiter for AGT calls"""
    
    def __init__(self, max_requests: int = 10, window_seconds: int = 1):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: Dict[str, list] = defaultdict(list)
    
    async def wait_if_needed(self, endpoint: str = "default"):
        """Wait if necessary to respect rate limit"""
        now = time.time()
        window_start = now - self.window_seconds
        
        # Clean old timestamps
        self.requests[endpoint] = [
            ts for ts in self.requests[endpoint]
            if ts > window_start
        ]
        
        # Check if we can make request
        if len(self.requests[endpoint]) >= self.max_requests:
            # Calculate wait time
            oldest = min(self.requests[endpoint])
            wait_time = oldest + self.window_seconds - now
            if wait_time > 0:
                await asyncio.sleep(wait_time)
        
        # Register this request
        self.requests[endpoint].append(now)
