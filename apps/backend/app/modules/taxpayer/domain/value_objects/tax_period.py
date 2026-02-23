"""TaxPeriod Value Object - Período Fiscal"""
from dataclasses import dataclass
from datetime import date
import re
from typing import Optional


@dataclass(frozen=True)
class TaxPeriod:
    """
    Value Object para períodos fiscais.
    
    Formatos suportados:
    - YYYY: Ano completo (ex: 2024)
    - YYYY-QX: Trimestre (ex: 2024-Q1, 2024-Q2, 2024-Q3, 2024-Q4)
    - YYYY-MX: Mês (ex: 2024-M01, 2024-M12)
    - YYYY-SX: Semestre (ex: 2024-S1, 2024-S2)
    """
    value: str
    period_type: str  # "YEAR", "QUARTER", "MONTH", "SEMESTER"

    def __post_init__(self) -> None:
        """Valida o período fiscal."""
        if not self._is_valid(self.value, self.period_type):
            raise ValueError(
                f"Período fiscal inválido: {self.value} "
                f"(tipo: {self.period_type})"
            )

    @staticmethod
    def _is_valid(value: str, period_type: str) -> bool:
        """Valida formato do período."""
        if not value or not period_type:
            return False

        value = value.strip().upper()

        validators = {
            "YEAR": lambda v: re.match(r"^\d{4}$", v),
            "QUARTER": lambda v: re.match(r"^\d{4}-Q[1-4]$", v),
            "MONTH": lambda v: re.match(r"^\d{4}-M(0[1-9]|1[0-2])$", v),
            "SEMESTER": lambda v: re.match(r"^\d{4}-S[1-2]$", v),
        }

        validator = validators.get(period_type)
        return bool(validator(value)) if validator else False

    @classmethod
    def from_year(cls, year: int) -> "TaxPeriod":
        """Cria período para um ano completo."""
        if year < 1900 or year > 2100:
            raise ValueError(f"Ano inválido: {year}")
        return cls(value=str(year), period_type="YEAR")

    @classmethod
    def from_quarter(cls, year: int, quarter: int) -> "TaxPeriod":
        """Cria período para um trimestre."""
        if quarter not in [1, 2, 3, 4]:
            raise ValueError(f"Trimestre inválido: {quarter}")
        value = f"{year}-Q{quarter}"
        return cls(value=value, period_type="QUARTER")

    @classmethod
    def from_month(cls, year: int, month: int) -> "TaxPeriod":
        """Cria período para um mês."""
        if month < 1 or month > 12:
            raise ValueError(f"Mês inválido: {month}")
        value = f"{year}-M{month:02d}"
        return cls(value=value, period_type="MONTH")

    @classmethod
    def from_semester(cls, year: int, semester: int) -> "TaxPeriod":
        """Cria período para um semestre."""
        if semester not in [1, 2]:
            raise ValueError(f"Semestre inválido: {semester}")
        value = f"{year}-S{semester}"
        return cls(value=value, period_type="SEMESTER")

    @classmethod
    def from_date(cls, date_obj: date) -> "TaxPeriod":
        """Cria período de um ano a partir de uma data."""
        return cls.from_year(date_obj.year)

    def __str__(self) -> str:
        """Retorna valor do período."""
        return self.value

    def __repr__(self) -> str:
        """Representação para debug."""
        return f"TaxPeriod({self.value}, {self.period_type})"

    @property
    def year(self) -> int:
        """Extrai o ano do período."""
        return int(self.value.split("-")[0])

    @property
    def is_year(self) -> bool:
        """Retorna True se é período anual."""
        return self.period_type == "YEAR"

    @property
    def is_quarter(self) -> bool:
        """Retorna True se é período trimestral."""
        return self.period_type == "QUARTER"

    @property
    def is_month(self) -> bool:
        """Retorna True se é período mensal."""
        return self.period_type == "MONTH"

    @property
    def is_semester(self) -> bool:
        """Retorna True se é período semestral."""
        return self.period_type == "SEMESTER"

    def get_quarter(self) -> Optional[int]:
        """Retorna o trimestre (1-4) se aplicável."""
        if self.is_quarter:
            return int(self.value.split("-Q")[1])
        return None

    def get_month(self) -> Optional[int]:
        """Retorna o mês (1-12) se aplicável."""
        if self.is_month:
            return int(self.value.split("-M")[1])
        return None

    def get_semester(self) -> Optional[int]:
        """Retorna o semestre (1-2) se aplicável."""
        if self.is_semester:
            return int(self.value.split("-S")[1])
        return None

    def display_pt(self) -> str:
        """Retorna descrição em português."""
        if self.is_year:
            return f"{self.year}"
        elif self.is_quarter:
            quarter = self.get_quarter()
            return f"{self.year} - Q{quarter}"
        elif self.is_month:
            month = self.get_month()
            month_names = {
                1: "Jan", 2: "Fev", 3: "Mar", 4: "Abr",
                5: "Mai", 6: "Jun", 7: "Jul", 8: "Ago",
                9: "Set", 10: "Out", 11: "Nov", 12: "Dez"
            }
            return f"{month_names.get(month, '')} {self.year}"
        elif self.is_semester:
            semester = self.get_semester()
            return f"{self.year} - S{semester}"
        return self.value
