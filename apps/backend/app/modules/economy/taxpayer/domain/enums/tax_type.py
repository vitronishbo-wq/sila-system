"""Enums para tipos de imposto."""

from enum import StrEnum


class TaxType(StrEnum):
    """Tipos de impostos suportados na Angola."""

    IRS = "IRS"
    IVA = "IVA"
    IRC = "IRC"
    IPCA = "IPCA"
    ISENÇÃO = "ISENÇÃO"

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
