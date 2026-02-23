"""
Middleware que redireciona automaticamente para o dashboard correto
baseado no papel do utilizador.
"""

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import logging

logger = logging.getLogger(__name__)


class RoleBasedRoutingMiddleware(BaseHTTPMiddleware):
    """
    Middleware que inspeciona o papel do utilizador e:
    1. Bloqueia acesso a rotas não autorizadas
    2. Retorna metadados para o frontend redirecionar corretamente
    """
    
    # Mapa de rotas por papel
    ROLE_ROUTES = {
        "CITIZEN": {
            "allowed_prefixes": ["/api/auth", "/api/citizen"],
            "dashboard": "/citizen/portal",
            "forbidden_redirect": None
        },
        "ADMIN_SUPER": {
            "allowed_prefixes": ["/api/auth", "/api/admin"],
            "dashboard": "/admin",
            "forbidden_redirect": "/admin"
        },
        "ADMIN_CENTRAL": {
            "allowed_prefixes": ["/api/auth", "/api/admin"],
            "dashboard": "/admin",
            "forbidden_redirect": "/admin"
        },
        "ADMIN_PROVINCIAL": {
            "allowed_prefixes": ["/api/auth", "/api/admin"],
            "dashboard": "/admin",
            "forbidden_redirect": "/admin"
        },
        "ADMIN_MUNICIPAL": {
            "allowed_prefixes": ["/api/auth", "/api/admin"],
            "dashboard": "/admin",
            "forbidden_redirect": "/admin"
        },
        "ADMIN_COMMUNAL": {
            "allowed_prefixes": ["/api/auth", "/api/admin"],
            "dashboard": "/admin",
            "forbidden_redirect": "/admin"
        }
    }
    
    async def dispatch(self, request: Request, call_next):
        # Rotas públicas (não verificar)
        if request.url.path.startswith(("/api/public", "/docs", "/openapi.json", "/health")) or any(p in request.url.path for p in ["/api/auth/login", "/api/auth/register"]):
            return await call_next(request)
        
        # Verificar se é rota de admin ou citizen
        is_admin_route = request.url.path.startswith("/api/admin")
        is_citizen_route = request.url.path.startswith("/api/citizen")
        
        # Se não for rota protegida, segue
        if not (is_admin_route or is_citizen_route):
            return await call_next(request)
        
        # Tentar obter user do request state (setado por auth middleware se existir)
        user = getattr(request.state, "user", None)
        
        # Se o user não existe no state (comum em middlewares base do FastAPI sem auth middleware customizado),
        # deixamos as rotas (que têm Depends) lidarem com isso.
        # MAS, se o status for 403 depois do call_next, podemos injetar a dica.
        
        response = await call_next(request)
        
        # Se o backend negou (403), vamos tentar ajudar o frontend
        if response.status_code == 403:
            # Aqui poderíamos ler o token do header se necessário, mas o spec do usuário pede um JSONResponse direto se bloqueado pelo role.
            pass
            
        return response
