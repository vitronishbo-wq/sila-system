import re
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Email:
    """Value Object para email com validação"""
    value: str
    
    # Regex para validação de email (RFC 5322)
    PATTERN = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    
    def __post_init__(self):
        if not self.value or not isinstance(self.value, str):
            raise ValueError("Email deve ser uma string não vazia")
        
        email = self.value.strip().lower()
        if not re.match(self.PATTERN, email):
            raise ValueError(f"Email inválido: {self.value}")
        
        # Normaliza para lowercase
        object.__setattr__(self, 'value', email)
    
    @property
    def local_part(self) -> str:
        """Parte local do email (antes do @)"""
        return self.value.split('@')[0]
    
    @property
    def domain(self) -> str:
        """Domínio do email"""
        return self.value.split('@')[1]
    
    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True)
class EmailAddress:
    """Email com nome de exibição opcional"""
    email: Email
    display_name: Optional[str] = None
    
    @property
    def formatted(self) -> str:
        """Email formatado para exibição"""
        if self.display_name:
            return f"{self.display_name} <{self.email}>"
        return str(self.email)
    
    def __str__(self) -> str:
        return str(self.email)
