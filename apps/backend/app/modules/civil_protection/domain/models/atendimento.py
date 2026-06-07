from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID, uuid4

from apps.backend.app.modules.civil_protection.domain.enums import StatusAtendimento


@dataclass
class Atendimento:
    id: UUID
    codigo_atendimento: str
    despacho_id: UUID
    ocorrencia_id: UUID
    status: StatusAtendimento
    inicio_atendimento: datetime
    local_atendimento: str
    fim_atendimento: datetime | None = None
    resumo: str | None = None
    vitimas_atendidas: int = 0
    desalojados_atendidos: int = 0
    obitos_confirmados: int = 0
    equipe_responsavel_id: UUID | None = None
    observacoes: str | None = None
    ativo: bool = True

    @classmethod
    def iniciar(
        cls,
        *,
        codigo_atendimento: str,
        despacho_id: UUID,
        ocorrencia_id: UUID,
        local_atendimento: str,
        vitimas_atendidas: int = 0,
        desalojados_atendidos: int = 0,
        obitos_confirmados: int = 0,
        equipe_responsavel_id: UUID | None = None,
        observacoes: str | None = None,
    ) -> Atendimento:
        if len(local_atendimento.strip()) < 3:
            raise ValueError("Local de atendimento deve ter pelo menos 3 caracteres")
        if vitimas_atendidas < 0 or desalojados_atendidos < 0 or obitos_confirmados < 0:
            raise ValueError("Quantidades nao podem ser negativas")
        return cls(
            id=uuid4(),
            codigo_atendimento=codigo_atendimento.strip(),
            despacho_id=despacho_id,
            ocorrencia_id=ocorrencia_id,
            status=StatusAtendimento.INICIADO,
            inicio_atendimento=datetime.now(),
            local_atendimento=local_atendimento.strip(),
            vitimas_atendidas=vitimas_atendidas,
            desalojados_atendidos=desalojados_atendidos,
            obitos_confirmados=obitos_confirmados,
            equipe_responsavel_id=equipe_responsavel_id,
            observacoes=observacoes.strip() if observacoes else None,
            ativo=True,
        )

    def atualizar_status(self, status: StatusAtendimento, observacoes: str | None = None) -> None:
        self.status = status
        self.ativo = status not in {StatusAtendimento.CANCELADO}
        if observacoes:
            self.observacoes = observacoes.strip()
        if status == StatusAtendimento.FINALIZADO and self.fim_atendimento is None:
            self.fim_atendimento = datetime.now()

    def finalizar(self, resumo: str | None = None, observacoes: str | None = None) -> None:
        self.status = StatusAtendimento.FINALIZADO
        self.fim_atendimento = datetime.now()
        if resumo:
            self.resumo = resumo.strip()
        if observacoes:
            self.observacoes = observacoes.strip()
