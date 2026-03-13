from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from typing import Optional
from uuid import UUID, uuid4
from app.modules.society.seguranca_social.domain.enums import EstadoBeneficiario, RegimeSegurancaSocial, TipoBeneficiario

@dataclass
class Beneficiario:
    id: UUID
    numero_beneficiario: str
    citizen_id: UUID
    data_inscricao: date
    tipo: TipoBeneficiario
    regime: RegimeSegurancaSocial
    estado: EstadoBeneficiario
    data_ativacao: Optional[date] = None
    data_suspensao: Optional[date] = None
    data_cancelamento: Optional[date] = None
    motivo_cancelamento: Optional[str] = None
    observacoes: Optional[str] = None

    @classmethod
    def criar(cls, *, citizen_id: UUID, tipo: TipoBeneficiario, regime: RegimeSegurancaSocial, numero_beneficiario: str) -> 'Beneficiario':
        return cls(id=uuid4(), numero_beneficiario=numero_beneficiario, citizen_id=citizen_id, data_inscricao=date.today(), tipo=tipo, regime=regime, estado=EstadoBeneficiario.PENDENTE)

    def ativar(self) -> None:
        if self.estado != EstadoBeneficiario.PENDENTE:
            raise ValueError('Apenas beneficiarios pendentes podem ser ativados')
        self.estado = EstadoBeneficiario.ATIVO
        self.data_ativacao = date.today()

    def suspender(self, motivo: str) -> None:
        if self.estado != EstadoBeneficiario.ATIVO:
            raise ValueError('Apenas beneficiarios ativos podem ser suspensos')
        self.estado = EstadoBeneficiario.SUSPENSO
        self.data_suspensao = date.today()
        self.observacoes = motivo

    def cancelar(self, motivo: str) -> None:
        if self.estado == EstadoBeneficiario.CANCELADO:
            raise ValueError('Beneficiario ja esta cancelado')
        self.estado = EstadoBeneficiario.CANCELADO
        self.data_cancelamento = date.today()
        self.motivo_cancelamento = motivo