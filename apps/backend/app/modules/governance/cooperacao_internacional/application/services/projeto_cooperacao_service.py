from __future__ import annotations

from datetime import date
from uuid import UUID

from apps.backend.app.modules.governance.cooperacao_internacional.application.events import (
    ProjetoCooperacaoAprovadoEvent,
    event_bus,
)
from apps.backend.app.modules.governance.cooperacao_internacional.application.ports.projeto_repository_port import (
    ProjetoCooperacaoRepositoryPort,
)
from apps.backend.app.modules.governance.cooperacao_internacional.domain.enums import (
    ModalidadeCooperacao,
    TipoProjeto,
)
from apps.backend.app.modules.governance.cooperacao_internacional.domain.models.projeto_cooperacao import (
    ProjetoCooperacao,
)
from apps.backend.app.modules.governance.cooperacao_internacional.infrastructure.persistence.outbox import (
    InMemoryOutbox,
)


class ProjetoCooperacaoService:
    def __init__(
        self, *, projeto_repo: ProjetoCooperacaoRepositoryPort, outbox: InMemoryOutbox
    ) -> None:
        self.projeto_repo = projeto_repo
        self.outbox = outbox

    async def criar_projeto(
        self,
        *,
        titulo: str,
        tipo: TipoProjeto,
        modalidade: ModalidadeCooperacao,
        orgao_responsavel_id: UUID,
        orgao_parceiro_id: UUID,
        pais_parceiro_id: UUID,
        data_inicio: date,
        data_fim: date,
        objetivo_geral: str,
        objetivos_especificos: list[str],
        orcamento_total: float,
        fonte_recursos: str,
        acordo_base_id: UUID | None = None,
    ) -> ProjetoCooperacao:
        projeto = ProjetoCooperacao(
            titulo=titulo,
            tipo=tipo,
            modalidade=modalidade,
            acordo_base_id=acordo_base_id,
            orgao_responsavel_id=orgao_responsavel_id,
            orgao_parceiro_id=orgao_parceiro_id,
            pais_parceiro_id=pais_parceiro_id,
            data_inicio=data_inicio,
            data_fim=data_fim,
            objetivo_geral=objetivo_geral,
            objetivos_especificos=objetivos_especificos,
            orcamento_total=orcamento_total,
            fonte_recursos=fonte_recursos,
        )
        await self.projeto_repo.save(projeto)
        return projeto

    async def aprovar_projeto(self, *, projeto_id: UUID) -> ProjetoCooperacao:
        projeto = await self.projeto_repo.get_by_id(projeto_id)
        if projeto is None:
            raise ValueError("Projeto nao encontrado")
        projeto.aprovar()
        await self.projeto_repo.save(projeto)
        evento = ProjetoCooperacaoAprovadoEvent(
            projeto_id=projeto.id,
            codigo_projeto=projeto.codigo_projeto,
            titulo=projeto.titulo,
            pais_parceiro_id=projeto.pais_parceiro_id,
            orcamento_total=projeto.orcamento_total,
        )
        await self.outbox.append(evento)
        await event_bus.publish(evento)
        return projeto

    async def iniciar_execucao(self, *, projeto_id: UUID) -> ProjetoCooperacao:
        projeto = await self.projeto_repo.get_by_id(projeto_id)
        if projeto is None:
            raise ValueError("Projeto nao encontrado")
        projeto.iniciar_execucao()
        await self.projeto_repo.save(projeto)
        return projeto

    async def listar_projetos(self) -> list[ProjetoCooperacao]:
        return await self.projeto_repo.list_all()
