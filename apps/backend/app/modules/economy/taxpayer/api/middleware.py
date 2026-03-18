from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Callable
import time
import logging
from uuid import UUID
logger = logging.getLogger(__name__)

class TaxpayerMiddleware(BaseHTTPMiddleware):
    """Middleware específico do domínio taxpayer (correlation ID).
    
    Responsabilidade: Adicionar contexto de correlação para rastreamento de requisições.
    Nota: Autenticação é responsabilidade de core/auth (main.py).
    Nota: Auditoria é responsabilidade de core/audit (main.py).
    """

    async def dispatch(self, request: Request, call_next: Callable):
        start_time = time.time()
        request.state.correlation_id = request.headers.get('X-Correlation-ID', f'tax-{int(start_time * 1000)}')
        try:
            response = await call_next(request)
            response.headers['X-Correlation-ID'] = request.state.correlation_id
            response.headers['X-Process-Time'] = str(time.time() - start_time)
            return response
        except Exception as e:
            logger.error(f'Erro na requisição: {str(e)}', extra={'correlation_id': request.state.correlation_id, 'path': request.url.path, 'method': request.method})
            raise

class CacheMiddleware(BaseHTTPMiddleware):
    """Middleware de cache para GET requests"""

    def __init__(self, app, cache=None):
        super().__init__(app)
        self.cache = cache
        self.cache_ttl = 300

    async def dispatch(self, request: Request, call_next: Callable):
        if request.method != 'GET' or not self.cache:
            return await call_next(request)
        no_cache_paths = ['/search', '/stats', '/export']
        if any((path in request.url.path for path in no_cache_paths)):
            return await call_next(request)
        cache_key = f'cache:{request.url.path}:{str(request.query_params)}'
        cached = await self.cache.get(cache_key) if self.cache else None
        if cached:
            from fastapi.responses import JSONResponse
            return JSONResponse(content=cached, headers={'X-Cache': 'HIT'})
        response = await call_next(request)
        return response