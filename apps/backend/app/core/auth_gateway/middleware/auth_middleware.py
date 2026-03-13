from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from ..infrastructure.security.jwt_engine import JWTEngine

jwt_engine = JWTEngine()


class AuthMiddleware(BaseHTTPMiddleware):
    """Global authentication middleware for all SILA services"""

    async def dispatch(self, request: Request, call_next):
        """Extract and validate JWT from Authorization header"""
        auth = request.headers.get("Authorization")

        if auth and auth.startswith("Bearer"):
            token = auth.split(" ")[1]
            try:
                payload = jwt_engine.verify(token)
                request.state.user = payload
            except Exception:
                request.state.user = None
        else:
            request.state.user = None

        response = await call_next(request)
        return response
