from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from uuid import UUID, uuid4
from app.modules.civil_protection.domain.enums import StatusCorporacao

@dataclass
class Corporacao:
    id: UUID
    codigo_corporacao: str
    nome: str
    municipio: str
    provincia: str
    endereco: str
    comandante: str
    data_ativacao: date
    status: StatusCorporacao = StatusCorporacao.ATIVA
    telefone: str | None = None
    email: str | None = None
    observacoes: str | None = None
    ativo: bool = True

    @classmethod
    def cadastrar(cls, *, codigo_corporacao: str, nome: str, municipio: str, provincia: str, endereco: str, comandante: str, telefone: str | None=None, email: str | None=None, observacoes: str | None=None) -> 'Corporacao':
        if len(nome.strip()) < 3:
            raise ValueError('Nome da corporacao deve ter pelo menos 3 caracteres')
        if len(comandante.strip()) < 3:
            raise ValueError('Comandante deve ter pelo menos 3 caracteres')
        return cls(id=uuid4(), codigo_corporacao=codigo_corporacao.strip(), nome=nome.strip(), municipio=municipio.strip(), provincia=provincia.strip(), endereco=endereco.strip(), comandante=comandante.strip(), data_ativacao=date.today(), status=StatusCorporacao.ATIVA, telefone=telefone.strip() if telefone else None, email=email.strip().lower() if email else None, observacoes=observacoes.strip() if observacoes else None, ativo=True)

    def atualizar_status(self, status: StatusCorporacao, motivo: str | None=None) -> None:
        self.status = status
        self.ativo = status not in {StatusCorporacao.DESATIVADA}
        if motivo:
            self.observacoes = motivo.strip()