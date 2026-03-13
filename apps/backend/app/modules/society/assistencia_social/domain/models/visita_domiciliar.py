from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID, uuid4
from app.modules.society.assistencia_social.domain.enums import ResultadoVisita

@dataclass
class VisitaDomiciliar:
    id: UUID
    codigo: str
    beneficiario_id: UUID
    assistente_social_id: UUID
    data_visita: datetime
    condicoes_moradia: str
    observacoes: str | None
    recomendacoes: list[str]
    resultado: ResultadoVisita

    @classmethod
    def registrar(cls, *, codigo: str, beneficiario_id: UUID, assistente_social_id: UUID, condicoes_moradia: str, observacoes: str | None=None, recomendacoes: list[str] | None=None, resultado: ResultadoVisita=ResultadoVisita.RETORNO_NECESSARIO) -> 'VisitaDomiciliar':
        return cls(id=uuid4(), codigo=codigo, beneficiario_id=beneficiario_id, assistente_social_id=assistente_social_id, data_visita=datetime.utcnow(), condicoes_moradia=condicoes_moradia, observacoes=observacoes, recomendacoes=recomendacoes or [], resultado=resultado)