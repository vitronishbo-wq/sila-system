import re
import secrets
import string
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional, List


class PasswordPolicy:
    """Política de senhas do sistema"""
    
    MIN_LENGTH = 8
    MAX_LENGTH = 128
    REQUIRE_UPPERCASE = True
    REQUIRE_LOWERCASE = True
    REQUIRE_DIGITS = True
    REQUIRE_SPECIAL = True
    SPECIAL_CHARS = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    @classmethod
    def validate(cls, password: str) -> List[str]:
        """Valida senha contra a política e retorna lista de erros"""
        errors = []
        
        if len(password) < cls.MIN_LENGTH:
            errors.append(f"Senha deve ter no mínimo {cls.MIN_LENGTH} caracteres")
        
        if len(password) > cls.MAX_LENGTH:
            errors.append(f"Senha deve ter no máximo {cls.MAX_LENGTH} caracteres")
        
        if cls.REQUIRE_UPPERCASE and not re.search(r"[A-Z]", password):
            errors.append("Senha deve conter pelo menos uma letra maiúscula")
        
        if cls.REQUIRE_LOWERCASE and not re.search(r"[a-z]", password):
            errors.append("Senha deve conter pelo menos uma letra minúscula")
        
        if cls.REQUIRE_DIGITS and not re.search(r"\d", password):
            errors.append("Senha deve conter pelo menos um número")
        
        if cls.REQUIRE_SPECIAL and not any(c in cls.SPECIAL_CHARS for c in password):
            errors.append(f"Senha deve conter pelo menos um caractere especial {cls.SPECIAL_CHARS}")
        
        return errors
    
    @classmethod
    def is_valid(cls, password: str) -> bool:
        """Verifica se senha é válida"""
        return len(cls.validate(password)) == 0


@dataclass(frozen=True)
class Password:
    """Value Object para senha (nunca armazena o valor original)"""
    hash_value: str
    algorithm: str = "argon2id"
    
    @classmethod
    def generate_random(cls, length: int = 12) -> str:
        """Gera senha aleatória segura"""
        alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
        return ''.join(secrets.choice(alphabet) for _ in range(length))
    
    def __str__(self) -> str:
        """Nunca expõe o hash em string"""
        return "********"
    
    def __repr__(self) -> str:
        return f"<Password hash={self.hash_value[:10]}...>"


@dataclass
class PasswordResetToken:
    """Token para reset de senha"""
    token: str
    user_id: str
    expires_at: datetime
    used: bool = False
    created_at: datetime = field(default_factory=datetime.now)
    
    @classmethod
    def generate(cls, user_id: str, ttl_minutes: int = 30) -> 'PasswordResetToken':
        """Gera novo token de reset"""
        token = secrets.token_urlsafe(32)
        expires_at = datetime.now() + timedelta(minutes=ttl_minutes)
        return cls(token=token, user_id=user_id, expires_at=expires_at)
    
    @property
    def is_expired(self) -> bool:
        """Verifica se token expirou"""
        return datetime.now() > self.expires_at
    
    def mark_used(self):
        """Marca token como utilizado"""
        self.used = True
