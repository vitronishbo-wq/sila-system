"""Serviço de autenticação para cidadãos"""
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from datetime import datetime
import logging
from uuid import UUID

from ...domain.models.user import User
from ...domain.enums.user_status import UserStatus
from .base_service import BaseService, AuthenticationError, ValidationError, NotFoundError
from ...infrastructure.security.password_hasher import Argon2PasswordHasher
from ...infrastructure.repositories.user_repository import UserRepository
from ...domain.value_objects.email import Email


class CitizenAuthService(BaseService):
    """Serviço de autenticação específico para cidadãos"""
    
    def __init__(self, db: Session):
        super().__init__(db)
        self.logger = logging.getLogger(__name__)
    
    def citizen_login(self, identifier: str, password: str, 
                      ip_address: Optional[str] = None,
                      user_agent: Optional[str] = None,
                      mfa_code: Optional[str] = None) -> Dict[str, Any]:
        """
        Login específico para cidadãos
        identifier pode ser: BI, NIF, Email, Citizen ID, ou Username
        """
        try:
            # PASSO 1: Resolver identificador e encontrar conta IAM
            user_model = self.user_repo.get_by_identifier(identifier)
            
            if not user_model:
                self._log_failed_login(identifier, ip_address, "user_not_found")
                raise AuthenticationError("Credenciais inválidas")
            
            # PASSO 2: Verificar status da conta
            self._check_user_status(user_model)
            
            # PASSO 3: Verificar senha
            if not self.hasher.verify(password, user_model.password_hash):
                self.user_repo.increment_failed_attempts(user_model.id)
                self._log_failed_login(identifier, ip_address, "invalid_password", user_model.id)
                raise AuthenticationError("Credenciais inválidas")
            
            # PASSO 4: Verificar MFA se habilitado
            if user_model.mfa_enabled:
                if not mfa_code:
                    return {
                        "requires_mfa": True,
                        "user_id": user_model.id,
                        "mfa_type": user_model.mfa_type
                    }
                
                if not self._verify_mfa(user_model, mfa_code):
                    self._log_failed_login(identifier, ip_address, "invalid_mfa", user_model.id)
                    raise AuthenticationError("Código MFA inválido")
            
            # PASSO 5: Registrar login bem-sucedido
            self.user_repo.update_last_login(user_model.id, ip_address)
            
            # PASSO 6: Criar tokens
            tokens = self._create_tokens(user_model)
            
            # PASSO 7: Registrar auditoria
            self._log_successful_login(user_model, ip_address, user_agent)
            
            # PASSO 8: Retornar resposta
            return self._build_login_response(user_model, tokens)
            
        except AuthenticationError:
            raise
        except Exception as e:
            self.logger.error(f"Erro no login do cidadão: {str(e)}", exc_info=True)
            raise AuthenticationError("Erro durante a autenticação")
    
    def register_citizen_account(self, citizen_id: str, email: str, 
                                  password: str, full_name: str,
                                  phone: Optional[str] = None) -> Dict[str, Any]:
        """
        Cria conta IAM para um cidadão existente no FUC
        """
        try:
            # Validar email único
            try:
                email_obj = Email(email)
            except Exception as e:
                raise ValidationError(f"Email inválido: {str(e)}")
            
            if self.user_repo.exists_by_email(email):
                raise ValidationError("Email já utilizado", field="email")
            
            # Validar citizen_id é UUID válido
            try:
                citizen_uuid = UUID(citizen_id)
            except Exception:
                raise ValidationError("ID do cidadão inválido", field="citizen_id")
            
            if self.user_repo.exists_by_citizen_id(citizen_uuid):
                raise ValidationError("Cidadão já possui conta")
            
            # Criar usuário
            username = email.split('@')[0]
            
            # Verificar username único
            if self.user_repo.exists_by_username(username):
                username = f"{username}_{citizen_uuid.hex[:6]}"
            
            user_model = self.user_repo.create(
                username=username,
                email=str(email_obj),
                password_hash=self.hasher.hash(password),
                citizen_id=citizen_uuid,
                full_name=full_name,
                phone=phone,
                status="ACTIVE",
                is_superuser=False,
                mfa_enabled=False
            )
            self.db.flush()
            
            # Adicionar role de cidadão se existir
            citizen_role = self.role_repo.get_by_name("CITIZEN")
            if citizen_role:
                from ...infrastructure.models.user_model import UserRoleModel
                user_role = UserRoleModel(
                    user_id=user_model.id,
                    role_id=citizen_role.id
                )
                self.db.add(user_role)
                self.db.flush()
            
            self.db.commit()
            
            # Registrar auditoria
            self._log_action(
                action="CITIZEN_ACCOUNT_CREATED",
                user_id=user_model.id,
                resource="user",
                resource_id=user_model.id
            )
            
            return {
                "user_id": user_model.id,
                "username": user_model.username,
                "email": user_model.email,
                "citizen_id": str(user_model.citizen_id)
            }
            
        except (ValidationError, AuthenticationError):
            raise
        except Exception as e:
            self.logger.error(f"Erro ao criar conta de cidadão: {str(e)}", exc_info=True)
            raise ValidationError(f"Erro ao criar conta: {str(e)}")
    
    def link_citizen_to_user(self, user_id: str, citizen_id: str, 
                             linked_by: str) -> Dict[str, Any]:
        """
        Vincula um usuário existente a um cidadão do FUC
        Útil para funcionários que também são cidadãos
        """
        try:
            # Validar citizen_id é UUID válido
            try:
                citizen_uuid = UUID(citizen_id)
            except Exception:
                raise ValidationError("ID do cidadão inválido", field="citizen_id")
            
            # Validar se já está vinculado a outro usuário
            existing = self.user_repo.get_by_citizen_id(citizen_uuid)
            if existing and existing.id != user_id:
                raise ValidationError("Cidadão já vinculado a outra conta")
            
            # Vincular
            user_model = self.user_repo.link_to_citizen(user_id, citizen_uuid)
            if not user_model:
                raise NotFoundError("User", user_id)
            
            self.db.commit()
            
            # Registrar auditoria
            self._log_action(
                action="CITIZEN_LINKED",
                user_id=linked_by,
                resource="user",
                resource_id=user_id
            )
            
            return {
                "user_id": user_model.id,
                "citizen_id": str(user_model.citizen_id)
            }
            
        except (ValidationError, NotFoundError):
            raise
        except Exception as e:
            self.logger.error(f"Erro ao vincular cidadão: {str(e)}", exc_info=True)
            raise ValidationError(f"Erro ao vincular cidadão: {str(e)}")
    
    def get_citizen_profile(self, user_id: str) -> Dict[str, Any]:
        """
        Obtém perfil completo do cidadão (IAM)
        """
        user_model = self.user_repo.get_by_id(user_id)
        if not user_model:
            raise NotFoundError("User", user_id)
        
        if not user_model.citizen_id:
            raise ValidationError("Usuário não é um cidadão")
        
        return {
            "user_id": user_model.id,
            "username": user_model.username,
            "email": user_model.email,
            "citizen_id": str(user_model.citizen_id),
            "full_name": user_model.full_name,
            "phone": user_model.phone,
            "status": user_model.status,
            "is_active": user_model.is_active,
            "mfa_enabled": user_model.mfa_enabled,
            "created_at": user_model.created_at.isoformat() if user_model.created_at else None
        }
    
    def _check_user_status(self, user_model):
        """Verifica status do usuário"""
        if user_model.status == "BLOCKED":
            raise AuthenticationError("Conta bloqueada. Contacte o administrador.")
        
        if user_model.status == "INACTIVE":
            raise AuthenticationError("Conta inativa")
        
        if user_model.status == "LOCKED":
            raise AuthenticationError("Conta temporariamente bloqueada. Tente mais tarde.")
    
    def _verify_mfa(self, user_model, code: str) -> bool:
        """Verifica código MFA"""
        if user_model.mfa_type == "TOTP" and user_model.mfa_secret:
            try:
                import pyotp
                totp = pyotp.TOTP(user_model.mfa_secret)
                return totp.verify(code)
            except Exception as e:
                self.logger.error(f"Erro ao verificar TOTP: {str(e)}")
                return False
        return False
    
    def _create_tokens(self, user_model) -> Dict[str, str]:
        """Cria tokens JWT"""
        roles = [r.role.name for r in user_model.roles if r.role]
        permissions = []  # Será derivado das roles no validate
        
        access_token = self.jwt_provider.create_access_token(
            user_id=user_model.id,
            roles=roles,
            permissions=permissions
        )
        
        refresh_token = self.jwt_provider.create_refresh_token(user_model.id)
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        }
    
    def _build_login_response(self, user_model, tokens: Dict[str, str]) -> Dict[str, Any]:
        """Constrói resposta de login"""
        roles = [r.role.name for r in user_model.roles if r.role]
        
        response = {
            "access_token": tokens["access_token"],
            "refresh_token": tokens["refresh_token"],
            "token_type": "Bearer",
            "expires_in": 3600 * 24,  # 24 horas
            "user": {
                "id": user_model.id,
                "username": user_model.username,
                "email": user_model.email,
                "full_name": user_model.full_name,
                "citizen_id": str(user_model.citizen_id) if user_model.citizen_id else None,
                "is_citizen": user_model.citizen_id is not None,
                "roles": roles,
                "mfa_enabled": user_model.mfa_enabled
            }
        }
        
        return response
    
    def _log_failed_login(self, identifier: str, ip: Optional[str], 
                          reason: str, user_id: Optional[str] = None):
        """Regista tentativa de login falha"""
        self._log_action(
            action="LOGIN_FAILED",
            user_id=user_id or "UNKNOWN",
            resource="auth",
            resource_id="citizen_login",
            success=False,
            error=reason,
            details={
                "identifier": identifier[:20],  # Para não expor dados
                "ip": ip,
                "reason": reason
            }
        )
    
    def _log_successful_login(self, user_model, ip: Optional[str], 
                              agent: Optional[str]):
        """Regista login bem-sucedido"""
        self._log_action(
            action="LOGIN_SUCCESS",
            user_id=user_model.id,
            resource="auth",
            resource_id="citizen_login",
            success=True,
            details={
                "ip": ip,
                "user_agent": agent[:100] if agent else None,
                "citizen_id": str(user_model.citizen_id) if user_model.citizen_id else None
            }
        )
