from __future__ import annotations

from datetime import date
from uuid import UUID

from apps.backend.app.modules.governance.cooperacao_internacional.application.events import (
    VistoAprovadoEvent,
    event_bus,
)
from apps.backend.app.modules.governance.cooperacao_internacional.application.ports.visto_repository_port import (
    VistoRepositoryPort,
)
from apps.backend.app.modules.governance.cooperacao_internacional.domain.enums import (
    CategoriaVisto,
    TipoVisto,
)
from apps.backend.app.modules.governance.cooperacao_internacional.domain.models.visto import Visto
from apps.backend.app.modules.governance.cooperacao_internacional.infrastructure.persistence.outbox import (
    InMemoryOutbox,
)


class VistoService:
    def __init__(self, *, visto_repo: VistoRepositoryPort, outbox: InMemoryOutbox) -> None:
        self.visto_repo = visto_repo
        self.outbox = outbox

    async def solicitar_visto(
        self,
        *,
        tipo: TipoVisto,
        categoria: CategoriaVisto,
        solicitante_cpf: str,
        solicitante_nome: str,
        solicitante_passaporte: str,
        pais_origem_id: UUID,
        pais_destino_id: UUID,
        data_entrada_prevista: date,
        data_saida_prevista: date,
        objetivo_viagem: str,
        consulato_emissor_id: UUID,
    ) -> Visto:
        visto = Visto(
            tipo=tipo,
            categoria=categoria,
            solicitante_cpf=solicitante_cpf,
            solicitante_nome=solicitante_nome,
            solicitante_passaporte=solicitante_passaporte,
            pais_origem_id=pais_origem_id,
            pais_destino_id=pais_destino_id,
            data_entrada_prevista=data_entrada_prevista,
            data_saida_prevista=data_saida_prevista,
            objetivo_viagem=objetivo_viagem,
            consulato_emissor_id=consulato_emissor_id,
        )
        await self.visto_repo.save(visto)
        return visto

    async def analisar_visto(
        self, *, visto_id: UUID, analista: str, resultado: str, justificativa: str | None = None
    ) -> Visto:
        visto = await self.visto_repo.get_by_id(visto_id)
        if visto is None:
            raise ValueError("Visto nao encontrado")
        visto.analisar(analista=analista, resultado=resultado, justificativa=justificativa)
        await self.visto_repo.save(visto)
        return visto

    async def aprovar_visto(
        self, *, visto_id: UUID, autoridade: str, validade_dias: int = 90
    ) -> Visto:
        visto = await self.visto_repo.get_by_id(visto_id)
        if visto is None:
            raise ValueError("Visto nao encontrado")
        visto.aprovar(autoridade=autoridade, validade_dias=validade_dias)
        await self.visto_repo.save(visto)
        evento = VistoAprovadoEvent(
            visto_id=visto.id,
            numero_processo=visto.numero_processo,
            solicitante_cpf=visto.solicitante_cpf,
            tipo=visto.tipo.value,
            data_validade=visto.data_validade.isoformat() if visto.data_validade else "",
        )
        await self.outbox.append(evento)
        await event_bus.publish(evento)
        return visto

    async def emitir_visto(self, *, visto_id: UUID) -> Visto:
        visto = await self.visto_repo.get_by_id(visto_id)
        if visto is None:
            raise ValueError("Visto nao encontrado")
        visto.emitir()
        await self.visto_repo.save(visto)
        return visto

    async def negar_visto(self, *, visto_id: UUID, motivo: str) -> Visto:
        visto = await self.visto_repo.get_by_id(visto_id)
        if visto is None:
            raise ValueError("Visto nao encontrado")
        visto.negar(motivo=motivo)
        await self.visto_repo.save(visto)
        return visto

    async def listar_vistos(self) -> list[Visto]:
        return await self.visto_repo.list_all()
