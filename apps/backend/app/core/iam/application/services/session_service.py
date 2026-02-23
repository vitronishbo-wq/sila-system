from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session as SQLSession

from .base_service import BaseService, NotFoundError


class SessionService(BaseService):
    """Serviço de gestão de sessões"""
    
    def __init__(self, db: SQLSession):
        super().__init__(db)
    
    def get_user_sessions(self, user_id: str, active_only: bool = True) -> List:
        """
        Lista sessões de um usuário
        """
        return self.session_repo.get_user_sessions(user_id, active_only)
    
    def get_session(self, session_id: str):
        """
        Busca sessão por ID
        """
        session = self.session_repo.get_session_by_id(session_id)
        if not session:
            raise NotFoundError("Session", session_id)
        return session
    
    def revoke_session(self, session_id: str, revoked_by: str) -> bool:
        """
        Revoga uma sessão específica
        """
        try:
            session = self.session_repo.get_session_by_id(session_id)
            if not session:
                raise NotFoundError("Session", session_id)
            
            result = self.session_repo.revoke_session(session_id)
            
            if result:
                self._log_action(
                    action="REVOKE_SESSION",
                    user_id=revoked_by,
                    resource="SESSION",
                    resource_id=session_id,
                    details={"user_id": session.user_id},
                    success=True
                )
            
            return result
            
        except Exception as e:
            self.db.rollback()
            self._handle_error(e, {"session_id": session_id})
    
    def revoke_all_user_sessions(self, user_id: str, revoked_by: str, 
                                 exclude_session_id: Optional[str] = None) -> int:
        """
        Revoga todas as sessões de um usuário
        """
        try:
            count = self.session_repo.revoke_all_user_sessions(user_id, exclude_session_id)
            
            self._log_action(
                action="REVOKE_ALL_SESSIONS",
                user_id=revoked_by,
                resource="SESSION",
                resource_id=user_id,
                details={"sessions_revoked": count},
                success=True
            )
            
            return count
            
        except Exception as e:
            self.db.rollback()
            self._handle_error(e, {"user_id": user_id})
    
    def cleanup_expired(self) -> Dict[str, int]:
        """
        Limpa sessões e tokens expirados
        """
        try:
            count = self.session_repo.cleanup_expired()
            
            self._log_action(
                action="CLEANUP_SESSIONS",
                user_id="system",
                resource="SESSION",
                details={"cleaned": count},
                success=True
            )
            
            return {"cleaned": count}
            
        except Exception as e:
            self.db.rollback()
            self._handle_error(e)
    
    def get_active_sessions_count(self, user_id: Optional[str] = None) -> int:
        """
        Conta sessões ativas
        """
        if user_id:
            return len(self.session_repo.get_user_sessions(user_id, active_only=True))
        else:
            return 0
    
    def get_session_info(self, session_id: str) -> Dict[str, Any]:
        """
        Obtém informações detalhadas da sessão
        """
        session = self.get_session(session_id)
        
        expires_at = session.expires_at if hasattr(session, 'expires_at') else None
        
        return {
            "id": session.id,
            "user_id": session.user_id,
            "ip_address": getattr(session, 'ip_address', None),
            "user_agent": getattr(session, 'user_agent', None),
            "created_at": session.created_at.isoformat() if hasattr(session, 'created_at') else None,
            "is_active": session.is_active if hasattr(session, 'is_active') else True,
            "expires_at": expires_at.isoformat() if expires_at else None,
        }
