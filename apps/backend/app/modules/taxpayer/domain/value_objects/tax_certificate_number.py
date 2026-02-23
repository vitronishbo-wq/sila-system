"""TaxCertificateNumber Value Object - Número de Certidão Fiscal"""
from dataclasses import dataclass
import re


@dataclass(frozen=True)
class TaxCertificateNumber:
    """
    Value Object para números de certidão fiscal.
    
    Formato: CERT-TIPO-ANO-SEQUENCIA
    Exemplo: CERT-REGULAR-2024-0001234
    
    Tipos de certidão:
    - REGULAR: Certidão de regularidade fiscal
    - NEGATIVA: Certidão de dívida não existente
    - ESPECIAL: Certidão especial (para fins específicos)
    """
    value: str
    certificate_type: str  # REGULAR, NEGATIVA, ESPECIAL
    year: int

    def __post_init__(self) -> None:
        """Valida o número de certidão."""
        if not self._is_valid(self.value):
            raise ValueError(f"Número de certidão inválido: {self.value}")
        
        # Validar coerência
        parts = self.value.split("-")
        if parts[1] != self.certificate_type:
            raise ValueError(
                f"Tipo de certidão não corresponde: "
                f"{parts[1]} vs {self.certificate_type}"
            )
        
        if int(parts[2]) != self.year:
            raise ValueError(
                f"Ano não corresponde: {parts[2]} vs {self.year}"
            )

    @staticmethod
    def _is_valid(value: str) -> bool:
        """
        Valida formato do número de certidão.
        
        Formato esperado: CERT-TIPO-YYYY-NNNNNN
        """
        if not value:
            return False
        
        pattern = r"^CERT-(REGULAR|NEGATIVA|ESPECIAL)-\d{4}-\d{6,10}$"
        return bool(re.match(pattern, value.strip()))

    @classmethod
    def generate(
        cls,
        certificate_type: str,
        year: int,
        sequence: int
    ) -> "TaxCertificateNumber":
        """
        Gera um novo número de certidão.
        
        Args:
            certificate_type: Tipo de certidão (REGULAR, NEGATIVA, ESPECIAL)
            year: Ano da certidão
            sequence: Número sequencial
            
        Returns:
            Instância de TaxCertificateNumber
        """
        valid_types = ["REGULAR", "NEGATIVA", "ESPECIAL"]
        if certificate_type not in valid_types:
            raise ValueError(
                f"Tipo de certidão inválido: {certificate_type}. "
                f"Use um dos: {', '.join(valid_types)}"
            )
        
        if year < 1990 or year > 2100:
            raise ValueError(f"Ano inválido: {year}")
        
        if sequence < 1:
            raise ValueError("Sequência deve ser maior que 0")
        
        # Formatar com até 10 dígitos
        sequence_str = str(sequence).zfill(10)[-10:]
        value = f"CERT-{certificate_type}-{year}-{sequence_str}"
        return cls(value=value, certificate_type=certificate_type, year=year)

    def __str__(self) -> str:
        """Retorna valor formatado."""
        return self.value

    def __repr__(self) -> str:
        """Representação para debug."""
        return f"TaxCertificateNumber({self.value})"

    @property
    def sequence(self) -> int:
        """Extrai o número sequencial."""
        return int(self.value.split("-")[3])

    @property
    def is_regular(self) -> bool:
        """Retorna True se é certificado regular."""
        return self.certificate_type == "REGULAR"

    @property
    def is_debt_free(self) -> bool:
        """Retorna True se é certidão de dívida não existente."""
        return self.certificate_type == "NEGATIVA"

    @property
    def is_special(self) -> bool:
        """Retorna True se é certidão especial."""
        return self.certificate_type == "ESPECIAL"

    def format_display(self) -> str:
        """Retorna formatado para exibição."""
        parts = self.value.split("-")
        type_name = {
            "REGULAR": "Regularidade",
            "NEGATIVA": "Dívida Não Existente",
            "ESPECIAL": "Especial"
        }
        return (
            f"{type_name.get(self.certificate_type, self.certificate_type)} "
            f"- {parts[2]} #{parts[3].lstrip('0') or '0'}"
        )

    def description_pt(self) -> str:
        """Retorna descrição em português."""
        descriptions = {
            "REGULAR": "Certidão de Regularidade Fiscal",
            "NEGATIVA": "Certidão de Dívida Não Existente",
            "ESPECIAL": "Certidão Especial"
        }
        return descriptions.get(
            self.certificate_type,
            f"Certidão {self.certificate_type}"
        )
