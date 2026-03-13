import jwt
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional
from uuid import UUID
from jwt.exceptions import InvalidTokenError
from pydantic import BaseModel
from config.settings import settings

# Configurações centralizadas vindas do settings
ACCESS_TOKEN_EXPIRE_MINUTES = getattr(settings, "ACCESS_TOKEN_EXPIRE_MINUTES", 129600)  # 90 dias em minutos
REFRESH_TOKEN_EXPIRE_DAYS = getattr(settings, "REFRESH_TOKEN_EXPIRE_DAYS", 90)          # 90 dias
ALGORITHM = "HS256"
AUTH_SECRET = settings.AUTH_SECRET_KEY  # chave definida no settings.py

class DecodedToken(BaseModel):
    """Schema para validação e acesso aos dados do JWT."""
    sub: str
    exp: int
    type: str
    iat: Optional[int] = None
    
    def get(self, key: str) -> Any:
        return getattr(self, key, None)

def _encode(payload: Dict[str, Any], secret: str, expires_delta: timedelta) -> str:
    to_encode = payload.copy()
    now = datetime.now(timezone.utc)
    expire = now + expires_delta
    to_encode.update({"exp": expire, "iat": now})
    
    # 🔧 Convert UUID objects to strings for JSON serialization
    to_encode = {
        k: str(v) if isinstance(v, UUID) else v 
        for k, v in to_encode.items()
    }
    
    return jwt.encode(to_encode, secret, algorithm=ALGORITHM)

def create_access_token(
    subject: str,
    data: Optional[Dict[str, Any]] = None,
    expires_delta: Optional[timedelta] = None,
) -> str:
    claims = data.copy() if data else {}
    claims.update({"type": "access", "sub": str(subject)})
    expiry = expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return _encode(claims, AUTH_SECRET, expiry)

def create_refresh_token(
    subject: str,
    data: Optional[Dict[str, Any]] = None,
    expires_delta: Optional[timedelta] = None,
) -> str:
    claims = data.copy() if data else {}
    claims.update({"type": "refresh", "sub": str(subject)})
    expiry = expires_delta or timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    return _encode(claims, AUTH_SECRET, expiry)

def decode_token(token: str, verify_exp: bool = True) -> Dict[str, Any]:
    try:
        options = {"verify_exp": verify_exp}
        payload = jwt.decode(token, AUTH_SECRET, algorithms=[ALGORITHM], options=options)
        return payload
    except Exception as e:
        raise InvalidTokenError(str(e))

def decode_access_token(token: str, verify_exp: bool = True) -> DecodedToken:
    payload = decode_token(token, verify_exp=verify_exp)
    if payload.get("type") != "access":
        raise InvalidTokenError("O token fornecido não é um token de acesso")
    return DecodedToken(**payload)

def decode_refresh_token(token: str, verify_exp: bool = True) -> DecodedToken:
    payload = decode_token(token, verify_exp=verify_exp)
    if payload.get("type") != "refresh":
        raise InvalidTokenError("O token fornecido não é um token de atualização")
    return DecodedToken(**payload)
