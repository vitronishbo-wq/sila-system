from __future__ import annotations
from dataclasses import dataclass
from datetime import date, datetime
from uuid import UUID, uuid4
from app.modules.civil_protection.domain.enums import PrioridadeAtendimento, StatusOcorrenciaEmergencial, TipoOcorrenciaEmergencial

@dataclass
class OcorrenciaEmergencial:
    id: UUID
    codigo_ocorrencia: str
    corporacao_id: UUID
    tipo: TipoOcorrenciaEmergencial
    status: StatusOcorrenciaEmergencial
    prioridade: PrioridadeAtendimento
    data_ocorrencia: datetime
    descricao: str
    municipio: str
    provincia: str
    data_registro: date
    bombeiro_responsavel_id: UUID | None = None
    endereco: str | None = None
    vitimas: int = 0
    desalojados: int = 0
    obitos: int = 0
    observacoes: str | None = None
    ativo: bool = True

    @classmethod
    def registrar(cls, *, codigo_ocorrencia: str, corporacao_id: UUID, tipo: TipoOcorrenciaEmergencial, prioridade: PrioridadeAtendimento, data_ocorrencia: datetime, descricao: str, municipio: str, provincia: str, bombeiro_responsavel_id: UUID | None=None, endereco: str | None=None, vitimas: int=0, desalojados: int=0, obitos: int=0, observacoes: str | None=None) -> 'OcorrenciaEmergencial':
        if len(descricao.strip()) < 5:
            raise ValueError('Descricao da ocorrencia deve ter pelo menos 5 caracteres')
        if data_ocorrencia > datetime.now():
            raise ValueError('Data da ocorrencia nao pode estar no futuro')
        if vitimas < 0 or desalojados < 0 or obitos < 0:
            raise ValueError('Quantidades nao podem ser negativas')
        return cls(id=uuid4(), codigo_ocorrencia=codigo_ocorrencia.strip(), corporacao_id=corporacao_id, tipo=tipo, status=StatusOcorrenciaEmergencial.RECEBIDA, prioridade=prioridade, data_ocorrencia=data_ocorrencia, descricao=descricao.strip(), municipio=municipio.strip(), provincia=provincia.strip(), data_registro=date.today(), bombeiro_responsavel_id=bombeiro_responsavel_id, endereco=endereco.strip() if endereco else None, vitimas=vitimas, desalojados=desalojados, obitos=obitos, observacoes=observacoes.strip() if observacoes else None, ativo=True)

    def atualizar_status(self, status: StatusOcorrenciaEmergencial, observacoes: str | None=None) -> None:
        self.status = status
        self.ativo = status not in {StatusOcorrenciaEmergencial.CANCELADA}
        if observacoes:
            self.observacoes = observacoes.strip()