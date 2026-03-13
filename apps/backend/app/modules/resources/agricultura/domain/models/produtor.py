from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from typing import Optional
from uuid import UUID, uuid4
from app.modules.resources.agricultura.domain.enums import StatusProdutor, TipoProdutor

@dataclass
class Produtor:
    id: UUID
    cadastro_produtor: str
    tipo: TipoProdutor
    status: StatusProdutor
    nome: str
    documento: str
    documento_tipo: str
    data_cadastro: date
    telefone: Optional[str] = None
    email: Optional[str] = None
    endereco: Optional[str] = None
    citizen_id: Optional[UUID] = None
    empresa_id: Optional[UUID] = None
    familiar: bool = False
    observacoes: Optional[str] = None

    @classmethod
    def criar(cls, *, nome: str, documento: str, documento_tipo: str, tipo: TipoProdutor, citizen_id: Optional[UUID]=None, empresa_id: Optional[UUID]=None, telefone: Optional[str]=None, email: Optional[str]=None, endereco: Optional[str]=None, observacoes: Optional[str]=None) -> 'Produtor':
        return cls(id=uuid4(), cadastro_produtor='', tipo=tipo, status=StatusProdutor.PENDENTE, nome=nome, documento=documento, documento_tipo=documento_tipo, data_cadastro=date.today(), telefone=telefone, email=email, endereco=endereco, citizen_id=citizen_id, empresa_id=empresa_id, familiar=tipo == TipoProdutor.FAMILIAR, observacoes=observacoes)

    def ativar(self) -> None:
        if self.status != StatusProdutor.PENDENTE:
            raise ValueError('Apenas produtores pendentes podem ser ativados')
        self.status = StatusProdutor.ATIVO

    def suspender(self, motivo: str) -> None:
        if self.status != StatusProdutor.ATIVO:
            raise ValueError('Apenas produtores ativos podem ser suspensos')
        self.status = StatusProdutor.SUSPENSO
        self.observacoes = motivo