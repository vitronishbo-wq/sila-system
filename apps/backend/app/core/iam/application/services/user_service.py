from typing import List, Dict, Any, Tuple
from sqlalchemy.orm import Session
from datetime import datetime

from .base_service import BaseService, ValidationError, NotFoundError, ConflictError
from ...infrastructure.security.password_hasher import PasswordGenerator
from app.utils.security import validate_password_strength


class UserService(BaseService):
    """Serviço de gestão de usuários"""
    
    def __init__(self, db: Session):
        super().__init__(db)
    
    def create_user(self, user_data: Dict[str, Any], created_by: str):
        """
        Cria um novo usuário
        """
        try:
            # Valida dados
            self._validate_user_data(user_data)
            
            # Verifica duplicidade
            if self.user_repo.exists_by_username(user_data["username"]):
                raise ConflictError("Username já existe", field="username")
            
            # Gera senha se não fornecida
            if "password" not in user_data:
                password = PasswordGenerator.generate()
                user_data["password"] = password
                user_data["_temp_password"] = password  # Para retornar
            
            # Hash da senha
            password_hash = self.hasher.hash(user_data["password"])
            
            # Cria usuário via repositório
            from ...infrastructure.models.user_model import UserModel
            user = UserModel(
                username=user_data["username"],
                email=user_data["email"],
                password_hash=password_hash,
                full_name=user_data.get("full_name"),
                phone=user_data.get("phone"),
                department=user_data.get("department"),
                position=user_data.get("position"),
                status=user_data.get("status", "PENDING_VERIFICATION"),
                is_superuser=user_data.get("is_superuser", False),
                created_by=created_by
            )
            
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
            
            self._log_action(
                action="CREATE",
                user_id=created_by,
                resource="USER",
                resource_id=user.id,
                details={"username": user.username, "email": user.email},
                success=True
            )
            
            return user
            
        except Exception as e:
            self.db.rollback()
            self._handle_error(e, {"user_data": user_data})
    
    def get_user(self, user_id: str, requesting_user_id: str):
        """
        Busca usuário por ID
        """
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise NotFoundError("User", user_id)
        
        self._log_action(
            action="VIEW",
            user_id=requesting_user_id,
            resource="USER",
            resource_id=user_id,
            success=True
        )
        
        return user
    
    def get_user_by_username(self, username: str):
        """
        Busca usuário por username
        """
        return self.user_repo.get_by_username(username)
    
    def list_users(self, skip: int = 0, limit: int = 100, 
                   include_inactive: bool = False) -> Tuple[List, int]:
        """
        Lista usuários com paginação
        """
        return self.user_repo.get_all(skip, limit, include_inactive)
    
    def update_user(self, user_id: str, user_data: Dict[str, Any], 
                   updated_by: str):
        """
        Atualiza dados de um usuário
        """
        try:
            user = self.user_repo.get_by_id(user_id)
            if not user:
                raise NotFoundError("User", user_id)
            
            # Atualiza campos
            if "full_name" in user_data:
                user.full_name = user_data["full_name"]
            if "phone" in user_data:
                user.phone = user_data["phone"]
            if "department" in user_data:
                user.department = user_data["department"]
            if "position" in user_data:
                user.position = user_data["position"]
            if "status" in user_data:
                user.status = user_data["status"]
            
            user.updated_by = updated_by
            user.updated_at = datetime.now()
            
            self.db.commit()
            self.db.refresh(user)
            
            self._log_action(
                action="UPDATE",
                user_id=updated_by,
                resource="USER",
                resource_id=user_id,
                details={k: v for k, v in user_data.items() if k not in ["password"]},
                success=True
            )
            
            return user
            
        except Exception as e:
            self.db.rollback()
            self._handle_error(e, {"user_id": user_id, "user_data": user_data})
    
    def delete_user(self, user_id: str, deleted_by: str, soft_delete: bool = True) -> bool:
        """
        Remove um usuário
        """
        try:
            user = self.user_repo.get_by_id(user_id)
            if not user:
                raise NotFoundError("User", user_id)
            
            result = self.user_repo.delete(user_id, soft_delete)
            
            if result:
                self._log_action(
                    action="DELETE",
                    user_id=deleted_by,
                    resource="USER",
                    resource_id=user_id,
                    details={"soft_delete": soft_delete},
                    success=True
                )
            
            return result
            
        except Exception as e:
            self.db.rollback()
            self._handle_error(e, {"user_id": user_id})
    
    def assign_roles(self, user_id: str, role_ids: List[str], assigned_by: str):
        """
        Atribui roles a um usuário
        """
        try:
            user = self.user_repo.get_by_id(user_id)
            if not user:
                raise NotFoundError("User", user_id)
            
            roles_added = []
            for role_id in role_ids:
                result = self.role_repo.assign_to_user(user_id, role_id)
                if result:
                    roles_added.append(role_id)
            
            self._log_action(
                action="ASSIGN",
                user_id=assigned_by,
                resource="USER",
                resource_id=user_id,
                details={"roles_added": roles_added},
                success=True
            )
            
            return user
            
        except Exception as e:
            self.db.rollback()
            self._handle_error(e, {"user_id": user_id, "role_ids": role_ids})
    
    def remove_roles(self, user_id: str, role_ids: List[str], removed_by: str):
        """
        Remove roles de um usuário
        """
        try:
            user = self.user_repo.get_by_id(user_id)
            if not user:
                raise NotFoundError("User", user_id)
            
            roles_removed = []
            for role_id in role_ids:
                result = self.role_repo.remove_from_user(user_id, role_id)
                if result:
                    roles_removed.append(role_id)
            
            self._log_action(
                action="REVOKE",
                user_id=removed_by,
                resource="USER",
                resource_id=user_id,
                details={"roles_removed": roles_removed},
                success=True
            )
            
            return user
            
        except Exception as e:
            self.db.rollback()
            self._handle_error(e, {"user_id": user_id, "role_ids": role_ids})
    
    def activate_user(self, user_id: str, activated_by: str):
        """
        Ativa um usuário
        """
        return self._change_user_status(user_id, "ACTIVE", activated_by)
    
    def deactivate_user(self, user_id: str, deactivated_by: str):
        """
        Desativa um usuário
        """
        return self._change_user_status(user_id, "INACTIVE", deactivated_by)
    
    def block_user(self, user_id: str, blocked_by: str):
        """
        Bloqueia um usuário
        """
        return self._change_user_status(user_id, "BLOCKED", blocked_by)
    
    def unlock_user(self, user_id: str, unlocked_by: str):
        """
        Desbloqueia um usuário
        """
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise NotFoundError("User", user_id)
        
        user.failed_login_attempts = 0
        user.updated_by = unlocked_by
        
        self.db.commit()
        self.db.refresh(user)
        
        self._log_action(
            action="UNLOCK",
            user_id=unlocked_by,
            resource="USER",
            resource_id=user_id,
            success=True
        )
        
        return user
    
    def _change_user_status(self, user_id: str, status: str, changed_by: str):
        """Altera status do usuário"""
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise NotFoundError("User", user_id)
        
        old_status = user.status
        user.status = status
        user.updated_by = changed_by
        user.updated_at = datetime.now()
        
        self.db.commit()
        self.db.refresh(user)
        
        self._log_action(
            action="STATUS_CHANGE",
            user_id=changed_by,
            resource="USER",
            resource_id=user_id,
            details={"old_status": old_status, "new_status": status},
            success=True
        )
        
        return user
    
    def _validate_user_data(self, data: Dict[str, Any]):
        """Valida dados do usuário"""
        required = ["username", "email"]
        for field in required:
            if field not in data:
                raise ValidationError(f"Campo obrigatório: {field}", field=field)
        
        if len(data["username"]) < 3:
            raise ValidationError("Username deve ter pelo menos 3 caracteres", field="username")
        
        if "password" in data:
            is_strong, strength, messages, score = validate_password_strength(data["password"])
            if not is_strong:
                raise ValidationError(
                    "Senha fraca",
                    field="password",
                    details={"messages": messages, "strength": strength, "score": score}
                )
