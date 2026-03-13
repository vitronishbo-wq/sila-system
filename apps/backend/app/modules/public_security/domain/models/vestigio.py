from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID, uuid4
from app.modules.public_security.domain.enums import StatusVestigio, TipoVestigio

@dataclass
class Vestigio:
    id: UUID
    codigo_vestigio: str
    cadeia_custodia_id: UUID
    ocorrencia_id: UUID
    tipo: TipoVestigio
    descricao: str
    localizacao: str
    data_coleta: datetime
    status: StatusVestigio
    coletado_por_id: UUID | None = None
    observacoes: str | None = None
    ativo: bool = True

    @classmethod
    def registrar(cls, *, codigo_vestigio: str, cadeia_custodia_id: UUID, ocorrencia_id: UUID, tipo: TipoVestigio, descricao: str, localizacao: str, coletado_por_id: UUID | None=None, observacoes: str | None=None) -> 'Vestigio':
        if len(descricao.strip()) < 5:
            raise ValueError('Descricao do vestigio deve ter pelo menos 5 caracteres')
        if len(localizacao.strip()) < 3:
            raise ValueError('Localizacao do vestigio deve ter pelo menos 3 caracteres')
        return cls(id=uuid4(), codigo_vestigio=codigo_vestigio.strip(), cadeia_custodia_id=cadeia_custodia_id, ocorrencia_id=ocorrencia_id, tipo=tipo, descricao=descricao.strip(), localizacao=localizacao.strip(), data_coleta=datetime.utcnow(), status=StatusVestigio.COLETADO, coletado_por_id=coletado_por_id, observacoes=observacoes.strip() if observacoes else None, ativo=True)

    def atualizar_status(self, status: StatusVestigio, observacoes: str | None=None) -> None:
        self.status = status
        self.ativo = status is not StatusVestigio.DESCARTADO
        if observacoes:
            self.observacoes = observacoes.strip()