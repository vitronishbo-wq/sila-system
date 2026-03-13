from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from uuid import UUID, uuid4
from apps.backend.app.modules.public_security.domain.enums import CargoPolicial, Patente, StatusAgente, TipoAgente, TipoVinculo

@dataclass
class Policial:
    id: UUID
    matricula: str
    unidade_id: UUID
    nome: str
    data_nascimento: date
    cpf: str
    rg: str
    tipo: TipoAgente
    vinculo: TipoVinculo
    data_ingresso: date
    cargo: CargoPolicial | None = None
    patente: Patente | None = None
    status: StatusAgente = StatusAgente.ATIVO
    porte_arma: bool = False
    numero_porte: str | None = None
    data_validade_porte: date | None = None
    telefone: str | None = None
    email: str | None = None
    endereco: str | None = None
    observacoes: str | None = None
    ativo: bool = True

    @classmethod
    def cadastrar(cls, *, matricula: str, unidade_id: UUID, nome: str, data_nascimento: date, cpf: str, rg: str, tipo: TipoAgente, vinculo: TipoVinculo, cargo: CargoPolicial | None=None, patente: Patente | None=None, telefone: str | None=None, email: str | None=None, endereco: str | None=None, observacoes: str | None=None) -> 'Policial':
        if len(nome.strip()) < 3:
            raise ValueError('Nome do policial deve ter pelo menos 3 caracteres')
        return cls(id=uuid4(), matricula=matricula.strip(), unidade_id=unidade_id, nome=nome.strip(), data_nascimento=data_nascimento, cpf=cpf.strip(), rg=rg.strip(), tipo=tipo, vinculo=vinculo, data_ingresso=date.today(), cargo=cargo, patente=patente, status=StatusAgente.ATIVO, porte_arma=False, numero_porte=None, data_validade_porte=None, telefone=telefone.strip() if telefone else None, email=email.strip().lower() if email else None, endereco=endereco.strip() if endereco else None, observacoes=observacoes.strip() if observacoes else None, ativo=True)

    def atualizar_status(self, status: StatusAgente, motivo: str | None=None) -> None:
        self.status = status
        self.ativo = status not in {StatusAgente.APOSENTADO, StatusAgente.EXONERADO}
        if motivo:
            self.observacoes = motivo.strip()

    def ativar_porte(self, *, numero_porte: str, data_validade: date) -> None:
        if data_validade < date.today():
            raise ValueError('Data de validade do porte nao pode ser no passado')
        self.porte_arma = True
        self.numero_porte = numero_porte.strip()
        self.data_validade_porte = data_validade