import time


class RateLimiter:
    """Rate limiter for API gateway protection"""

    store = {}
    limit = 200  # 200 requests per 60 second window
    window = 60

    def allow(self, ip):
        """Check if IP is within rate limit"""
        now = time.time()

        if ip not in self.store:
            self.store[ip] = []

        # Clean old entries outside window
        self.store[ip] = [
            t for t in self.store[ip]
            if now - t < self.window
        ]

        if len(self.store[ip]) >= self.limit:
            return False

        self.store[ip].append(now)
        return True
