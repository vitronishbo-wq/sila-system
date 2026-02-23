from typing import Set, List, Dict
from datetime import datetime

from ..repositories.permission_repository import PermissionRepository
from ..repositories.user_repository import UserRepository


class PermissionResolver:
    """Resolvedor de permissões com cache"""
    
    def __init__(self, 
                 permission_repo: PermissionRepository,
                 user_repo: UserRepository,
                 cache_ttl: int = 300):  # 5 minutos
        self.permission_repo = permission_repo
        self.user_repo = user_repo
        self.cache_ttl = cache_ttl
        self._cache = {}
        self._cache_timestamps = {}
    
    def get_user_permissions(self, user_id: str) -> Set[str]:
        """Obtém todas as permissões de um usuário (com cache)"""
        # Verifica cache
        cache_key = f"user_perms:{user_id}"
        if cache_key in self._cache:
            timestamp = self._cache_timestamps.get(cache_key)
            if timestamp and (datetime.now() - timestamp).seconds < self.cache_ttl:
                return self._cache[cache_key]
        
        # Busca do repositório
        permissions = self.permission_repo.get_by_user(user_id)
        perm_codes = {f"{p.resource}:{p.action}" for p in permissions}
        
        # Atualiza cache
        self._cache[cache_key] = perm_codes
        self._cache_timestamps[cache_key] = datetime.now()
        
        return perm_codes
    
    def has_permission(self, user_id: str, resource: str, action: str) -> bool:
        """Verifica se usuário tem permissão específica"""
        permissions = self.get_user_permissions(user_id)
        permission_code = f"{resource}:{action}"
        return permission_code in permissions
    
    def has_any_permission(self, user_id: str, *permission_codes: str) -> bool:
        """Verifica se usuário tem qualquer uma das permissões"""
        permissions = self.get_user_permissions(user_id)
        
        for perm_code in permission_codes:
            if perm_code in permissions:
                return True
        
        return False
    
    def has_all_permissions(self, user_id: str, *permission_codes: str) -> bool:
        """Verifica se usuário tem todas as permissões"""
        permissions = self.get_user_permissions(user_id)
        
        for perm_code in permission_codes:
            if perm_code not in permissions:
                return False
        
        return True
    
    def filter_by_permission(self, user_ids: List[str], 
                           resource: str,
                           action: str) -> List[str]:
        """Filtra usuários que têm uma permissão"""
        result = []
        for user_id in user_ids:
            if self.has_permission(user_id, resource, action):
                result.append(user_id)
        return result
    
    def get_permissions_matrix(self, user_id: str) -> Dict[str, List[str]]:
        """Retorna matriz de permissões (recurso -> ações)"""
        permissions = self.get_user_permissions(user_id)
        matrix = {}
        
        for perm_code in permissions:
            parts = perm_code.split(":")
            if len(parts) == 2:
                resource, action = parts
                if resource not in matrix:
                    matrix[resource] = []
                if action not in matrix[resource]:
                    matrix[resource].append(action)
        
        return matrix
    
    def invalidate_cache(self, user_id: str):
        """Invalida cache para um usuário"""
        cache_key = f"user_perms:{user_id}"
        if cache_key in self._cache:
            del self._cache[cache_key]
        if cache_key in self._cache_timestamps:
            del self._cache_timestamps[cache_key]


class PermissionEvaluator:
    """Avaliador de permissões para uso em decorators/middleware"""
    
    def __init__(self, resolver: PermissionResolver):
        self.resolver = resolver
    
    def evaluate(self, user_id: str, required_permissions: List[str], 
                require_all: bool = False) -> bool:
        """
        Avalia se usuário tem as permissões necessárias
        """
        if not user_id:
            return False
        
        if require_all:
            return self.resolver.has_all_permissions(user_id, *required_permissions)
        else:
            return self.resolver.has_any_permission(user_id, *required_permissions)
    
    def get_missing_permissions(self, user_id: str, required_permissions: List[str]) -> List[str]:
        """Retorna lista de permissões faltantes"""
        missing = []
        for perm_code in required_permissions:
            if not self.resolver.has_any_permission(user_id, perm_code):
                missing.append(perm_code)
        
        return missing


# Decorator para uso em rotas (será implementado no middleware)
def requires_permissions(*permissions, require_all: bool = False):
    """Decorator para verificar permissões"""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            # A implementação será feita no middleware com acesso ao request.user
            return await func(*args, **kwargs)
        return wrapper
    return decorator
