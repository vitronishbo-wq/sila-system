import hashlib
import secrets
import string
from typing import Tuple
from passlib.context import CryptContext
from datetime import datetime, timedelta


class PasswordPolicy:
    """Política de senhas"""
    MIN_LENGTH = 8
    SPECIAL_CHARS = "!@#$%^&*()_+-=[]{}';:\"\\|,.<>/?`~"


class Argon2PasswordHasher:
    """Implementação de hashing de senha com Argon2 (recomendado)"""
    
    def __init__(self):
        # Contexto do passlib com Argon2
        self.pwd_context = CryptContext(
            schemes=["argon2", "bcrypt"],
            default="argon2",
            argon2__memory_cost=102400,  # 100MB
            argon2__time_cost=3,
            argon2__parallelism=4,
            bcrypt__rounds=12
        )
    
    def hash(self, password: str) -> str:
        """Gera hash da senha usando Argon2"""
        if not password or len(password) < PasswordPolicy.MIN_LENGTH:
            raise ValueError(f"Senha deve ter no mínimo {PasswordPolicy.MIN_LENGTH} caracteres")
        
        return self.pwd_context.hash(password)
    
    def verify(self, password: str, password_hash: str) -> bool:
        """Verifica se senha corresponde ao hash"""
        try:
            return self.pwd_context.verify(password, password_hash)
        except Exception:
            return False
    
    def needs_rehash(self, password_hash: str) -> bool:
        """Verifica se hash precisa ser atualizado"""
        return self.pwd_context.needs_update(password_hash)


class BcryptPasswordHasher:
    """Implementação alternativa com bcrypt (fallback)"""
    
    def __init__(self, rounds: int = 12):
        self.pwd_context = CryptContext(
            schemes=["bcrypt"],
            default="bcrypt",
            bcrypt__rounds=rounds
        )
    
    def hash(self, password: str) -> str:
        if not password or len(password) < PasswordPolicy.MIN_LENGTH:
            raise ValueError(f"Senha deve ter no mínimo {PasswordPolicy.MIN_LENGTH} caracteres")
        
        return self.pwd_context.hash(password)
    
    def verify(self, password: str, password_hash: str) -> bool:
        try:
            return self.pwd_context.verify(password, password_hash)
        except Exception:
            return False
    
    def needs_rehash(self, password_hash: str) -> bool:
        return self.pwd_context.needs_update(password_hash)


class PasswordGenerator:
    """Gerador de senhas seguras"""
    
    @staticmethod
    def generate(length: int = 16, 
                 use_uppercase: bool = True,
                 use_lowercase: bool = True,
                 use_digits: bool = True,
                 use_special: bool = True) -> str:
        """
        Gera senha aleatória segura
        """
        if length < PasswordPolicy.MIN_LENGTH:
            length = PasswordPolicy.MIN_LENGTH
        
        chars = ""
        if use_uppercase:
            chars += string.ascii_uppercase
        if use_lowercase:
            chars += string.ascii_lowercase
        if use_digits:
            chars += string.digits
        if use_special:
            chars += PasswordPolicy.SPECIAL_CHARS
        
        if not chars:
            chars = string.ascii_letters + string.digits
        
        # Garantir pelo menos um de cada tipo
        password = []
        if use_uppercase:
            password.append(secrets.choice(string.ascii_uppercase))
        if use_lowercase:
            password.append(secrets.choice(string.ascii_lowercase))
        if use_digits:
            password.append(secrets.choice(string.digits))
        if use_special:
            password.append(secrets.choice(PasswordPolicy.SPECIAL_CHARS))
        
        # Preencher o resto
        remaining = length - len(password)
        for _ in range(remaining):
            password.append(secrets.choice(chars))
        
        # Embaralhar
        secrets.SystemRandom().shuffle(password)
        
        return ''.join(password)
    
    @staticmethod
    def generate_pin(length: int = 6) -> str:
        """Gera PIN numérico (para MFA)"""
        if length < 4:
            length = 4
        return ''.join(secrets.choice(string.digits) for _ in range(length))
    
    @staticmethod
    def generate_temporary_password() -> Tuple[str, datetime]:
        """Gera senha temporária com expiração"""
        password = PasswordGenerator.generate(length=12)
        expires_at = datetime.now() + timedelta(hours=24)
        return password, expires_at
