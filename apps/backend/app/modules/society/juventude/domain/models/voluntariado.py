from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from uuid import UUID, uuid4
from apps.backend.app.modules.society.juventude.domain.enums import AreaInteresse, StatusVoluntariado

@dataclass
class Voluntariado:
    id: UUID
    codigo_voluntariado: str
    jovem_id: UUID
    organizacao: str
    causa: AreaInteresse
    carga_horaria_total: int
    data_inicio: date
    data_cadastro: date
    status: StatusVoluntariado = StatusVoluntariado.INSCRITO
    data_fim: date | None = None
    observacoes: str | None = None
    ativo: bool = True

    @classmethod
    def iniciar(cls, *, codigo_voluntariado: str, jovem_id: UUID, organizacao: str, causa: AreaInteresse, carga_horaria_total: int, data_inicio: date, data_fim: date | None=None, observacoes: str | None=None) -> 'Voluntariado':
        if len(organizacao.strip()) < 3:
            raise ValueError('Organizacao do voluntariado deve ter pelo menos 3 caracteres')
        if carga_horaria_total <= 0:
            raise ValueError('Carga horaria total deve ser maior que zero')
        if data_fim is not None and data_fim < data_inicio:
            raise ValueError('Data fim do voluntariado deve ser maior ou igual a data inicio')
        return cls(id=uuid4(), codigo_voluntariado=codigo_voluntariado.strip(), jovem_id=jovem_id, organizacao=organizacao.strip(), causa=causa, carga_horaria_total=carga_horaria_total, data_inicio=data_inicio, data_fim=data_fim, data_cadastro=date.today(), observacoes=observacoes.strip() if observacoes else None, status=StatusVoluntariado.INSCRITO, ativo=True)

    def atualizar_status(self, status: StatusVoluntariado) -> None:
        self.status = status
        self.ativo = status not in {StatusVoluntariado.CANCELADO, StatusVoluntariado.CONCLUIDO}
        if status == StatusVoluntariado.CONCLUIDO and self.data_fim is None:
            self.data_fim = date.today()