from typing import Optional, List, Tuple
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from datetime import datetime
from uuid import UUID

from ..models.user_model import UserModel, UserRoleModel
from ..models.permission_model import UserPermissionModel
from .base_repository import BaseRepository


class UserRepository(BaseRepository[UserModel]):
    """Implementação do repositório de usuários"""
    
    def __init__(self, db: Session):
        super().__init__(db, UserModel)
    
    def save(self, user_data: dict) -> UserModel:
        """Salva ou atualiza um usuário"""
        # Verifica se já existe
        existing = self.get_by_id(user_data.get("id"))
        if existing:
            # Atualiza
            for key, value in user_data.items():
                if value is not None and hasattr(existing, key):
                    setattr(existing, key, value)
            
            existing.updated_at = datetime.utcnow()
            self.db.flush()
            return existing
        else:
            # Cria novo
            return self.create(**user_data)
    
    def get_by_id(self, user_id: str) -> Optional[UserModel]:
        """Busca usuário por ID"""
        return self.db.query(UserModel).options(
            joinedload(UserModel.roles).joinedload(UserRoleModel.role),
            joinedload(UserModel.permissions_direct).joinedload(UserPermissionModel.permission)
        ).filter(
            UserModel.id == user_id,
            UserModel.is_active == True
        ).first()
    
    def get_by_username(self, username: str) -> Optional[UserModel]:
        """Busca usuário por username"""
        return self.db.query(UserModel).options(
            joinedload(UserModel.roles).joinedload(UserRoleModel.role),
            joinedload(UserModel.permissions_direct).joinedload(UserPermissionModel.permission)
        ).filter(
            func.lower(UserModel.username) == username.lower(),
            UserModel.is_active == True
        ).first()
    
    def get_by_email(self, email: str) -> Optional[UserModel]:
        """Busca usuário por email"""
        return self.db.query(UserModel).options(
            joinedload(UserModel.roles).joinedload(UserRoleModel.role),
            joinedload(UserModel.permissions_direct).joinedload(UserPermissionModel.permission)
        ).filter(
            func.lower(UserModel.email) == email.lower(),
            UserModel.is_active == True
        ).first()
    
    def get_all(self, skip: int = 0, limit: int = 100, 
                include_inactive: bool = False) -> Tuple[List[UserModel], int]:
        """Lista usuários com paginação"""
        query = self.db.query(UserModel)
        
        if not include_inactive:
            query = query.filter(UserModel.is_active == True)
        
        total = query.count()
        
        models = query.options(
            joinedload(UserModel.roles).joinedload(UserRoleModel.role)
        ).order_by(
            UserModel.created_at.desc()
        ).offset(skip).limit(limit).all()
        
        return models, total
    
    def get_by_role(self, role_id: str, skip: int = 0, limit: int = 100) -> List[UserModel]:
        """Busca usuários por role"""
        return self.db.query(UserModel).join(
            UserRoleModel, UserModel.id == UserRoleModel.user_id
        ).filter(
            UserRoleModel.role_id == role_id,
            UserModel.is_active == True
        ).offset(skip).limit(limit).all()
    
    def update_last_login(self, user_id: str, ip_address: Optional[str] = None) -> Optional[UserModel]:
        """Atualiza timestamp do último login"""
        model = super().get_by_id(user_id)
        if model:
            model.last_login_at = datetime.utcnow()
            model.last_login_ip = ip_address
            model.failed_login_attempts = 0
            model.updated_at = datetime.utcnow()
            self.db.flush()
            return model
        return None
    
    def increment_failed_attempts(self, user_id: str) -> Optional[UserModel]:
        """Incrementa contador de tentativas falhas"""
        model = super().get_by_id(user_id)
        if model:
            model.failed_login_attempts += 1
            model.updated_at = datetime.utcnow()
            
            # Auto-lock após 5 tentativas
            if model.failed_login_attempts >= 5:
                model.status = "LOCKED"
            
            self.db.flush()
            return model
        return None
    
    def reset_failed_attempts(self, user_id: str) -> Optional[UserModel]:
        """Reseta contador de tentativas falhas"""
        model = super().get_by_id(user_id)
        if model:
            model.failed_login_attempts = 0
            model.updated_at = datetime.utcnow()
            self.db.flush()
            return model
        return None
    
    def update_password(self, user_id: str, password_hash: str) -> Optional[UserModel]:
        """Atualiza senha do usuário"""
        model = super().get_by_id(user_id)
        if model:
            model.password_hash = password_hash
            model.password_changed_at = datetime.utcnow()
            model.failed_login_attempts = 0
            model.updated_at = datetime.utcnow()
            
            # Se estava bloqueado por tentativas, desbloqueia
            if model.status == "LOCKED":
                model.status = "ACTIVE"
            
            self.db.flush()
            return model
        return None
    
    def delete(self, user_id: str, soft_delete: bool = True) -> bool:
        """Remove usuário (soft delete por padrão)"""
        model = super().get_by_id(user_id)
        if model:
            if soft_delete:
                model.is_active = False
                model.deleted_at = datetime.utcnow()
                model.updated_at = datetime.utcnow()
                self.db.flush()
            else:
                self.db.delete(model)
                self.db.flush()
            return True
        return False
    
    def exists_by_username(self, username: str) -> bool:
        """Verifica se username já existe"""
        return self.db.query(UserModel).filter(
            func.lower(UserModel.username) == username.lower()
        ).first() is not None
    
    def exists_by_email(self, email: str) -> bool:
        """Verifica se email já existe"""
        return self.db.query(UserModel).filter(
            func.lower(UserModel.email) == email.lower()
        ).first() is not None
    
    def get_by_citizen_id(self, citizen_id: UUID) -> Optional[UserModel]:
        """Busca usuário por ID do cidadão FUC"""
        return self.db.query(UserModel).options(
            joinedload(UserModel.roles).joinedload(UserRoleModel.role),
            joinedload(UserModel.permissions_direct).joinedload(UserPermissionModel.permission)
        ).filter(
            UserModel.citizen_id == citizen_id,
            UserModel.is_active == True
        ).first()
    
    def get_by_identifier(self, identifier: str) -> Optional[UserModel]:
        """
        Busca usuário por qualquer identificador:
        - email
        - username
        - citizen_id (se for UUID)
        """
        # Tenta como email
        user = self.get_by_email(identifier)
        if user:
            return user
        
        # Tenta como username
        user = self.get_by_username(identifier)
        if user:
            return user
        
        # Tenta como UUID (citizen_id)
        try:
            citizen_id = UUID(identifier)
            user = self.get_by_citizen_id(citizen_id)
            if user:
                return user
        except:
            pass
        
        return None
    
    def link_to_citizen(self, user_id: str, citizen_id: UUID) -> Optional[UserModel]:
        """Vincula usuário a um cidadão do FUC"""
        model = super().get_by_id(user_id)
        if model:
            model.citizen_id = citizen_id
            model.updated_at = datetime.utcnow()
            self.db.flush()
            return model
        return None
    
    def unlink_from_citizen(self, user_id: str) -> Optional[UserModel]:
        """Desvincula usuário do cidadão"""
        model = super().get_by_id(user_id)
        if model:
            model.citizen_id = None
            model.updated_at = datetime.utcnow()
            self.db.flush()
            return model
        return None
    
    def exists_by_citizen_id(self, citizen_id: UUID) -> bool:
        """Verifica se já existe conta para este cidadão"""
        return self.db.query(UserModel).filter(
            UserModel.citizen_id == citizen_id,
            UserModel.is_active == True
        ).first() is not None
    
    def count_active(self) -> int:
        """Conta usuários ativos"""
        return self.db.query(UserModel).filter(
            UserModel.is_active == True,
            UserModel.status == "ACTIVE"
        ).count()
