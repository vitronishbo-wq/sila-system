from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from uuid import UUID, uuid4
from app.modules.civil_protection.domain.enums import CargoBombeiro, StatusAgenteProtecao, TipoAgenteProtecao

@dataclass
class Bombeiro:
    id: UUID
    matricula: str
    corporacao_id: UUID
    nome: str
    data_nascimento: date
    cpf: str
    rg: str
    tipo: TipoAgenteProtecao
    data_ingresso: date
    cargo: CargoBombeiro | None = None
    status: StatusAgenteProtecao = StatusAgenteProtecao.ATIVO
    telefone: str | None = None
    email: str | None = None
    endereco: str | None = None
    observacoes: str | None = None
    ativo: bool = True

    @classmethod
    def cadastrar(cls, *, matricula: str, corporacao_id: UUID, nome: str, data_nascimento: date, cpf: str, rg: str, cargo: CargoBombeiro | None=None, telefone: str | None=None, email: str | None=None, endereco: str | None=None, observacoes: str | None=None) -> 'Bombeiro':
        if len(nome.strip()) < 3:
            raise ValueError('Nome do bombeiro deve ter pelo menos 3 caracteres')
        return cls(id=uuid4(), matricula=matricula.strip(), corporacao_id=corporacao_id, nome=nome.strip(), data_nascimento=data_nascimento, cpf=cpf.strip(), rg=rg.strip(), tipo=TipoAgenteProtecao.BOMBEIRO, data_ingresso=date.today(), cargo=cargo, status=StatusAgenteProtecao.ATIVO, telefone=telefone.strip() if telefone else None, email=email.strip().lower() if email else None, endereco=endereco.strip() if endereco else None, observacoes=observacoes.strip() if observacoes else None, ativo=True)

    def atualizar_status(self, status: StatusAgenteProtecao, motivo: str | None=None) -> None:
        self.status = status
        self.ativo = status not in {StatusAgenteProtecao.APOSENTADO, StatusAgenteProtecao.DESLIGADO}
        if motivo:
            self.observacoes = motivo.strip()