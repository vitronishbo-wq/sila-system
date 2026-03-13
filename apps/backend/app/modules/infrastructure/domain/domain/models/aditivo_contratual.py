from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from uuid import UUID, uuid4
from app.modules.infrastructure.domain.enums import TipoAditivo

@dataclass
class AditivoContratual:
    id: UUID
    tipo: TipoAditivo
    justificativa: str
    data_assinatura: date
    valor_aditivo: Decimal = Decimal('0')
    prazo_adicional_dias: int = 0

    @classmethod
    def registrar(cls, *, tipo: TipoAditivo, justificativa: str, valor_aditivo: Decimal=Decimal('0'), prazo_adicional_dias: int=0, data_assinatura: date | None=None) -> 'AditivoContratual':
        if not justificativa.strip():
            raise ValueError('Justificativa do aditivo e obrigatoria')
        if valor_aditivo < Decimal('0'):
            raise ValueError('Valor de aditivo nao pode ser negativo')
        if prazo_adicional_dias < 0:
            raise ValueError('Prazo adicional nao pode ser negativo')
        if tipo in {TipoAditivo.PRAZO, TipoAditivo.AMBOS} and prazo_adicional_dias == 0:
            raise ValueError('Aditivo de prazo exige dias adicionais')
        if tipo in {TipoAditivo.VALOR, TipoAditivo.AMBOS} and valor_aditivo == Decimal('0'):
            raise ValueError('Aditivo de valor exige valor adicional')
        return cls(id=uuid4(), tipo=tipo, justificativa=justificativa.strip(), data_assinatura=data_assinatura or date.today(), valor_aditivo=valor_aditivo.quantize(Decimal('0.01')), prazo_adicional_dias=prazo_adicional_dias)

    def to_dict(self) -> dict:
        return {'id': str(self.id), 'tipo': self.tipo.value, 'justificativa': self.justificativa, 'data_assinatura': self.data_assinatura.isoformat(), 'valor_aditivo': str(self.valor_aditivo), 'prazo_adicional_dias': self.prazo_adicional_dias}
