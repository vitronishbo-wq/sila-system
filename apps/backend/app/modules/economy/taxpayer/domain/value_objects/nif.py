"""NIF Value Object - Número de Identificação Fiscal Angolano"""
from dataclasses import dataclass
import re

@dataclass(frozen=True)
class NIF:
    """
    Value Object para NIF (Número de Identificação Fiscal) angolano.
    
    Validação:
    - NIF simples: 9 dígitos (ex: 123456789)
    - NIF estendido: 14 dígitos (ex: 12345678912345)
    """
    value: str

    def __post_init__(self) -> None:
        """Valida o NIF no momento da instanciação."""
        if not self._is_valid(self.value):
            raise ValueError(f'NIF inválido: {self.value}. Deve ter 9 ou 14 dígitos.')

    @staticmethod
    def _is_valid(nif: str) -> bool:
        """
        Valida formato do NIF angolano.
        
        Args:
            nif: String contendo o NIF
            
        Returns:
            True se o NIF é válido, False caso contrário
        """
        if not nif:
            return False
        pattern = '^\\d{9}(\\d{5})?$'
        return bool(re.match(pattern, nif.strip()))

    def __str__(self) -> str:
        """Retorna o valor do NIF formatado."""
        return self.value

    def __repr__(self) -> str:
        """Representação para debug."""
        return f'NIF({self.value})'

    def format_display(self) -> str:
        """
        Retorna o NIF formatado para exibição.
        
        Exemplo: 123456789 -> 123-456-789
        """
        nif = self.value.strip()
        if len(nif) == 9:
            return f'{nif[:3]}-{nif[3:6]}-{nif[6:]}'
        elif len(nif) == 14:
            return f'{nif[:3]}-{nif[3:6]}-{nif[6:9]}-{nif[9:12]}-{nif[12:]}'
        return nif

    @classmethod
    def from_string(cls, nif_string: str) -> 'NIF':
        """
        Cria NIF a partir de uma string, removendo formatação.
        
        Args:
            nif_string: String contendo o NIF (pode conter hífens)
            
        Returns:
            Instância de NIF
            
        Raises:
            ValueError: Se o NIF for inválido
        """
        cleaned = nif_string.replace('-', '').replace(' ', '').strip()
        return cls(cleaned)

    @property
    def is_extended(self) -> bool:
        """Retorna True se o NIF é o formato estendido (14 dígitos)."""
        return len(self.value) == 14

    @property
    def is_simple(self) -> bool:
        """Retorna True se o NIF é o formato simples (9 dígitos)."""
        return len(self.value) == 9

    def is_valid_checksum(self) -> bool:
        """
        Valida o checksum do NIF angolano (se implementado).
        
        Futura funcionalidade para quando AGT evoluir validação.
        Por enquanto retorna True (validação futura).
        
        Returns:
            True se o checksum é válido, False caso contrário
        """
        return True