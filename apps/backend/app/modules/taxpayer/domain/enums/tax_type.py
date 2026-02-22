"""Enums para tipos de imposto."""
from enum import Enum


class TaxType(str, Enum):
    """Tipos de impostos suportados na Angola."""
    
    IRS = "IRS"  # Imposto sobre o Rendimento de Pessoas Singulares
    IVA = "IVA"  # Imposto sobre o Valor Acrescentado
    IRC = "IRC"  # Imposto sobre o Rendimento de Pessoas Coletivas
    IPCA = "IPCA"  # Imposto Pessoal de Circulação Automóvel
    ISENÇÃO = "ISENÇÃO"  # Isenção fiscal

    def description_pt(self) -> str:
        """Descrição do tipo de imposto em português."""
        descriptions = {
            "IRS": "Imposto sobre o Rendimento de Pessoas Singulares",
            "IVA": "Imposto sobre o Valor Acrescentado",
            "IRC": "Imposto sobre o Rendimento de Pessoas Coletivas",
            "IPCA": "Imposto Pessoal de Circulação Automóvel",
            "ISENÇÃO": "Isenção Fiscal",
        }
        return descriptions.get(self.value, self.value)
