from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from uuid import UUID, uuid4
from apps.backend.app.modules.public_security.domain.enums import StatusMandado, TipoMandado

@dataclass
class Mandado:
    id: UUID
    numero_mandado: str
    ocorrencia_id: UUID
    tipo: TipoMandado
    autoridade_judicial: str
    data_expedicao: date
    data_validade: date
    status: StatusMandado
    unidade_id: UUID | None = None
    policial_responsavel_id: UUID | None = None
    observacoes: str | None = None
    ativo: bool = True

    @classmethod
    def expedir(cls, *, numero_mandado: str, ocorrencia_id: UUID, tipo: TipoMandado, autoridade_judicial: str, data_expedicao: date, data_validade: date, unidade_id: UUID | None=None, policial_responsavel_id: UUID | None=None, observacoes: str | None=None) -> 'Mandado':
        if data_validade < data_expedicao:
            raise ValueError('Data de validade do mandado deve ser maior ou igual a expedicao')
        if len(autoridade_judicial.strip()) < 3:
            raise ValueError('Autoridade judicial deve ter pelo menos 3 caracteres')
        return cls(id=uuid4(), numero_mandado=numero_mandado.strip(), ocorrencia_id=ocorrencia_id, tipo=tipo, autoridade_judicial=autoridade_judicial.strip(), data_expedicao=data_expedicao, data_validade=data_validade, status=StatusMandado.EXPEDIDO, unidade_id=unidade_id, policial_responsavel_id=policial_responsavel_id, observacoes=observacoes.strip() if observacoes else None, ativo=True)

    def atualizar_status(self, status: StatusMandado, observacoes: str | None=None) -> None:
        self.status = status
        self.ativo = status not in {StatusMandado.CANCELADO, StatusMandado.VENCIDO}
        if observacoes:
            self.observacoes = observacoes.strip()