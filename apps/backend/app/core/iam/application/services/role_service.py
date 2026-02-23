from typing import List, Dict, Any, Tuple
from sqlalchemy.orm import Session
from datetime import datetime

from .base_service import BaseService, ValidationError, NotFoundError, ConflictError


class RoleService(BaseService):
    """Serviço de gestão de roles"""
    
    def __init__(self, db: Session):
        super().__init__(db)
    
    def create_role(self, role_data: Dict[str, Any], created_by: str):
        """
        Cria uma nova role
        """
        try:
            # Valida dados
            if not role_data.get("name"):
                raise ValidationError("Nome da role é obrigatório", field="name")
            
            name = role_data["name"].upper().strip()
            
            # Verifica duplicidade
            if self.role_repo.exists_by_name(name):
                raise ConflictError("Role já existe", field="name")
            
            # Cria role via repositório
            from ...infrastructure.models.role_model import RoleModel
            role = RoleModel(
                name=name,
                description=role_data.get("description"),
                is_system=role_data.get("is_system", False),
                created_by=created_by
            )
            
            self.db.add(role)
            self.db.commit()
            self.db.refresh(role)
            
            self._log_action(
                action="CREATE",
                user_id=created_by,
                resource="ROLE",
                resource_id=role.id,
                details={"name": role.name},
                success=True
            )
            
            return role
            
        except Exception as e:
            self.db.rollback()
            self._handle_error(e, {"role_data": role_data})
    
    def get_role(self, role_id: str):
        """
        Busca role por ID
        """
        role = self.role_repo.get_by_id(role_id)
        if not role:
            raise NotFoundError("Role", role_id)
        return role
    
    def get_role_by_name(self, name: str):
        """
        Busca role por nome
        """
        return self.role_repo.get_by_name(name)
    
    def list_roles(self, skip: int = 0, limit: int = 100, 
                   include_system: bool = True) -> Tuple[List, int]:
        """
        Lista roles com paginação
        """
        return self.role_repo.get_all(skip, limit, include_system)
    
    def update_role(self, role_id: str, role_data: Dict[str, Any], 
                   updated_by: str):
        """
        Atualiza uma role
        """
        try:
            role = self.role_repo.get_by_id(role_id)
            if not role:
                raise NotFoundError("Role", role_id)
            
            # Não permite alterar roles do sistema
            if role.is_system:
                raise ValidationError("Não é possível alterar roles do sistema")
            
            # Atualiza campos
            if "name" in role_data:
                new_name = role_data["name"].upper().strip()
                if new_name != role.name and self.role_repo.exists_by_name(new_name):
                    raise ConflictError("Nome da role já existe", field="name")
                role.name = new_name
            
            if "description" in role_data:
                role.description = role_data["description"]
            
            role.updated_by = updated_by
            role.updated_at = datetime.now()
            
            self.db.commit()
            self.db.refresh(role)
            
            self._log_action(
                action="UPDATE",
                user_id=updated_by,
                resource="ROLE",
                resource_id=role_id,
                details=role_data,
                success=True
            )
            
            return role
            
        except Exception as e:
            self.db.rollback()
            self._handle_error(e, {"role_id": role_id, "role_data": role_data})
    
    def delete_role(self, role_id: str, deleted_by: str) -> bool:
        """
        Remove uma role
        """
        try:
            role = self.role_repo.get_by_id(role_id)
            if not role:
                raise NotFoundError("Role", role_id)
            
            # Não permite deletar roles do sistema
            if role.is_system:
                raise ValidationError("Não é possível deletar roles do sistema")
            
            result = self.role_repo.delete(role_id)
            
            if result:
                self._log_action(
                    action="DELETE",
                    user_id=deleted_by,
                    resource="ROLE",
                    resource_id=role_id,
                    success=True
                )
            
            return result
            
        except Exception as e:
            self.db.rollback()
            self._handle_error(e, {"role_id": role_id})
    
    def assign_permissions(self, role_id: str, permission_ids: List[str], 
                          assigned_by: str):
        """
        Atribui permissões a uma role
        """
        try:
            role = self.role_repo.get_by_id(role_id)
            if not role:
                raise NotFoundError("Role", role_id)
            
            permissions_added = []
            for perm_id in permission_ids:
                result = self.permission_repo.assign_to_role(role_id, perm_id)
                if result:
                    permissions_added.append(perm_id)
            
            # Invalida cache de permissões
            self._init_permission_resolver()
            
            self._log_action(
                action="ASSIGN",
                user_id=assigned_by,
                resource="ROLE",
                resource_id=role_id,
                details={"permissions_added": permissions_added},
                success=True
            )
            
            return role
            
        except Exception as e:
            self.db.rollback()
            self._handle_error(e, {"role_id": role_id, "permission_ids": permission_ids})
    
    def remove_permissions(self, role_id: str, permission_ids: List[str], 
                          removed_by: str):
        """
        Remove permissões de uma role
        """
        try:
            role = self.role_repo.get_by_id(role_id)
            if not role:
                raise NotFoundError("Role", role_id)
            
            permissions_removed = []
            for perm_id in permission_ids:
                result = self.permission_repo.remove_from_role(role_id, perm_id)
                if result:
                    permissions_removed.append(perm_id)
            
            # Invalida cache de permissões
            self._init_permission_resolver()
            
            self._log_action(
                action="REVOKE",
                user_id=removed_by,
                resource="ROLE",
                resource_id=role_id,
                details={"permissions_removed": permissions_removed},
                success=True
            )
            
            return role
            
        except Exception as e:
            self.db.rollback()
            self._handle_error(e, {"role_id": role_id, "permission_ids": permission_ids})
