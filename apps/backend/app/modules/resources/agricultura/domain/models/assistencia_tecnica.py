from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from uuid import UUID, uuid4

from apps.backend.app.modules.resources.agricultura.domain.enums import StatusAssistencia


@dataclass
class AssistenciaTecnica:
    id: UUID
    codigo_assistencia: str
    codigo_propriedade: str
    tecnico_nome: str
    objetivo: str
    status: StatusAssistencia
    data_agendamento: date
    data_realizacao: date | None = None
    recomendacoes: str | None = None
    motivo_cancelamento: str | None = None

    @classmethod
    def agendar(
        cls, *, codigo_propriedade: str, tecnico_nome: str, objetivo: str
    ) -> AssistenciaTecnica:
        return cls(
            id=uuid4(),
            codigo_assistencia="",
            codigo_propriedade=codigo_propriedade,
            tecnico_nome=tecnico_nome,
            objetivo=objetivo,
            status=StatusAssistencia.AGENDADA,
            data_agendamento=date.today(),
        )

    def concluir(self, recomendacoes: str | None = None) -> None:
        if self.status != StatusAssistencia.AGENDADA:
            raise ValueError("Somente assistencia agendada pode ser concluida")
        self.status = StatusAssistencia.REALIZADA
        self.data_realizacao = date.today()
        self.recomendacoes = recomendacoes

    def cancelar(self, motivo: str) -> None:
        if self.status != StatusAssistencia.AGENDADA:
            raise ValueError("Somente assistencia agendada pode ser cancelada")
        self.status = StatusAssistencia.CANCELADA
        self.motivo_cancelamento = motivo
