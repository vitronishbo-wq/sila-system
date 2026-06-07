from __future__ import annotations

from datetime import date
from uuid import UUID

from apps.backend.app.modules.society.desporto.application.events import (
    EventBus,
    JogoAgendadoEvent,
    JogoResultadoRegistradoEvent,
)
from apps.backend.app.modules.society.desporto.application.ports.clube_repository_port import (
    ClubeRepositoryPort,
)
from apps.backend.app.modules.society.desporto.application.ports.competicao_repository_port import (
    CompeticaoRepositoryPort,
)
from apps.backend.app.modules.society.desporto.application.ports.jogo_repository_port import (
    JogoRepositoryPort,
)
from apps.backend.app.modules.society.desporto.application.ports.obras_publicas_service_port import (
    ObrasPublicasServicePort,
)
from apps.backend.app.modules.society.desporto.application.ports.outbox_repository_port import (
    OutboxRepositoryPort,
)
from apps.backend.app.modules.society.desporto.application.ports.request_service_port import (
    RequestServicePort,
)
from apps.backend.app.modules.society.desporto.application.ports.turismo_service_port import (
    TurismoServicePort,
)
from apps.backend.app.modules.society.desporto.domain.enums import StatusJogo
from apps.backend.app.modules.society.desporto.domain.models.jogo import Jogo


