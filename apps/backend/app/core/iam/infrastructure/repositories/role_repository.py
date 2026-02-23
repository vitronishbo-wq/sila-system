from typing import Optional, List, Tuple
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from datetime import datetime

from ..models.role_model import RoleModel, RolePermissionModel
from ..models.user_model import UserRoleModel
from .base_repository import BaseRepository


class RoleRepository(BaseRepository[RoleModel]):
    """Implementação do repositório de roles"""
    
    def __init__(self, db: Session):
        super().__init__(db, RoleModel)
    
    def save(self, role_data: dict) -> RoleModel:
        """Salva ou atualiza uma role"""
        existing = self.get_by_id(role_data.get("id"))
        if existing:
            # Atualiza
            for key, value in role_data.items():
                if value is not None and hasattr(existing, key):
                    setattr(existing, key, value)
            
            existing.updated_at = datetime.utcnow()
            self.db.flush()
            return existing
        else:
            # Cria novo
            return self.create(**role_data)
    
    def get_by_id(self, role_id: str) -> Optional[RoleModel]:
        """Busca role por ID"""
        return self.db.query(RoleModel).options(
            joinedload(RoleModel.permissions).joinedload(RolePermissionModel.permission)
        ).filter(
            RoleModel.id == role_id,
            RoleModel.is_active == True
        ).first()
    
    def get_by_name(self, name: str) -> Optional[RoleModel]:
        """Busca role por nome"""
        return self.db.query(RoleModel).options(
            joinedload(RoleModel.permissions).joinedload(RolePermissionModel.permission)
        ).filter(
            func.lower(RoleModel.name) == name.lower(),
            RoleModel.is_active == True
        ).first()
    
    def get_all(self, skip: int = 0, limit: int = 100, 
                include_system: bool = True) -> Tuple[List[RoleModel], int]:
        """Lista roles com paginação"""
        query = self.db.query(RoleModel).filter(RoleModel.is_active == True)
        
        if not include_system:
            query = query.filter(RoleModel.is_system == False)
        
        total = query.count()
        
        models = query.options(
            joinedload(RoleModel.permissions).joinedload(RolePermissionModel.permission)
        ).order_by(
            RoleModel.created_at.desc()
        ).offset(skip).limit(limit).all()
        
        return models, total
    
    def get_by_user(self, user_id: str) -> List[RoleModel]:
        """Busca roles de um usuário"""
        return self.db.query(RoleModel).join(
            UserRoleModel, RoleModel.id == UserRoleModel.role_id
        ).filter(
            UserRoleModel.user_id == user_id,
            RoleModel.is_active == True
        ).all()
    
    def assign_to_user(self, role_id: str, user_id: str, assigned_by: str) -> bool:
        """Atribui role a um usuário"""
        # Verifica se já existe
        existing = self.db.query(UserRoleModel).filter(
            UserRoleModel.user_id == user_id,
            UserRoleModel.role_id == role_id
        ).first()
        
        if existing:
            return True
        
        user_role = UserRoleModel(
            user_id=user_id,
            role_id=role_id,
            assigned_by=assigned_by
        )
        self.db.add(user_role)
        self.db.flush()
        return True
    
    def remove_from_user(self, role_id: str, user_id: str) -> bool:
        """Remove role de um usuário"""
        self.db.query(UserRoleModel).filter(
            UserRoleModel.user_id == user_id,
            UserRoleModel.role_id == role_id
        ).delete()
        self.db.flush()
        return True
    
    def delete(self, role_id: str) -> bool:
        """Remove role (apenas se não for system)"""
        model = super().get_by_id(role_id)
        if model and not model.is_system:
            return super().delete(role_id)
        return False
    
    def exists_by_name(self, name: str) -> bool:
        """Verifica se role já existe por nome"""
        return self.db.query(RoleModel).filter(
            func.lower(RoleModel.name) == name.lower()
        ).first() is not None
    
    def get_system_roles(self) -> List[RoleModel]:
        """Retorna roles do sistema"""
        return self.db.query(RoleModel).filter(
            RoleModel.is_system == True,
            RoleModel.is_active == True
        ).all()
