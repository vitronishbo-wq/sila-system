"""TaxDeclarationNumber Value Object - Número de Declaração Fiscal"""

import re
from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class TaxDeclarationNumber:
    """
    Value Object para números de declaração fiscal.

    Formato: TIPO-ANO-SEQUENCIA
    Exemplo: IRS-2024-0001234

    Onde:
    - TIPO: IRS, IVA, IRC, etc (2-3 caracteres)
    - ANO: Ano da declaração (4 dígitos)
    - SEQUENCIA: Número sequencial (6-10 dígitos)
    """

    value: str
    tax_type: str
    year: int

    def __post_init__(self) -> None:
        """Valida o número de declaração."""
        if not self._is_valid(self.value):
            raise ValueError(f"Número de declaração inválido: {self.value}")
        parts = self.value.split("-")
        if parts[0] != self.tax_type:
            raise ValueError(f"Tipo de imposto não corresponde: {parts[0]} vs {self.tax_type}")
        if int(parts[1]) != self.year:
            raise ValueError(f"Ano não corresponde: {parts[1]} vs {self.year}")

    @staticmethod
    def _is_valid(value: str) -> bool:
        """
        Valida formato do número de declaração.

        Formato esperado: TIPO-YYYY-NNNNNN
        """
        if not value:
            return False
        pattern = "^[A-Z]{2,3}-\\d{4}-\\d{6,10}$"
        return bool(re.match(pattern, value.strip()))

    @classmethod
    def generate(cls, tax_type: str, year: int, sequence: int) -> "TaxDeclarationNumber":
        """
        Gera um novo número de declaração.

        Args:
            tax_type: Tipo de imposto (ex: IRS, IVA, IRC)
            year: Ano da declaração
            sequence: Número sequencial (será zerado �\xa0 esquerda)

        Returns:
            Instância de TaxDeclarationNumber
        """
        if not re.match("^[A-Z]{2,3}$", tax_type):
            raise ValueError(f"Tipo de imposto inválido: {tax_type}")
        if year < 1990 or year > 2100:
            raise ValueError(f"Ano inválido: {year}")
        if sequence < 1:
            raise ValueError("Sequência deve ser maior que 0")
        sequence_str = str(sequence).zfill(10)[-10:]
        value = f"{tax_type}-{year}-{sequence_str}"
        return cls(value=value, tax_type=tax_type, year=year)

    @classmethod
    def from_uuid_and_tax_type(cls, tax_type: str, year: int) -> "TaxDeclarationNumber":
        """
        Gera número usando UUID como base para sequência.

        Args:
            tax_type: Tipo de imposto
            year: Ano da declaração

        Returns:
            Instância de TaxDeclarationNumber
        """
        uuid_value = UUID(int=0).int % 1000000000
        return cls.generate(tax_type, year, uuid_value)

    def __str__(self) -> str:
        """Retorna valor formatado."""
        return self.value

    def __repr__(self) -> str:
        """Representação para debug."""
        return f"TaxDeclarationNumber({self.value})"

    @property
    def sequence(self) -> int:
        """Extrai o número sequencial."""
        return int(self.value.split("-")[2])

    def format_display(self) -> str:
        """Retorna formatado para exibição."""
        parts = self.value.split("-")
        return f"{parts[0]} {parts[1]} #{parts[2].lstrip('0') or '0'}"
