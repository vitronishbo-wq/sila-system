from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from ..threat_detection.application.threat_engine import ThreatEngine
threat_engine = ThreatEngine()

class SecurityMiddleware(BaseHTTPMiddleware):
    """Global security middleware for all services"""

    async def dispatch(self, request: Request, call_next):
        """Check threat status before processing request"""
        ip = request.client.host
        status = threat_engine.register_ip(ip)
        if status == 'blacklisted':
            return JSONResponse({'error': 'access_denied'}, status_code=403)
        response = await call_next(request)
        return response