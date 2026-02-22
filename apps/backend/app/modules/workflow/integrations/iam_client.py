from typing import Dict, Any, Optional
from uuid import UUID


class IAMClient:
    """Cliente para integração com IAM"""
    
    def get_user(self, user_id: UUID) -> Dict[str, Any]:
        """
        Busca informações do usuário no IAM
        Mock para desenvolvimento
        """
        # Em produção, chamaria a API do IAM
        return {
            "id": str(user_id),
            "roles": ["OPERATOR", "MANAGER"] if "prov" in str(user_id) else ["CITIZEN"],
            "permissions": ["workflow:view", "workflow:execute"]
        }
    
    def has_permission(self, user_id: UUID, permission: str) -> bool:
        """Verifica se usuário tem permissão"""
        user = self.get_user(user_id)
        return permission in user.get('permissions', [])
    
    def has_role(self, user_id: UUID, role: str) -> bool:
        """Verifica se usuário tem role"""
        user = self.get_user(user_id)
        return role in user.get('roles', [])
