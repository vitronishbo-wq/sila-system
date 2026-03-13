from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from typing import Optional
from uuid import UUID, uuid4
from apps.backend.app.modules.resources.pecuaria.domain.enums import StatusPecuarista

@dataclass
class Pecuarista:
    id: UUID
    cadastro_pecuarista: str
    nome: str
    documento: str
    documento_tipo: str
    data_cadastro: date
    status: StatusPecuarista
    telefone: Optional[str] = None
    email: Optional[str] = None
    endereco: Optional[str] = None
    citizen_id: Optional[UUID] = None
    empresa_id: Optional[UUID] = None
    observacoes: Optional[str] = None

    @classmethod
    def criar(cls, *, nome: str, documento: str, documento_tipo: str, telefone: Optional[str]=None, email: Optional[str]=None, endereco: Optional[str]=None, citizen_id: Optional[UUID]=None, empresa_id: Optional[UUID]=None, observacoes: Optional[str]=None) -> 'Pecuarista':
        return cls(id=uuid4(), cadastro_pecuarista='', nome=nome, documento=documento, documento_tipo=documento_tipo, data_cadastro=date.today(), status=StatusPecuarista.PENDENTE, telefone=telefone, email=email, endereco=endereco, citizen_id=citizen_id, empresa_id=empresa_id, observacoes=observacoes)

    def ativar(self) -> None:
        if self.status != StatusPecuarista.PENDENTE:
            raise ValueError('Apenas pecuaristas pendentes podem ser ativados')
        self.status = StatusPecuarista.ATIVO

    def suspender(self, motivo: str) -> None:
        if self.status != StatusPecuarista.ATIVO:
            raise ValueError('Apenas pecuaristas ativos podem ser suspensos')
        self.status = StatusPecuarista.SUSPENSO
        self.observacoes = motivo