from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Callable
import time
import logging
from uuid import UUID
import json

logger = logging.getLogger(__name__)


class TaxpayerMiddleware(BaseHTTPMiddleware):
    """Middleware principal do módulo taxpayer"""
    
    async def dispatch(self, request: Request, call_next: Callable):
        start_time = time.time()
        
        request.state.correlation_id = request.headers.get(
            "X-Correlation-ID",
            f"tax-{int(start_time * 1000)}"
        )
        
        try:
            response = await call_next(request)
            response.headers["X-Correlation-ID"] = request.state.correlation_id
            response.headers["X-Process-Time"] = str(time.time() - start_time)
            return response
            
        except Exception as e:
            logger.error(
                f"Erro na requisição: {str(e)}",
                extra={
                    "correlation_id": request.state.correlation_id,
                    "path": request.url.path,
                    "method": request.method
                }
            )
            raise


class AuthenticationMiddleware(BaseHTTPMiddleware):
    """Middleware de autenticação"""
    
    async def dispatch(self, request: Request, call_next: Callable):
        public_paths = [
            "/docs",
            "/redoc",
            "/openapi.json",
            "/health",
            "/api/v1/taxpayer/webhook"
        ]
        
        if any(request.url.path.startswith(path) for path in public_paths):
            return await call_next(request)
        
        request.state.user = None
        request.state.user_id = None
        request.state.user_roles = []
        request.state.user_permissions = []
        
        auth_header = request.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            token = auth_header[7:]
            try:
                request.state.user = {"id": token}
                request.state.user_id = UUID(token[:36])
            except:
                pass
        
        return await call_next(request)


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Middleware de rate limiting"""
    
    def __init__(self, app, limiter=None):
        super().__init__(app)
        self.limiter = limiter
    
    async def dispatch(self, request: Request, call_next: Callable):
        client_ip = request.client.host if request.client else "unknown"
        
        if self.limiter and not await self.limiter.check(f"ratelimit:{client_ip}:{request.url.path}"):
            raise HTTPException(
                status_code=429,
                detail={
                    "message": "Muitas requisições. Tente novamente mais tarde.",
                    "code": "RATE_LIMIT_EXCEEDED"
                }
            )
        
        return await call_next(request)


class AuditMiddleware(BaseHTTPMiddleware):
    """Middleware de auditoria"""
    
    def __init__(self, app, audit_logger=None):
        super().__init__(app)
        self.audit = audit_logger
    
    async def dispatch(self, request: Request, call_next: Callable):
        audit_methods = ["POST", "PUT", "PATCH", "DELETE"]
        
        if request.method not in audit_methods:
            return await call_next(request)
        
        start_time = time.time()
        
        try:
            response = await call_next(request)
            
            if response.status_code < 400 and self.audit:
                await self.audit.log(
                    action=f"{request.method}_{request.url.path}",
                    user_id=getattr(request.state, "user_id", None),
                    entity_type="taxpayer",
                    details={
                        "path": request.url.path,
                        "method": request.method,
                        "status_code": response.status_code,
                        "duration": time.time() - start_time
                    },
                    ip_address=getattr(request.client, "host", None)
                )
            
            return response
            
        except Exception as e:
            if self.audit:
                await self.audit.log_error(
                    error_type="API_ERROR",
                    message=str(e),
                    details={
                        "path": request.url.path,
                        "method": request.method
                    },
                    user_id=getattr(request.state, "user_id", None)
                )
            raise


class CacheMiddleware(BaseHTTPMiddleware):
    """Middleware de cache para GET requests"""
    
    def __init__(self, app, cache=None):
        super().__init__(app)
        self.cache = cache
        self.cache_ttl = 300
    
    async def dispatch(self, request: Request, call_next: Callable):
        if request.method != "GET" or not self.cache:
            return await call_next(request)
        
        no_cache_paths = ["/search", "/stats", "/export"]
        if any(path in request.url.path for path in no_cache_paths):
            return await call_next(request)
        
        cache_key = f"cache:{request.url.path}:{str(request.query_params)}"
        
        cached = await self.cache.get(cache_key) if self.cache else None
        if cached:
            from fastapi.responses import JSONResponse
            return JSONResponse(
                content=cached,
                headers={"X-Cache": "HIT"}
            )
        
        response = await call_next(request)
        
        return response
