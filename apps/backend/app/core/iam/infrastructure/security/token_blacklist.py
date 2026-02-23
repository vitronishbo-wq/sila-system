from datetime import datetime

from ..models.audit_model import TokenBlacklistModel
from sqlalchemy.orm import Session


class RedisTokenBlacklist:
    """Blacklist de tokens usando Redis (recomendado para produção)"""
    
    def __init__(self, redis_client):
        self.redis = redis_client
        self.prefix = "token_blacklist:"
    
    def add_to_blacklist(self, token: str, expires_at: datetime) -> bool:
        """Adiciona token à blacklist"""
        try:
            # Usar JTI como chave
            import jwt
            payload = jwt.decode(token, options={"verify_signature": False})
            jti = payload.get("jti")
            
            if not jti:
                return False
            
            key = f"{self.prefix}{jti}"
            ttl = int((expires_at - datetime.utcnow()).total_seconds())
            
            if ttl > 0:
                self.redis.setex(key, ttl, "1")
                return True
            return False
        except Exception:
            return False
    
    def is_blacklisted(self, token: str) -> bool:
        """Verifica se token está na blacklist"""
        try:
            import jwt
            payload = jwt.decode(token, options={"verify_signature": False})
            jti = payload.get("jti")
            
            if not jti:
                return False
            
            key = f"{self.prefix}{jti}"
            return self.redis.exists(key) > 0
        except Exception:
            return False
    
    def clean_expired(self) -> int:
        """Redis faz expiração automática, retorna 0"""
        return 0


class DatabaseTokenBlacklist:
    """Blacklist de tokens usando banco de dados (fallback)"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def add_to_blacklist(self, token: str, expires_at: datetime) -> bool:
        """Adiciona token à blacklist"""
        try:
            import jwt
            payload = jwt.decode(token, options={"verify_signature": False})
            jti = payload.get("jti")
            token_type = payload.get("type", "unknown")
            
            if not jti:
                return False
            
            blacklist_entry = TokenBlacklistModel(
                token_jti=jti,
                token_type=token_type,
                expires_at=expires_at
            )
            
            self.db.add(blacklist_entry)
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            return False
    
    def is_blacklisted(self, token: str) -> bool:
        """Verifica se token está na blacklist"""
        try:
            import jwt
            payload = jwt.decode(token, options={"verify_signature": False})
            jti = payload.get("jti")
            
            if not jti:
                return False
            
            entry = self.db.query(TokenBlacklistModel).filter(
                TokenBlacklistModel.token_jti == jti,
                TokenBlacklistModel.expires_at > datetime.utcnow()
            ).first()
            
            return entry is not None
        except Exception:
            return False
    
    def clean_expired(self) -> int:
        """Remove tokens expirados da blacklist"""
        result = self.db.query(TokenBlacklistModel).filter(
            TokenBlacklistModel.expires_at <= datetime.utcnow()
        ).delete()
        self.db.commit()
        return result


class MemoryTokenBlacklist:
    """Blacklist em memória (apenas para desenvolvimento)"""
    
    def __init__(self):
        self.blacklist = {}
    
    def add_to_blacklist(self, token: str, expires_at: datetime) -> bool:
        try:
            import jwt
            payload = jwt.decode(token, options={"verify_signature": False})
            jti = payload.get("jti")
            
            if jti:
                self.blacklist[jti] = expires_at
                return True
            return False
        except Exception:
            return False
    
    def is_blacklisted(self, token: str) -> bool:
        try:
            import jwt
            payload = jwt.decode(token, options={"verify_signature": False})
            jti = payload.get("jti")
            
            if jti and jti in self.blacklist:
                expires = self.blacklist[jti]
                if expires > datetime.utcnow():
                    return True
                else:
                    del self.blacklist[jti]
            return False
        except Exception:
            return False
    
    def clean_expired(self) -> int:
        now = datetime.utcnow()
        expired = [jti for jti, exp in self.blacklist.items() if exp <= now]
        for jti in expired:
            del self.blacklist[jti]
        return len(expired)
