from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from uuid import UUID, uuid4

from apps.backend.app.modules.public_security.domain.enums import (
    PrioridadeOcorrencia,
    StatusOcorrencia,
    TipoOcorrencia,
)


@dataclass
class Ocorrencia:
    id: UUID
    codigo_ocorrencia: str
    unidade_id: UUID
    tipo: TipoOcorrencia
    status: StatusOcorrencia
    prioridade: PrioridadeOcorrencia
    data_ocorrencia: datetime
    descricao: str
    municipio: str
    provincia: str
    data_registro: date
    policial_responsavel_id: UUID | None = None
    endereco: str | None = None
    vitimas: int = 0
    suspeitos: int = 0
    preso_em_flagrante: bool = False
    observacoes: str | None = None
    ativo: bool = True

    @classmethod
    def registrar(
        cls,
        *,
        codigo_ocorrencia: str,
        unidade_id: UUID,
        tipo: TipoOcorrencia,
        prioridade: PrioridadeOcorrencia,
        data_ocorrencia: datetime,
        descricao: str,
        municipio: str,
        provincia: str,
        policial_responsavel_id: UUID | None = None,
        endereco: str | None = None,
        vitimas: int = 0,
        suspeitos: int = 0,
        preso_em_flagrante: bool = False,
        observacoes: str | None = None,
    ) -> Ocorrencia:
        if len(descricao.strip()) < 5:
            raise ValueError("Descricao da ocorrencia deve ter pelo menos 5 caracteres")
        if data_ocorrencia > datetime.now():
            raise ValueError("Data da ocorrencia nao pode estar no futuro")
        if vitimas < 0 or suspeitos < 0:
            raise ValueError("Vitimas e suspeitos nao podem ser negativos")
        return cls(
            id=uuid4(),
            codigo_ocorrencia=codigo_ocorrencia.strip(),
            unidade_id=unidade_id,
            tipo=tipo,
            status=StatusOcorrencia.REGISTRADA,
            prioridade=prioridade,
            data_ocorrencia=data_ocorrencia,
            descricao=descricao.strip(),
            municipio=municipio.strip(),
            provincia=provincia.strip(),
            data_registro=date.today(),
            policial_responsavel_id=policial_responsavel_id,
            endereco=endereco.strip() if endereco else None,
            vitimas=vitimas,
            suspeitos=suspeitos,
            preso_em_flagrante=preso_em_flagrante,
            observacoes=observacoes.strip() if observacoes else None,
            ativo=True,
        )

    def atualizar_status(self, status: StatusOcorrencia, observacoes: str | None = None) -> None:
        self.status = status
        self.ativo = status not in {StatusOcorrencia.ARQUIVADA}
        if observacoes:
            self.observacoes = observacoes.strip()