class JogoService:
    def __init__(
        self,
        *,
        jogo_repo: JogoRepositoryPort,
        competicao_repo: CompeticaoRepositoryPort,
        clube_repo: ClubeRepositoryPort,
        turismo_service: TurismoServicePort | None = None,
        obras_publicas_service: ObrasPublicasServicePort | None = None,
        request_service: RequestServicePort | None = None,
        event_bus: EventBus | None = None,
        outbox_repo: OutboxRepositoryPort | None = None,
    ) -> None:
        self.jogo_repo = jogo_repo
        self.competicao_repo = competicao_repo
        self.clube_repo = clube_repo
        self.turismo_service = turismo_service
        self.obras_publicas_service = obras_publicas_service
        self.request_service = request_service
        self.event_bus = event_bus
        self.outbox_repo = outbox_repo

    async def agendar_jogo(
        self,
        *,
        competicao_id: UUID,
        clube_casa_id: UUID,
        clube_fora_id: UUID,
        data_jogo: date,
        local: str,
        municipio: str,
        provincia: str,
        codigo_obra_instalacao: str | None = None,
        atracao_turistica_id: UUID | None = None,
        publico_estimado: int | None = None,
        observacoes: str | None = None,
    ) -> Jogo:
        await self._validar_integracoes(
            competicao_id=competicao_id,
            clube_casa_id=clube_casa_id,
            clube_fora_id=clube_fora_id,
            codigo_obra_instalacao=codigo_obra_instalacao,
            atracao_turistica_id=atracao_turistica_id,
        )
        codigo = await self.jogo_repo.next_codigo()
        jogo = Jogo.agendar(
            codigo_jogo=codigo,
            competicao_id=competicao_id,
            clube_casa_id=clube_casa_id,
            clube_fora_id=clube_fora_id,
            data_jogo=data_jogo,
            local=local,
            municipio=municipio,
            provincia=provincia,
            codigo_obra_instalacao=codigo_obra_instalacao,
            atracao_turistica_id=atracao_turistica_id,
            publico_estimado=publico_estimado,
            observacoes=observacoes,
        )
        saved = await self.jogo_repo.save(jogo)
        if self.request_service is not None:
            await self.request_service.create_request(
                request_type="AGENDAMENTO_JOGO",
                entity_id=saved.id,
                metadata={
                    "codigo": saved.codigo_jogo,
                    "competicao_id": str(saved.competicao_id),
                    "clube_casa_id": str(saved.clube_casa_id),
                    "clube_fora_id": str(saved.clube_fora_id),
                },
                numero_processo=saved.codigo_jogo,
            )
        event = JogoAgendadoEvent(
            jogo_id=saved.id,
            codigo_jogo=saved.codigo_jogo,
            competicao_id=saved.competicao_id,
            clube_casa_id=saved.clube_casa_id,
            clube_fora_id=saved.clube_fora_id,
            data_jogo=saved.data_jogo.isoformat(),
        )
        if self.outbox_repo is not None:
            await self.outbox_repo.append(event)
        if self.event_bus is not None:
            await self.event_bus.publish(event)
        return saved

    async def buscar_jogo(self, jogo_id: UUID) -> Jogo:
        item = await self.jogo_repo.get_by_id(jogo_id)
        if item is None:
            raise ValueError("Jogo nao encontrado")
        return item

    async def listar_jogos(
        self,
        *,
        competicao_id: UUID | None = None,
        clube_id: UUID | None = None,
        status: StatusJogo | None = None,
        data_inicio: date | None = None,
        data_fim: date | None = None,
        somente_ativos: bool = True,
    ) -> list[Jogo]:
        if data_inicio is not None and data_fim is not None:
            itens = await self.jogo_repo.list_by_periodo(data_inicio, data_fim)
        elif competicao_id is not None:
            itens = await self.jogo_repo.list_by_competicao(competicao_id)
        elif clube_id is not None:
            itens = await self.jogo_repo.list_by_clube(clube_id)
        elif status is not None:
            itens = await self.jogo_repo.list_by_status(status)
        else:
            itens = await self.jogo_repo.list_all()
        if somente_ativos:
            return [item for item in itens if item.ativo]
        return itens

    async def atualizar_jogo(
        self,
        *,
        jogo_id: UUID,
        data_jogo: date | None = None,
        local: str | None = None,
        municipio: str | None = None,
        provincia: str | None = None,
        status: StatusJogo | None = None,
        codigo_obra_instalacao: str | None = None,
        atracao_turistica_id: UUID | None = None,
        publico_estimado: int | None = None,
        publico_presente: int | None = None,
        ativo: bool | None = None,
        observacoes: str | None = None,
    ) -> Jogo:
        item = await self.buscar_jogo(jogo_id)
        await self._validar_integracoes(
            competicao_id=item.competicao_id,
            clube_casa_id=item.clube_casa_id,
            clube_fora_id=item.clube_fora_id,
            codigo_obra_instalacao=codigo_obra_instalacao,
            atracao_turistica_id=atracao_turistica_id,
        )
        item.atualizar(
            data_jogo=data_jogo,
            local=local,
            municipio=municipio,
            provincia=provincia,
            status=status,
            codigo_obra_instalacao=codigo_obra_instalacao,
            atracao_turistica_id=atracao_turistica_id,
            publico_estimado=publico_estimado,
            publico_presente=publico_presente,
            ativo=ativo,
            observacoes=observacoes,
        )
        return await self.jogo_repo.save(item)

    async def registrar_resultado(
        self, *, jogo_id: UUID, placar_casa: int, placar_fora: int
    ) -> Jogo:
        item = await self.buscar_jogo(jogo_id)
        item.registrar_resultado(placar_casa=placar_casa, placar_fora=placar_fora)
        saved = await self.jogo_repo.save(item)
        event = JogoResultadoRegistradoEvent(
            jogo_id=saved.id,
            codigo_jogo=saved.codigo_jogo,
            placar_casa=placar_casa,
            placar_fora=placar_fora,
            status=saved.status.value,
        )
        if self.outbox_repo is not None:
            await self.outbox_repo.append(event)
        if self.event_bus is not None:
            await self.event_bus.publish(event)
        return saved

    async def remover_jogo(self, jogo_id: UUID) -> None:
        deleted = await self.jogo_repo.delete(jogo_id)
        if not deleted:
            raise ValueError("Jogo nao encontrado")

    async def _validar_integracoes(
        self,
        *,
        competicao_id: UUID,
        clube_casa_id: UUID,
        clube_fora_id: UUID,
        codigo_obra_instalacao: str | None,
        atracao_turistica_id: UUID | None,
    ) -> None:
        competicao = await self.competicao_repo.get_by_id(competicao_id)
        if competicao is None:
            raise ValueError("Competicao informada nao encontrada")
        clube_casa = await self.clube_repo.get_by_id(clube_casa_id)
        if clube_casa is None:
            raise ValueError("Clube casa informado nao encontrado")
        clube_fora = await self.clube_repo.get_by_id(clube_fora_id)
        if clube_fora is None:
            raise ValueError("Clube fora informado nao encontrado")
        if codigo_obra_instalacao and self.obras_publicas_service is not None:
            obra_ok = await self.obras_publicas_service.obra_exists(codigo_obra_instalacao)
            if not obra_ok:
                raise ValueError("Obra de instalacao informada nao encontrada")
        if atracao_turistica_id is not None and self.turismo_service is not None:
            atracao_ok = await self.turismo_service.atracao_exists(atracao_turistica_id)
            if not atracao_ok:
                raise ValueError("Atracao turistica informada nao encontrada")
