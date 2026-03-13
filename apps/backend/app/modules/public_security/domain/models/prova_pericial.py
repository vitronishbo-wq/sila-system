from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from uuid import UUID, uuid4
from apps.backend.app.modules.public_security.domain.enums import StatusProva, TipoProva

@dataclass
class ProvaPericial:
    id: UUID
    codigo_prova: str
    ocorrencia_id: UUID
    tipo: TipoProva
    descricao: str
    data_coleta: date
    local_coleta: str
    status: StatusProva
    coletado_por_id: UUID | None = None
    cadeia_custodia_id: UUID | None = None
    observacoes: str | None = None
    ativo: bool = True

    @classmethod
    def coletar(cls, *, codigo_prova: str, ocorrencia_id: UUID, tipo: TipoProva, descricao: str, local_coleta: str, data_coleta: date | None=None, coletado_por_id: UUID | None=None, observacoes: str | None=None) -> 'ProvaPericial':
        if len(descricao.strip()) < 5:
            raise ValueError('Descricao da prova deve ter pelo menos 5 caracteres')
        return cls(id=uuid4(), codigo_prova=codigo_prova.strip(), ocorrencia_id=ocorrencia_id, tipo=tipo, descricao=descricao.strip(), data_coleta=data_coleta or date.today(), local_coleta=local_coleta.strip(), status=StatusProva.COLETADA, coletado_por_id=coletado_por_id, cadeia_custodia_id=None, observacoes=observacoes.strip() if observacoes else None, ativo=True)

    def atualizar_status(self, status: StatusProva, observacoes: str | None=None) -> None:
        self.status = status
        self.ativo = status not in {StatusProva.DESCARTADA}
        if observacoes:
            self.observacoes = observacoes.strip()

    def vincular_cadeia_custodia(self, cadeia_custodia_id: UUID) -> None:
        self.cadeia_custodia_id = cadeia_custodia_id