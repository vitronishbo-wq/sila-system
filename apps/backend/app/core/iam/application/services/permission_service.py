from typing import Optional, List, Dict, Any, Tuple
from sqlalchemy.orm import Session
from datetime import datetime

from .base_service import BaseService, ValidationError, NotFoundError


class PermissionService(BaseService):
    """Serviço de gestão de permissões"""
    
    def __init__(self, db: Session):
        super().__init__(db)
    
    def create_permission(self, permission_data: Dict[str, Any], created_by: str):
        """
        Cria uma nova permissão
        """
        try:
            # Valida dados
            required = ["resource", "action"]
            for field in required:
                if field not in permission_data:
                    raise ValidationError(f"Campo obrigatório: {field}", field=field)
            
            resource = permission_data["resource"].upper()
            action = permission_data["action"].upper()
            
            # Gera código
            code = f"{resource}:{action}"
            
            # Cria permissão via repositório
            from ...infrastructure.models.permission_model import PermissionModel
            permission = PermissionModel(
                resource=resource,
                action=action,
                description=permission_data.get("description"),
                is_system=permission_data.get("is_system", False),
                created_by=created_by
            )
            
            self.db.add(permission)
            self.db.commit()
            self.db.refresh(permission)
            
            self._log_action(
                action="CREATE",
                user_id=created_by,
                resource="PERMISSION",
                resource_id=permission.id,
                details={"code": code},
                success=True
            )
            
            return permission
            
        except Exception as e:
            self.db.rollback()
            self._handle_error(e, {"permission_data": permission_data})
    
    def get_permission(self, permission_id: str):
        """
        Busca permissão por ID
        """
        permission = self.permission_repo.get_by_id(permission_id)
        if not permission:
            raise NotFoundError("Permission", permission_id)
        return permission
    
    def get_permission_by_code(self, code: str):
        """
        Busca permissão por código
        """
        return self.permission_repo.get_by_code(code)
    
    def list_permissions(self, skip: int = 0, limit: int = 100) -> Tuple[List, int]:
        """
        Lista permissões com paginação
        """
        return self.permission_repo.get_all(skip, limit)
    
    def list_by_resource(self, resource: str) -> List:
        """
        Lista permissões por recurso
        """
        return self.permission_repo.get_by_resource(resource)
    
    def update_permission(self, permission_id: str, permission_data: Dict[str, Any], 
                         updated_by: str):
        """
        Atualiza uma permissão
        """
        try:
            permission = self.permission_repo.get_by_id(permission_id)
            if not permission:
                raise NotFoundError("Permission", permission_id)
            
            # Não permite alterar permissões do sistema
            if permission.is_system:
                raise ValidationError("Não é possível alterar permissões do sistema")
            
            # Atualiza campos permitidos
            if "description" in permission_data:
                permission.description = permission_data["description"]
            
            self.db.commit()
            self.db.refresh(permission)
            
            self._log_action(
                action="UPDATE",
                user_id=updated_by,
                resource="PERMISSION",
                resource_id=permission_id,
                details=permission_data,
                success=True
            )
            
            return permission
            
        except Exception as e:
            self.db.rollback()
            self._handle_error(e, {"permission_id": permission_id, "permission_data": permission_data})
    
    def delete_permission(self, permission_id: str, deleted_by: str) -> bool:
        """
        Remove uma permissão
        """
        try:
            permission = self.permission_repo.get_by_id(permission_id)
            if not permission:
                raise NotFoundError("Permission", permission_id)
            
            # Não permite deletar permissões do sistema
            if permission.is_system:
                raise ValidationError("Não é possível deletar permissões do sistema")
            
            result = self.permission_repo.delete(permission_id)
            
            if result:
                self._log_action(
                    action="DELETE",
                    user_id=deleted_by,
                    resource="PERMISSION",
                    resource_id=permission_id,
                    success=True
                )
            
            return result
            
        except Exception as e:
            self.db.rollback()
            self._handle_error(e, {"permission_id": permission_id})
    
    def get_user_permissions(self, user_id: str) -> List[str]:
        """
        Retorna lista de códigos de permissão de um usuário
        """
        permissions = self.permission_repo.get_by_user(user_id)
        return [f"{p.resource}:{p.action}" for p in permissions]
    
    def assign_to_user_direct(self, user_id: str, permission_id: str, 
                             granted_by: str, expires_at: Optional[datetime] = None) -> bool:
        """
        Atribui permissão diretamente a um usuário
        """
        try:
            result = self.permission_repo.assign_to_user_direct(
                permission_id, user_id, granted_by, expires_at
            )
            
            if result:
                # Invalida cache
                self._init_permission_resolver()
                self.permission_resolver.invalidate_cache(user_id)
                
                permission = self.permission_repo.get_by_id(permission_id)
                self._log_action(
                    action="ASSIGN",
                    user_id=granted_by,
                    resource="PERMISSION",
                    resource_id=permission_id,
                    details={"user_id": user_id},
                    success=True
                )
            
            return result
            
        except Exception as e:
            self.db.rollback()
            self._handle_error(e, {"user_id": user_id, "permission_id": permission_id})
    
    def remove_from_user_direct(self, user_id: str, permission_id: str, removed_by: str) -> bool:
        """
        Remove permissão direta de um usuário
        """
        try:
            result = self.permission_repo.remove_from_user_direct(permission_id, user_id)
            
            if result:
                # Invalida cache
                self._init_permission_resolver()
                self.permission_resolver.invalidate_cache(user_id)
                
                self._log_action(
                    action="REVOKE",
                    user_id=removed_by,
                    resource="PERMISSION",
                    resource_id=permission_id,
                    details={"user_id": user_id},
                    success=True
                )
            
            return result
            
        except Exception as e:
            self.db.rollback()
            self._handle_error(e, {"user_id": user_id, "permission_id": permission_id})
