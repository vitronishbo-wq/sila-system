from __future__ import annotations
import base64
import hashlib
import os
import time
import uuid
from pathlib import Path
from dataclasses import dataclass
from typing import Any, Dict, Optional
from jose import jwt
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
DEFAULT_TOKEN_TTL_SECONDS = 3600
DEFAULT_ALGORITHM = 'RS256'

@dataclass(frozen=True)
class ProviderConfig:
    issuer: str
    audience: Optional[str]
    algorithm: str
    token_ttl_seconds: int

@dataclass(frozen=True)
class ProviderKeys:
    private_key_pem: str
    public_key_pem: str
    kid: str
    jwk: Dict[str, Any]
_KEYS: Optional[ProviderKeys] = None
DEFAULT_KEY_DIR_NAME = '.secrets/oidc'
DEFAULT_PRIVATE_KEY_NAME = 'oidc_provider_private.pem'
DEFAULT_PUBLIC_KEY_NAME = 'oidc_provider_public.pem'

def _normalize_pem(value: Optional[str]) -> Optional[str]:
    if not value:
        return None
    if '\\n' in value and 'BEGIN' in value:
        return value.replace('\\n', '\n')
    return value

def _backend_root() -> Path:
    return Path(__file__).resolve().parents[5]

def _default_key_dir() -> Path:
    return _backend_root() / DEFAULT_KEY_DIR_NAME

def _read_key_from_path(path_value: Optional[str]) -> Optional[str]:
    if not path_value:
        return None
    path = Path(path_value).expanduser()
    if not path.is_absolute():
        path = _backend_root() / path
    if path.exists():
        return path.read_text(encoding='utf-8')
    return None

def _resolve_key_paths() -> tuple[Optional[str], Optional[str]]:
    private_path = os.getenv('OIDC_PROVIDER_PRIVATE_KEY_PATH')
    public_path = os.getenv('OIDC_PROVIDER_PUBLIC_KEY_PATH')
    key_dir = os.getenv('OIDC_PROVIDER_KEY_DIR')
    if not key_dir:
        default_dir = _default_key_dir()
        private_default = default_dir / DEFAULT_PRIVATE_KEY_NAME
        public_default = default_dir / DEFAULT_PUBLIC_KEY_NAME
        return (str(private_default), str(public_default))
    base = Path(key_dir).expanduser()
    if not base.is_absolute():
        base = _backend_root() / base
    private_default = base / DEFAULT_PRIVATE_KEY_NAME
    public_default = base / DEFAULT_PUBLIC_KEY_NAME
    return (private_path or str(private_default), public_path or str(public_default))

def _b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b'=').decode('ascii')

def _build_jwk(public_key, kid: str) -> Dict[str, Any]:
    numbers = public_key.public_numbers()
    n = numbers.n.to_bytes((numbers.n.bit_length() + 7) // 8, 'big')
    e = numbers.e.to_bytes((numbers.e.bit_length() + 7) // 8, 'big')
    return {'kty': 'RSA', 'use': 'sig', 'alg': DEFAULT_ALGORITHM, 'kid': kid, 'n': _b64url(n), 'e': _b64url(e)}

def _compute_kid(public_key) -> str:
    public_der = public_key.public_bytes(encoding=serialization.Encoding.DER, format=serialization.PublicFormat.SubjectPublicKeyInfo)
    digest = hashlib.sha256(public_der).digest()
    return _b64url(digest)

def load_provider_config() -> ProviderConfig:
    issuer = os.getenv('OIDC_PROVIDER_ISSUER') or os.getenv('OIDC_ISSUER') or 'sila-oidc'
    audience = os.getenv('OIDC_PROVIDER_AUDIENCE') or os.getenv('OIDC_AUDIENCE')
    algorithm = os.getenv('OIDC_PROVIDER_ALGORITHM') or os.getenv('OIDC_ALGORITHM') or DEFAULT_ALGORITHM
    token_ttl_seconds = int(os.getenv('OIDC_PROVIDER_TOKEN_TTL', str(DEFAULT_TOKEN_TTL_SECONDS)))
    return ProviderConfig(issuer=issuer, audience=audience, algorithm=algorithm, token_ttl_seconds=token_ttl_seconds)

def get_provider_keys() -> ProviderKeys:
    global _KEYS
    if _KEYS:
        return _KEYS
    private_pem = _normalize_pem(os.getenv('OIDC_PROVIDER_PRIVATE_KEY'))
    public_pem = _normalize_pem(os.getenv('OIDC_PROVIDER_PUBLIC_KEY'))
    private_path, public_path = _resolve_key_paths()
    if not private_pem:
        private_pem = _normalize_pem(_read_key_from_path(private_path))
    if not public_pem:
        public_pem = _normalize_pem(_read_key_from_path(public_path))
    if private_pem:
        private_key = serialization.load_pem_private_key(private_pem.encode('utf-8'), password=None)
        if not public_pem:
            public_pem = private_key.public_key().public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo).decode('utf-8')
        public_key = private_key.public_key()
    elif public_pem:
        raise ValueError('OIDC_PROVIDER_PRIVATE_KEY is required to issue JWTs')
    else:
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        private_pem = private_key.private_bytes(encoding=serialization.Encoding.PEM, format=serialization.PrivateFormat.PKCS8, encryption_algorithm=serialization.NoEncryption()).decode('utf-8')
        public_pem = private_key.public_key().public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo).decode('utf-8')
        public_key = private_key.public_key()
    kid = _compute_kid(public_key)
    jwk = _build_jwk(public_key, kid)
    _KEYS = ProviderKeys(private_key_pem=private_pem, public_key_pem=public_pem, kid=kid, jwk=jwk)
    return _KEYS

def get_jwks() -> Dict[str, Any]:
    keys = get_provider_keys()
    return {'keys': [keys.jwk]}

def issue_access_token(subject: str, claims: Dict[str, Any], scope: Optional[str]=None) -> Dict[str, Any]:
    config = load_provider_config()
    if config.algorithm.upper() != DEFAULT_ALGORITHM:
        raise ValueError('Only RS256 is supported for OIDC provider tokens')
    keys = get_provider_keys()
    now = int(time.time())
    payload: Dict[str, Any] = {'sub': subject, 'iat': now, 'exp': now + config.token_ttl_seconds, 'iss': config.issuer, 'jti': str(uuid.uuid4())}
    if config.audience:
        payload['aud'] = config.audience
    if scope:
        payload['scope'] = scope
    sanitized_claims = dict(claims)
    for reserved in ('sub', 'iss', 'aud', 'exp', 'iat', 'nbf', 'jti'):
        sanitized_claims.pop(reserved, None)
    payload.update(sanitized_claims)
    token = jwt.encode(payload, keys.private_key_pem, algorithm=config.algorithm, headers={'kid': keys.kid})
    return {'access_token': token, 'token_type': 'Bearer', 'expires_in': config.token_ttl_seconds, 'scope': scope}