"""Regimes fiscais."""
from enum import Enum


class TaxRegime(str, Enum):
    """Regimes fiscais suportados na Angola."""
    
    GERAL = "GERAL"  # Regime geral (IVA obrigatório)
    SIMPLIFICADO = "SIMPLIFICADO"  # Regime simplificado (pequenas empresas)
    ISENTO = "ISENTO"  # Isento de IVA
    ISENTO_BY_NATURE = "ISENTO_BY_NATURE"  # Atividades isentas por natureza
    IMPORTACAO = "IMPORTACAO"  # Regime especial de importação
    EXPORTACAO = "EXPORTACAO"  # Regime especial de exportação
    INTRA_UE = "INTRA_UE"  # Operações intra-comunitárias

    def requires_vat(self) -> bool:
        """Verifica se o regime obriga ao recolhimento de IVA."""
        requires = {
            self.GERAL,
            self.SIMPLIFICADO,
            self.IMPORTACAO,
            self.INTRA_UE,
        }
        return self in requires

    def is_simplified(self) -> bool:
        """Verifica se é regime simplificado."""
        return self == self.SIMPLIFICADO

    def is_exempt(self) -> bool:
        """Verifica se é regime isento."""
        exempt = {
            self.ISENTO,
            self.ISENTO_BY_NATURE,
        }
        return self in exempt

    def description_pt(self) -> str:
        """Descrição do regime em português."""
        descriptions = {
            "GERAL": "Regime Geral",
            "SIMPLIFICADO": "Regime Simplificado",
            "ISENTO": "Regime Isento",
            "ISENTO_BY_NATURE": "Atividades Isentas por Natureza",
            "IMPORTACAO": "Regime de Importação",
            "EXPORTACAO": "Regime de Exportação",
            "INTRA_UE": "Operações Intra-Comunitárias",
        }
        return descriptions.get(self.value, self.value)
