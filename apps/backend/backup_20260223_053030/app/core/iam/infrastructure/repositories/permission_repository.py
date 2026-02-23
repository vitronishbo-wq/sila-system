from typing import Optional, List, Set, Tuple, Dict
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from datetime import datetime

from ..models.permission_model import PermissionModel, UserPermissionModel
from ..models.role_model import RolePermissionModel
from ..models.user_model import UserRoleModel
from .base_repository import BaseRepository


class PermissionRepository(BaseRepository[PermissionModel]):
    """Implementação do repositório de permissões"""
    
    def __init__(self, db: Session):
        super().__init__(db, PermissionModel)
    
    def save(self, permission_data: dict) -> PermissionModel:
        """Salva ou atualiza uma permissão"""
        existing = self.get_by_id(permission_data.get("id"))
        if existing:
            for key, value in permission_data.items():
                if value is not None and hasattr(existing, key):
                    setattr(existing, key, value)
            existing.updated_at = datetime.utcnow()
            self.db.flush()
            return existing
        else:
            return self.create(**permission_data)
    
    def get_by_id(self, permission_id: str) -> Optional[PermissionModel]:
        """Busca permissão por ID"""
        return super().get_by_id(permission_id)
    
    def get_by_code(self, code: str) -> Optional[PermissionModel]:
        """Busca permissão por código (resource:action)"""
        return self.db.query(PermissionModel).filter(
            PermissionModel.code == code,
            PermissionModel.is_active == True
        ).first()
    
    def get_all(self, skip: int = 0, limit: int = 100) -> Tuple[List[PermissionModel], int]:
        """Lista permissões com paginação"""
        query = self.db.query(PermissionModel).filter(PermissionModel.is_active == True)
        total = query.count()
        models = query.order_by(PermissionModel.module, PermissionModel.resource).offset(skip).limit(limit).all()
        return models, total
    
    def get_by_resource(self, resource: str) -> List[PermissionModel]:
        """Busca permissões por recurso"""
        return self.db.query(PermissionModel).filter(
            PermissionModel.resource == resource,
            PermissionModel.is_active == True
        ).all()
    
    def get_by_role(self, role_id: str) -> Set[PermissionModel]:
        """Busca permissões de uma role"""
        permissions = set()
        
        role_perms = self.db.query(PermissionModel).join(
            RolePermissionModel, PermissionModel.id == RolePermissionModel.permission_id
        ).filter(
            RolePermissionModel.role_id == role_id,
            PermissionModel.is_active == True
        ).all()
        
        for perm in role_perms:
            permissions.add(perm)
        
        return permissions
    
    def get_by_user(self, user_id: str) -> Set[PermissionModel]:
        """Busca todas as permissões de um usuário (via roles + diretas)"""
        permissions = set()
        
        # Permissões via roles
        role_perms = self.db.query(PermissionModel).join(
            RolePermissionModel, PermissionModel.id == RolePermissionModel.permission_id
        ).join(
            UserRoleModel, RolePermissionModel.role_id == UserRoleModel.role_id
        ).filter(
            UserRoleModel.user_id == user_id,
            PermissionModel.is_active == True
        ).distinct().all()
        
        for perm in role_perms:
            permissions.add(perm)
        
        # Permissões diretas
        direct_perms = self.db.query(PermissionModel).join(
            UserPermissionModel, PermissionModel.id == UserPermissionModel.permission_id
        ).filter(
            UserPermissionModel.user_id == user_id,
            PermissionModel.is_active == True,
            or_(
                UserPermissionModel.expires_at.is_(None),
                UserPermissionModel.expires_at > datetime.utcnow()
            )
        ).all()
        
        for perm in direct_perms:
            permissions.add(perm)
        
        return permissions
    
    def assign_to_role(self, permission_id: str, role_id: str) -> bool:
        """Atribui permissão a uma role"""
        existing = self.db.query(RolePermissionModel).filter(
            RolePermissionModel.role_id == role_id,
            RolePermissionModel.permission_id == permission_id
        ).first()
        
        if existing:
            return True
        
        role_perm = RolePermissionModel(
            role_id=role_id,
            permission_id=permission_id
        )
        self.db.add(role_perm)
        self.db.flush()
        return True
    
    def remove_from_role(self, permission_id: str, role_id: str) -> bool:
        """Remove permissão de uma role"""
        self.db.query(RolePermissionModel).filter(
            RolePermissionModel.role_id == role_id,
            RolePermissionModel.permission_id == permission_id
        ).delete()
        self.db.flush()
        return True
    
    def assign_to_user_direct(self, permission_id: str, user_id: str, 
                             granted_by: str = None, expires_at: datetime = None) -> bool:
        """Atribui permissão diretamente a um usuário"""
        existing = self.db.query(UserPermissionModel).filter(
            UserPermissionModel.user_id == user_id,
            UserPermissionModel.permission_id == permission_id
        ).first()
        
        if existing:
            return True
        
        user_perm = UserPermissionModel(
            user_id=user_id,
            permission_id=permission_id,
            granted_by=granted_by,
            expires_at=expires_at
        )
        self.db.add(user_perm)
        self.db.flush()
        return True
    
    def remove_from_user_direct(self, permission_id: str, user_id: str) -> bool:
        """Remove permissão direta de um usuário"""
        self.db.query(UserPermissionModel).filter(
            UserPermissionModel.user_id == user_id,
            UserPermissionModel.permission_id == permission_id
        ).delete()
        self.db.flush()
        return True
    
    def delete(self, permission_id: str) -> bool:
        """Remove permissão (apenas se não for system)"""
        model = super().get_by_id(permission_id)
        if model and not model.is_system:
            return super().delete(permission_id)
        return False
    
    def exists_by_code(self, code: str) -> bool:
        """Verifica se permissão já existe por código"""
        return self.db.query(PermissionModel).filter(
            PermissionModel.code == code
        ).first() is not None
    
    def get_user_permissions_map(self, user_id: str) -> dict:
        """Retorna mapa de permissões do usuário agrupado por recurso"""
        permissions = self.get_by_user(user_id)
        
        result = {}
        for perm in permissions:
            resource = perm.resource
            if resource not in result:
                result[resource] = []
            result[resource].append(perm.action)
        
        return result
