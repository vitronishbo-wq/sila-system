from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from uuid import UUID, uuid4
from apps.backend.app.modules.society.juventude.domain.enums import AreaInteresse, StatusEstagio

@dataclass
class EstagioJuvenil:
    id: UUID
    codigo_estagio: str
    jovem_id: UUID
    instituicao: str
    area_interesse: AreaInteresse
    cargo: str
    carga_horaria_semanal: int
    data_inicio: date
    data_cadastro: date
    status: StatusEstagio = StatusEstagio.PLANEADO
    bolsa_auxilio: Decimal | None = None
    data_fim: date | None = None
    observacoes: str | None = None
    ativo: bool = True

    @classmethod
    def registrar(cls, *, codigo_estagio: str, jovem_id: UUID, instituicao: str, area_interesse: AreaInteresse, cargo: str, carga_horaria_semanal: int, data_inicio: date, bolsa_auxilio: Decimal | None=None, data_fim: date | None=None, observacoes: str | None=None) -> 'EstagioJuvenil':
        if len(instituicao.strip()) < 3:
            raise ValueError('Instituicao do estagio deve ter pelo menos 3 caracteres')
        if len(cargo.strip()) < 2:
            raise ValueError('Cargo do estagio deve ter pelo menos 2 caracteres')
        if carga_horaria_semanal <= 0:
            raise ValueError('Carga horaria semanal deve ser maior que zero')
        if bolsa_auxilio is not None and bolsa_auxilio < 0:
            raise ValueError('Bolsa auxilio nao pode ser negativa')
        if data_fim is not None and data_fim < data_inicio:
            raise ValueError('Data fim do estagio deve ser maior ou igual a data inicio')
        return cls(id=uuid4(), codigo_estagio=codigo_estagio.strip(), jovem_id=jovem_id, instituicao=instituicao.strip(), area_interesse=area_interesse, cargo=cargo.strip(), carga_horaria_semanal=carga_horaria_semanal, data_inicio=data_inicio, data_fim=data_fim, bolsa_auxilio=bolsa_auxilio, data_cadastro=date.today(), observacoes=observacoes.strip() if observacoes else None, status=StatusEstagio.PLANEADO, ativo=True)

    def atualizar_status(self, status: StatusEstagio) -> None:
        self.status = status
        self.ativo = status not in {StatusEstagio.CANCELADO, StatusEstagio.CONCLUIDO}
        if status == StatusEstagio.CONCLUIDO and self.data_fim is None:
            self.data_fim = date.today()