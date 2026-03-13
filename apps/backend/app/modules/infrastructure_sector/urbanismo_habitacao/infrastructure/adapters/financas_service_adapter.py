from __future__ import annotations
from decimal import Decimal
from uuid import UUID
from app.modules.infrastructure_sector.urbanismo_habitacao.application.ports.financas_service_port import FinancasServicePort
from app.modules.infrastructure_sector.urbanismo_habitacao.domain.enums import TipoAlvara

class FinancasServiceAdapter(FinancasServicePort):

    async def calcular_taxa_loteamento(self, *, area_total: Decimal, quantidade_lotes: int) -> Decimal:
        base = area_total * Decimal('0.0005')
        adicional = Decimal(quantidade_lotes) * Decimal('5.00')
        return (base + adicional).quantize(Decimal('0.01'))

    async def calcular_taxa_licenciamento(self, *, tipo_alvara: TipoAlvara, area_construida_prevista: Decimal | None) -> Decimal:
        fator_tipo = {TipoAlvara.CONSTRUCAO: Decimal('1.00'), TipoAlvara.REFORMA: Decimal('0.70'), TipoAlvara.AMPLIACAO: Decimal('0.85'), TipoAlvara.DEMOLICAO: Decimal('0.50'), TipoAlvara.FUNCIONAMENTO: Decimal('0.40'), TipoAlvara.LOCALIZACAO: Decimal('0.35')}[tipo_alvara]
        area = area_construida_prevista or Decimal('0')
        return (Decimal('1500.00') + area * fator_tipo * Decimal('0.20')).quantize(Decimal('0.01'))

    async def registrar_cobranca(self, *, referencia_id: UUID, descricao: str, valor: Decimal) -> str:
        _ = (referencia_id, descricao, valor)
        return f'COB-{str(referencia_id)[:8].upper()}'