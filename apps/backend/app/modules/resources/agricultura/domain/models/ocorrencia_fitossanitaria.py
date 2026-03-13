from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID, uuid4
from app.modules.resources.agricultura.domain.enums import SeveridadeOcorrencia, StatusOcorrencia

@dataclass
class OcorrenciaFitossanitaria:
    id: UUID
    codigo_ocorrencia: str
    codigo_propriedade: str
    praga_doenca: str
    descricao: str
    severidade: SeveridadeOcorrencia
    status: StatusOcorrencia
    data_registro: datetime
    cultura_afetada: str | None = None
    acao_recomendada: str | None = None
    data_resolucao: datetime | None = None

    @classmethod
    def registrar(cls, *, codigo_propriedade: str, praga_doenca: str, descricao: str, severidade: SeveridadeOcorrencia, cultura_afetada: str | None=None, acao_recomendada: str | None=None) -> 'OcorrenciaFitossanitaria':
        return cls(id=uuid4(), codigo_ocorrencia='', codigo_propriedade=codigo_propriedade, praga_doenca=praga_doenca, descricao=descricao, severidade=severidade, status=StatusOcorrencia.ABERTA, data_registro=datetime.utcnow(), cultura_afetada=cultura_afetada, acao_recomendada=acao_recomendada)

    def iniciar_tratamento(self) -> None:
        if self.status == StatusOcorrencia.RESOLVIDA:
            raise ValueError('Ocorrencia ja resolvida')
        self.status = StatusOcorrencia.EM_TRATAMENTO

    def resolver(self) -> None:
        if self.status == StatusOcorrencia.RESOLVIDA:
            raise ValueError('Ocorrencia ja resolvida')
        self.status = StatusOcorrencia.RESOLVIDA
        self.data_resolucao = datetime.utcnow()