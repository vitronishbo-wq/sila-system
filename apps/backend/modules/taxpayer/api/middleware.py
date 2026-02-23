from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Optional, Callable
import time
import logging
from uuid import UUID

from core.config import settings
from ...infrastructure.audit.audit_logger import AuditLogger
from ...infrastructure.cache.redis_cache import RedisCache
from .rate_limiter import RateLimiter


class TaxpayerMiddleware(BaseHTTPMiddleware):
    """Middleware principal do módulo taxpayer"""
    
    def __init__(self, app):
        super().__init__(app)
        self.logger = logging.getLogger(__name__)
        self.rate_limiter = RateLimiter()
        self.cache = RedisCache()
    
    async def dispatch(self, request: Request, call_next: Callable):
        # Registrar início da requisição
        start_time = time.time()
        
        # Adicionar ID de correlação
        request.state.correlation_id = request.headers.get(
            "X-Correlation-ID",
            f"tax-{int(start_time * 1000)}"
        )
        
        # Processar requisição
        try:
            response = await call_next(request)
            
            # Adicionar headers
            response.headers["X-Correlation-ID"] = request.state.correlation_id
            response.headers["X-Process-Time"] = str(time.time() - start_time)
            
            return response
            
        except Exception as e:
            self.logger.error(
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
        # Paths públicos
        public_paths = [
            "/docs",
            "/redoc",
            "/openapi.json",
            "/health",
            "/api/v1/taxpayer/webhook"
        ]
        
        if any(request.url.path.startswith(path) for path in public_paths):
            return await call_next(request)
        
        # Inicializar estado do usuário
        request.state.user = None
        request.state.user_id = None
        request.state.user_roles = []
        request.state.user_permissions = []
        
        # Tentar obter token do header Authorization
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            # Em produção, validar JWT aqui
            # Por enquanto, apenas simular usuário autenticado
            try:
                token = auth_header.split(" ")[1]
                # Token validation would happen here
                request.state.user = {"id": "system", "roles": ["operator"]}
                request.state.user_id = UUID("00000000-0000-0000-0000-000000000000")
                request.state.user_roles = ["operator"]
                request.state.user_permissions = ["taxpayer:read", "taxpayer:write"]
            except:
                pass
        
        return await call_next(request)


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Middleware de rate limiting"""
    
    def __init__(self, app):
        super().__init__(app)
        self.limiter = RateLimiter()
    
    async def dispatch(self, request: Request, call_next: Callable):
        # Rate limit por IP
        client_ip = request.client.host if request.client else "unknown"
        
        # Rate limit por usuário se autenticado
        user_id = getattr(request.state, "user_id", None)
        key = f"ratelimit:{user_id or client_ip}:{request.url.path}"
        
        # Verificar rate limit
        if not await self.limiter.check(key):
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
    
    def __init__(self, app, audit_logger: Optional[AuditLogger] = None):
        super().__init__(app)
        self.audit = audit_logger
        self.logger = logging.getLogger(__name__)
    
    async def dispatch(self, request: Request, call_next: Callable):
        # Métodos que devem ser auditados
        audit_methods = ["POST", "PUT", "PATCH", "DELETE"]
        
        if request.method in audit_methods and self.audit:
            # Registrar início da operação
            start_time = time.time()
            
            try:
                response = await call_next(request)
                
                # Registrar sucesso
                if response.status_code < 400:
                    try:
                        await self.audit.log(
                            action=f"{request.method}_{request.url.path}",
                            user_id=getattr(request.state, "user_id", None),
                            entity_id=request.path_params.get("taxpayer_id"),
                            entity_type="taxpayer",
                            details={
                                "path": request.url.path,
                                "method": request.method,
                                "status_code": response.status_code,
                                "duration": time.time() - start_time
                            },
                            ip_address=request.client.host if request.client else "unknown",
                            user_agent=request.headers.get("user-agent")
                        )
                    except Exception as e:
                        self.logger.warning(f"Erro ao registrar auditoria: {e}")
                
                return response
                
            except Exception as e:
                # Registrar erro
                try:
                    await self.audit.log_error(
                        error_type="API_ERROR",
                        message=str(e),
                        details={
                            "path": request.url.path,
                            "method": request.method
                        },
                        user_id=getattr(request.state, "user_id", None)
                    )
                except:
                    pass
                raise
            
        return await call_next(request)


class CacheMiddleware(BaseHTTPMiddleware):
    """Middleware de cache para GET requests"""
    
    def __init__(self, app):
        super().__init__(app)
        self.cache = RedisCache()
        self.cache_ttl = 300  # 5 minutos
        self.logger = logging.getLogger(__name__)
    
    async def dispatch(self, request: Request, call_next: Callable):
        # Cache apenas para GET
        if request.method != "GET":
            return await call_next(request)
        
        # Não cachear paths específicos
        no_cache_paths = ["/search", "/stats", "/export"]
        if any(path in request.url.path for path in no_cache_paths):
            return await call_next(request)
        
        # Gerar chave de cache
        cache_key = f"cache:{request.url.path}:{str(request.query_params)}"
        
        # Tentar obter do cache
        try:
            cached = await self.cache.get(cache_key)
            if cached:
                from fastapi.responses import JSONResponse
                return JSONResponse(
                    content=cached,
                    headers={"X-Cache": "HIT"}
                )
        except Exception as e:
            self.logger.warning(f"Erro ao obter cache: {e}")
        
        # Processar requisição
        response = await call_next(request)
        
        # Cachear resposta se for sucesso
        if response.status_code == 200:
            try:
                import json
                from starlette.responses import Response
                
                # Extrair conteúdo
                body = b""
                async for chunk in response.body_iterator:
                    body += chunk
                
                # Criar nova resposta
                new_response = Response(
                    content=body,
                    status_code=response.status_code,
                    headers=dict(response.headers)
                )
                new_response.headers["X-Cache"] = "MISS"
                
                # Cachear
                try:
                    await self.cache.set(
                        cache_key,
                        json.loads(body),
                        ttl=self.cache_ttl
                    )
                except:
                    pass
                
                return new_response
            except Exception as e:
                self.logger.warning(f"Erro ao cachear resposta: {e}")
                return response
        
        return response
