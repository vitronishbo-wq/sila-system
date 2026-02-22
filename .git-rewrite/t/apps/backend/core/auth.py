"""JWT helper utilities for access and refresh tokens."""

from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Iterable, Optional

import jwt
from jwt import InvalidTokenError
from pydantic import BaseModel

from config import settings

# ⚠️ CRÍTICO: Validar AUTH_SECRET_KEY em tempo de inicialização
if not settings.AUTH_SECRET_KEY or settings.AUTH_SECRET_KEY == "change_me_immediately":
    raise ValueError(
        "❌ AUTH_SECRET_KEY não configurado! Defina AUTH_SECRET_KEY em .env ou .env.development"
    )

ACCESS_TOKEN_EXPIRE_MINUTES = getattr(settings, "ACCESS_TOKEN_EXPIRE_MINUTES", 15)
REFRESH_TOKEN_EXPIRE_DAYS = getattr(settings, "REFRESH_TOKEN_EXPIRE_DAYS", 7)

# ✅ Hierarquia clara: AUTH_SECRET_KEY é a única fonte de verdade
# (Ambiguidade #1, #2 resolvidas - sem múltiplos fallbacks)
ACCESS_SECRET = settings.AUTH_SECRET_KEY
REFRESH_SECRET = settings.AUTH_SECRET_KEY

ALGORITHM = getattr(settings, "ALGORITHM", "HS256")


class DecodedToken(BaseModel):
    """Common JWT payload representation."""

    sub: str
    exp: int
    type: str
    iat: Optional[int] = None


def _iter_secrets(primary: str, fallback: str = None) -> Iterable[str]:
    """Iterar sobre secrets em ordem de prioridade.

    ✅ FASE 1: Remover fallbacks silenciosos
    Agora apenas retorna o secret primário.
    (Ambiguidade #1, #2 resolvidas)
    """
    if primary and primary not in ("change_me_immediately", "super-secret-key"):
        yield primary
    # ⚠️ REMOVED: fallback logic (causing ambiguity #1, #2)


def _encode(payload: Dict[str, Any], secret: str, expires_delta: timedelta) -> str:
    to_encode = payload.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire, "iat": datetime.now(timezone.utc)})
    return jwt.encode(to_encode, secret, algorithm=ALGORITHM)


def create_access_token(
    *,
    subject: str,
    additional_claims: Optional[Dict[str, Any]] = None,
    expires_delta: Optional[timedelta] = None,
) -> str:
    """Generate an access token with optional extra claims and expiry override."""

    claims: Dict[str, Any] = {"sub": subject, "type": "access"}
    if additional_claims:
        claims.update(additional_claims)

    expiry = expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return _encode(claims, ACCESS_SECRET, expiry)


def create_refresh_token(
    *,
    subject: str,
    additional_claims: Optional[Dict[str, Any]] = None,
    expires_delta: Optional[timedelta] = None,
) -> str:
    """Generate a refresh token with optional extra claims and expiry override."""

    claims: Dict[str, Any] = {"sub": subject, "type": "refresh"}
    if additional_claims:
        claims.update(additional_claims)

    expiry = expires_delta or timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    return _encode(claims, REFRESH_SECRET, expiry)


def _decode(
    token: str, *, expected_type: str, secrets: Iterable[str], verify_exp: bool = True
) -> DecodedToken:
    last_error: Optional[Exception] = None
    options = {"verify_exp": verify_exp}

    for secret in secrets:
        try:
            payload = jwt.decode(token, secret, algorithms=[ALGORITHM], options=options)
            if payload.get("type") != expected_type:
                raise InvalidTokenError("Unexpected token type")
            return DecodedToken(**payload)
        except jwt.ExpiredSignatureError as exc:
            # Don't try other secrets if the signature is valid but token expired.
            last_error = exc
            break
        except (
            Exception
        ) as exc:  # noqa: BLE001 - propagate last failure when all secrets exhausted
            last_error = exc
            continue

    if isinstance(last_error, jwt.ExpiredSignatureError):
        raise last_error
    raise InvalidTokenError("Token validation failed") from last_error


def decode_access_token(token: str, *, verify_exp: bool = True) -> DecodedToken:
    """Decodificar token de acesso usando AUTH_SECRET_KEY.

    ✅ FASE 1: Usar único secret (sem fallbacks)
    """
    secrets = _iter_secrets(ACCESS_SECRET)
    return _decode(
        token, expected_type="access", secrets=secrets, verify_exp=verify_exp
    )


def decode_refresh_token(token: str, *, verify_exp: bool = True) -> DecodedToken:
    """Decodificar token de refresh usando AUTH_SECRET_KEY.

    ✅ FASE 1: Usar único secret (sem fallbacks)
    """
    secrets = _iter_secrets(REFRESH_SECRET)
    return _decode(
        token, expected_type="refresh", secrets=secrets, verify_exp=verify_exp
    )
