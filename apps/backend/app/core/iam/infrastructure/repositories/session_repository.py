from typing import Optional, List
from sqlalchemy.orm import Session as SQLSession
from sqlalchemy import and_
from datetime import datetime, timedelta

from ..models.session_model import SessionModel, RefreshTokenModel
from .base_repository import BaseRepository


class SessionRepository(BaseRepository[SessionModel]):
    """Implementação do repositório de sessões"""
    
    def __init__(self, db: SQLSession):
        super().__init__(db, SessionModel)
        self.refresh_token_repo = BaseRepository(db, RefreshTokenModel)
    
    def save_session(self, session_data: dict) -> SessionModel:
        """Salva uma sessão"""
        existing = self.get_by_id(session_data.get("id"))
        if existing:
            for key, value in session_data.items():
                if value is not None and hasattr(existing, key):
                    setattr(existing, key, value)
            existing.updated_at = datetime.utcnow()
            self.db.flush()
            return existing
        else:
            model = SessionModel(**session_data)
            self.db.add(model)
            self.db.flush()
            return model
    
    def save_refresh_token(self, token_data: dict) -> RefreshTokenModel:
        """Salva um refresh token"""
        existing = self.refresh_token_repo.get_by_id(token_data.get("id"))
        if existing:
            for key, value in token_data.items():
                if value is not None and hasattr(existing, key):
                    setattr(existing, key, value)
            existing.updated_at = datetime.utcnow()
            self.db.flush()
            return existing
        else:
            model = RefreshTokenModel(**token_data)
            self.db.add(model)
            self.db.flush()
            return model
    
    def get_session_by_id(self, session_id: str) -> Optional[SessionModel]:
        """Busca sessão por ID"""
        return self.db.query(SessionModel).filter(
            SessionModel.id == session_id,
            SessionModel.is_active == True
        ).first()
    
    def get_refresh_token(self, token_hash: str) -> Optional[RefreshTokenModel]:
        """Busca refresh token por hash"""
        return self.db.query(RefreshTokenModel).filter(
            RefreshTokenModel.token_hash == token_hash,
            RefreshTokenModel.is_active == True
        ).first()
    
    def get_user_sessions(self, user_id: str, active_only: bool = True) -> List[SessionModel]:
        """Lista sessões de um usuário"""
        query = self.db.query(SessionModel).filter(SessionModel.user_id == user_id)
        
        if active_only:
            query = query.filter(
                SessionModel.is_active == True,
                SessionModel.expires_at > datetime.utcnow()
            )
        
        return query.order_by(SessionModel.last_activity_at.desc()).all()
    
    def get_user_refresh_tokens(self, user_id: str, active_only: bool = True) -> List[RefreshTokenModel]:
        """Lista refresh tokens de um usuário"""
        query = self.db.query(RefreshTokenModel).filter(RefreshTokenModel.user_id == user_id)
        
        if active_only:
            query = query.filter(
                RefreshTokenModel.revoked == False,
                RefreshTokenModel.expires_at > datetime.utcnow()
            )
        
        return query.all()
    
    def revoke_session(self, session_id: str) -> bool:
        """Revoga uma sessão"""
        model = self.db.query(SessionModel).filter(SessionModel.id == session_id).first()
        if model:
            model.is_active = False
            model.revoked_at = datetime.utcnow()
            model.updated_at = datetime.utcnow()
            self.db.flush()
            return True
        return False
    
    def revoke_refresh_token(self, token_hash: str) -> bool:
        """Revoga um refresh token"""
        model = self.db.query(RefreshTokenModel).filter(
            RefreshTokenModel.token_hash == token_hash
        ).first()
        if model:
            model.revoked = True
            model.revoked_at = datetime.utcnow()
            model.updated_at = datetime.utcnow()
            self.db.flush()
            return True
        return False
    
    def revoke_all_user_sessions(self, user_id: str, exclude_session_id: Optional[str] = None) -> int:
        """Revoga todas as sessões de um usuário"""
        query = self.db.query(SessionModel).filter(
            SessionModel.user_id == user_id,
            SessionModel.is_active == True
        )
        
        if exclude_session_id:
            query = query.filter(SessionModel.id != exclude_session_id)
        
        count = query.update({
            "is_active": False,
            "revoked_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        })
        
        self.db.flush()
        return count
    
    def revoke_all_user_refresh_tokens(self, user_id: str, exclude_token_id: Optional[str] = None) -> int:
        """Revoga todos os refresh tokens de um usuário"""
        query = self.db.query(RefreshTokenModel).filter(
            RefreshTokenModel.user_id == user_id,
            RefreshTokenModel.revoked == False
        )
        
        if exclude_token_id:
            query = query.filter(RefreshTokenModel.id != exclude_token_id)
        
        count = query.update({
            "revoked": True,
            "revoked_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        })
        
        self.db.flush()
        return count
    
    def cleanup_expired(self) -> int:
        """Remove sessões e tokens expirados"""
        now = datetime.utcnow()
        count = 0
        
        # Revoga sessões expiradas
        expired_sessions = self.db.query(SessionModel).filter(
            SessionModel.expires_at < now,
            SessionModel.is_active == True
        ).update({
            "is_active": False,
            "revoked_at": now,
            "updated_at": now
        })
        count += expired_sessions
        
        # Revoga refresh tokens expirados
        expired_tokens = self.db.query(RefreshTokenModel).filter(
            RefreshTokenModel.expires_at < now,
            RefreshTokenModel.revoked == False
        ).update({
            "revoked": True,
            "revoked_at": now,
            "updated_at": now
        })
        count += expired_tokens
        
        self.db.flush()
        return count
    
    def update_session_activity(self, session_id: str) -> bool:
        """Atualiza timestamp de última atividade"""
        model = self.db.query(SessionModel).filter(SessionModel.id == session_id).first()
        if model and model.is_active:
            model.last_activity_at = datetime.utcnow()
            model.updated_at = datetime.utcnow()
            self.db.flush()
            return True
        return False
