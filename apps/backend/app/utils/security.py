"""
Utilitários de segurança para IAM
"""
import re
import secrets
from typing import Optional
from datetime import datetime
import hashlib
import hmac

def sanitize_input(value: str) -> str:
    """Sanitiza input para prevenir XSS"""
    if not value:
        return value
    return re.sub('<[^>]*>', '', value).strip()

def generate_secure_token(length: int=32) -> str:
    """Gera token seguro aleatório"""
    return secrets.token_urlsafe(length)

def hash_token(token: str) -> str:
    """Gera hash de token para armazenamento seguro"""
    return hashlib.blake2b(token.encode(), digest_size=32).hexdigest()

def verify_token_hash(token: str, token_hash: str) -> bool:
    """Verifica token contra hash"""
    return hmac.compare_digest(hash_token(token), token_hash)

def mask_email(email: str) -> str:
    """Mascara email para exibição (ex: j***@gmail.com)"""
    if not email or '@' not in email:
        return email
    local, domain = email.split('@')
    if len(local) <= 2:
        masked_local = local[0] + '*' * (len(local) - 1)
    else:
        masked_local = local[0] + '*' * (len(local) - 2) + local[-1]
    return f'{masked_local}@{domain}'

def mask_phone(phone: str) -> str:
    """Mascara telefone para exibição"""
    if not phone or len(phone) < 8:
        return phone
    return '*' * (len(phone) - 4) + phone[-4:]

def is_password_compromised(password: str) -> bool:
    """
    Verifica se senha está em lista de senhas comuns
    Em produção, integrar com HaveIBeenPwned API
    """
    common_passwords = ['123456', 'password', '12345678', 'qwerty', '123456789', '12345', '1234', '111111', '1234567', 'dragon', '123123', 'baseball', 'abc123', 'football', 'monkey', 'letmein', 'shadow', 'master', '666666', 'qwertyuiop', '123321', 'mustang', '1234567890', 'michael', '654321', 'superman', '1qaz2wsx', '7777777', '121212', '000000']
    return password.lower() in common_passwords

def validate_password_strength(password: str) -> tuple:
    """
    Valida força da senha e retorna (is_strong, strength, messages, score)
    Score: 0-4 (0 muito fraca, 4 muito forte)
    """
    score = 0
    messages = []
    if len(password) >= 12:
        score += 2
    elif len(password) >= 8:
        score += 1
    else:
        messages.append('Senha muito curta')
    if re.search('[A-Z]', password):
        score += 1
    else:
        messages.append('Inclua letras maiúsculas')
    if re.search('[a-z]', password):
        score += 1
    else:
        messages.append('Inclua letras minúsculas')
    if re.search('\\d', password):
        score += 1
    else:
        messages.append('Inclua números')
    if re.search('[!@#$%^&*()_+\\-=\\[\\]{};\\\':"\\\\|,.<>/?]', password):
        score += 1
    else:
        messages.append('Inclua caracteres especiais')
    if is_password_compromised(password):
        messages.append('Senha muito comum, escolha outra')
        score = max(0, score - 2)
    if score >= 5:
        strength = 'MUITO_FORTE'
        is_strong = True
    elif score >= 4:
        strength = 'FORTE'
        is_strong = True
    elif score >= 3:
        strength = 'MÉDIA'
        is_strong = False
    else:
        strength = 'FRACA'
        is_strong = False
    return (is_strong, strength, messages, score)

def generate_session_id() -> str:
    """Gera ID único para sessão"""
    return secrets.token_hex(16)

def get_client_ip(request) -> Optional[str]:
    """Extrai IP do cliente do request"""
    forwarded = request.headers.get('X-Forwarded-For')
    if forwarded:
        return forwarded.split(',')[0].strip()
    return request.client.host if request.client else None

def get_user_agent(request) -> Optional[str]:
    """Extrai User-Agent do request"""
    return request.headers.get('User-Agent')

def rate_limit_key(user_id: str, action: str) -> str:
    """Gera chave para rate limiting"""
    return f'rate_limit:{user_id}:{action}:{datetime.now().strftime('%Y%m%d%H')}'