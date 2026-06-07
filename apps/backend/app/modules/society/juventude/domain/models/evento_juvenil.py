from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from uuid import UUID, uuid4

from apps.backend.app.modules.society.juventude.domain.enums import (
    AreaInteresse,
    StatusEvento,
    TipoEvento,
)


@dataclass
class EventoJuvenil:
    id: UUID
    codigo_evento: str
    titulo: str
    tipo_evento: TipoEvento
    area_interesse: AreaInteresse
    data_evento: date
    local: str
    municipio: str
    provincia: str
    data_cadastro: date
    vagas: int | None = None
    participantes: list[UUID] | None = None
    status: StatusEvento = StatusEvento.PLANEADO
    observacoes: str | None = None
    ativo: bool = True

    @classmethod
    def criar(
        cls,
        *,
        codigo_evento: str,
        titulo: str,
        tipo_evento: TipoEvento,
        area_interesse: AreaInteresse,
        data_evento: date,
        local: str,
        municipio: str,
        provincia: str,
        vagas: int | None = None,
        observacoes: str | None = None,
    ) -> EventoJuvenil:
        if len(titulo.strip()) < 3:
            raise ValueError("Titulo do evento deve ter pelo menos 3 caracteres")
        if len(local.strip()) < 3:
            raise ValueError("Local do evento deve ter pelo menos 3 caracteres")
        if vagas is not None and vagas <= 0:
            raise ValueError("Vagas do evento devem ser maiores que zero")
        return cls(
            id=uuid4(),
            codigo_evento=codigo_evento.strip(),
            titulo=titulo.strip(),
            tipo_evento=tipo_evento,
            area_interesse=area_interesse,
            data_evento=data_evento,
            local=local.strip(),
            municipio=municipio.strip(),
            provincia=provincia.strip(),
            vagas=vagas,
            data_cadastro=date.today(),
            observacoes=observacoes.strip() if observacoes else None,
            status=StatusEvento.PLANEADO,
            ativo=True,
        )

    def abrir_inscricoes(self) -> None:
        self.status = StatusEvento.INSCRICOES_ABERTAS

    def registrar_participante(self, jovem_id: UUID) -> None:
        if self.participantes is None:
            self.participantes = []
        if jovem_id in self.participantes:
            return
        if self.vagas is not None and len(self.participantes) >= self.vagas:
            raise ValueError("Evento sem vagas disponiveis")
        self.participantes.append(jovem_id)

    def concluir(self) -> None:
        self.status = StatusEvento.CONCLUIDO
        self.ativo = False
