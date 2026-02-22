from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from .base_service import (
    BaseService, 
    AuthenticationError, 
    ValidationError, 
    NotFoundError
)
from ...infrastructure.security.mfa import MFAProvider, EmailMFAProvider
from app.utils.security import validate_password_strength


class AuthService(BaseService):
    """Serviço de autenticação"""
    
    def __init__(self, db: Session):
        super().__init__(db)
        self.mfa_provider = MFAProvider()
        self.email_mfa = EmailMFAProvider()
    
    def login(self, username: str, password: str, ip_address: Optional[str] = None,
              user_agent: Optional[str] = None, mfa_code: Optional[str] = None) -> Dict[str, Any]:
        """
        Autentica um usuário
        """
        try:
            # Busca usuário por username ou email
            user = self.user_repo.get_by_username(username)
            if not user:
                user = self.user_repo.get_by_email(username)
            
            if not user:
                self._log_action(
                    action="LOGIN_FAILED",
                    user_id="unknown",
                    resource="SESSION",
                    details={"username": username, "reason": "user_not_found"},
                    success=False
                )
                raise AuthenticationError("Credenciais inválidas")
            
            # Verifica status
            if user.status == "BLOCKED":
                self._log_action(
                    action="LOGIN_FAILED",
                    user_id=user.id,
                    resource="SESSION",
                    details={"reason": "user_blocked"},
                    success=False
                )
                raise AuthenticationError("Usuário bloqueado. Contacte o administrador.")
            
            if user.status == "INACTIVE":
                self._log_action(
                    action="LOGIN_FAILED",
                    user_id=user.id,
                    resource="SESSION",
                    details={"reason": "user_inactive"},
                    success=False
                )
                raise AuthenticationError("Usuário inativo")
            
            # Verifica senha
            if not self.hasher.verify(password, user.password_hash):
                # Incrementa tentativas falhas
                self.user_repo.increment_failed_attempts(user.id)
                
                self._log_action(
                    action="LOGIN_FAILED",
                    user_id=user.id,
                    resource="SESSION",
                    details={"reason": "invalid_password"},
                    success=False
                )
                raise AuthenticationError("Credenciais inválidas")
            
            # Verifica MFA se habilitado
            if user.mfa_enabled:
                if not mfa_code:
                    # Solicita código MFA
                    return {
                        "requires_mfa": True,
                        "user_id": user.id,
                        "mfa_type": user.mfa_type
                    }
                
                # Verifica código MFA
                if not self._verify_mfa(user, mfa_code):
                    self._log_action(
                        action="LOGIN_FAILED",
                        user_id=user.id,
                        resource="SESSION",
                        details={"reason": "invalid_mfa"},
                        success=False
                    )
                    raise AuthenticationError("Código MFA inválido")
            
            # Reset failed attempts
            self.user_repo.reset_failed_attempts(user.id)
            
            # Login bem-sucedido
            self.user_repo.update_last_login(user.id, ip_address)
            
            # Gera tokens
            tokens = self._create_tokens(user, ip_address, user_agent)
            
            self._log_action(
                action="LOGIN",
                user_id=user.id,
                resource="SESSION",
                resource_id=tokens["session_id"],
                details={"ip": ip_address},
                success=True
            )
            
            return {
                "access_token": tokens["access_token"],
                "refresh_token": tokens["refresh_token"],
                "token_type": "Bearer",
                "expires_in": self.jwt_provider.access_token_expire_minutes * 60,
                "user_id": user.id,
                "username": user.username
            }
            
        except AuthenticationError:
            raise
        except Exception as e:
            self._handle_error(e, {"username": username})
    
    def logout(self, user_id: str, session_id: Optional[str] = None, 
               revoke_all: bool = False) -> bool:
        """
        Faz logout do usuário
        """
        try:
            if revoke_all:
                # Revoga todas as sessões
                count = self.session_repo.revoke_all_user_sessions(user_id)
                self._log_action(
                    action="LOGOUT_ALL",
                    user_id=user_id,
                    resource="SESSION",
                    details={"sessions_revoked": count},
                    success=True
                )
            elif session_id:
                # Revoga sessão específica
                self.session_repo.revoke_session(session_id)
                self._log_action(
                    action="LOGOUT",
                    user_id=user_id,
                    resource="SESSION",
                    resource_id=session_id,
                    success=True
                )
            
            return True
            
        except Exception as e:
            self._handle_error(e, {"user_id": user_id})
    
    def change_password(self, user_id: str, current_password: str, 
                       new_password: str, ip_address: Optional[str] = None) -> bool:
        """
        Altera senha do usuário
        """
        try:
            user = self.user_repo.get_by_id(user_id)
            if not user:
                raise NotFoundError("User", user_id)
            
            # Verifica senha atual
            if not self.hasher.verify(current_password, user.password_hash):
                self._log_action(
                    action="PASSWORD_CHANGE_FAILED",
                    user_id=user_id,
                    resource="USER",
                    resource_id=user_id,
                    details={"reason": "invalid_current_password"},
                    success=False
                )
                raise ValidationError("Senha atual incorreta")
            
            # Valida nova senha
            is_strong, strength, messages, score = validate_password_strength(new_password)
            
            if not is_strong:
                raise ValidationError(
                    "Senha fraca",
                    details={"messages": messages, "strength": strength, "score": score}
                )
            
            # Hash da nova senha
            new_hash = self.hasher.hash(new_password)
            
            # Atualiza
            self.user_repo.update_password(user_id, new_hash)
            
            # Revoga todas as sessões (exceto atual)
            self.session_repo.revoke_all_user_sessions(user_id)
            
            self._log_action(
                action="PASSWORD_CHANGE",
                user_id=user_id,
                resource="USER",
                resource_id=user_id,
                details={"ip": ip_address},
                success=True
            )
            
            return True
            
        except Exception as e:
            self._handle_error(e, {"user_id": user_id})
    
    def setup_mfa(self, user_id: str, mfa_type: str = "TOTP") -> Dict[str, Any]:
        """
        Configura MFA para usuário
        """
        try:
            user = self.user_repo.get_by_id(user_id)
            if not user:
                raise NotFoundError("User", user_id)
            
            if mfa_type == "TOTP":
                # Gera secret
                secret = self.mfa_provider.generate_totp_secret()
                
                # Gera URI e QR code
                uri = self.mfa_provider.get_totp_uri(secret, user.email)
                qr_code = self.mfa_provider.generate_qr_code(uri)
                
                # Gera códigos de backup
                backup_codes = self.mfa_provider.generate_backup_codes()
                
                # Salva secret (temporariamente)
                # Em produção, criptografar antes de salvar
                user.mfa_secret = secret
                user.mfa_type = mfa_type
                
                self._log_action(
                    action="MFA_SETUP",
                    user_id=user_id,
                    resource="USER",
                    resource_id=user_id,
                    details={"mfa_type": mfa_type},
                    success=True
                )
                
                return {
                    "secret": secret,
                    "uri": uri,
                    "qr_code": qr_code,
                    "backup_codes": backup_codes
                }
            
            elif mfa_type == "EMAIL":
                # MFA por email não precisa de setup
                user.mfa_type = mfa_type
                user.mfa_enabled = True
                
                return {"message": "MFA por email configurado"}
            
            else:
                raise ValidationError(f"Tipo MFA não suportado: {mfa_type}")
                
        except Exception as e:
            self._handle_error(e, {"user_id": user_id, "mfa_type": mfa_type})
    
    def verify_mfa(self, user_id: str, code: str) -> bool:
        """
        Verifica código MFA
        """
        try:
            user = self.user_repo.get_by_id(user_id)
            if not user or not user.mfa_enabled:
                return False
            
            return self._verify_mfa(user, code)
            
        except Exception:
            return False
    
    def _verify_mfa(self, user, code: str) -> bool:
        """Verifica código MFA interno"""
        if user.mfa_type == "TOTP" and user.mfa_secret:
            return self.mfa_provider.verify_totp(user.mfa_secret, code)
        elif user.mfa_type == "EMAIL":
            return self.email_mfa.verify_code(user.id, code)
        return False
    
    def _create_tokens(self, user, ip_address: Optional[str], 
                       user_agent: Optional[str]) -> Dict[str, str]:
        """Cria tokens e sessão"""
        # Gera tokens JWT
        access_token = self.jwt_provider.create_access_token(
            user.id,
            [],  # roles
            []   # permissions
        )
        
        refresh_token_value = self.jwt_provider.create_refresh_token(user.id)
        
        # Cria sessão simples
        from ...infrastructure.models.session_model import SessionModel
        session = SessionModel(
            user_id=user.id,
            ip_address=ip_address,
            user_agent=user_agent,
            expires_at=datetime.now() + timedelta(hours=24)
        )
        
        self.db.add(session)
        self.db.commit()
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token_value,
            "session_id": session.id
        }
