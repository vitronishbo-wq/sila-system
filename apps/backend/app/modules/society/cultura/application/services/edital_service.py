from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from uuid import UUID

from apps.backend.app.modules.society.cultura.application.events import (
    EditalPublicadoEvent,
    event_bus,
)
from apps.backend.app.modules.society.cultura.application.ports.edital_repository_port import (
    EditalRepositoryPort,
)
from apps.backend.app.modules.society.cultura.application.ports.projeto_cultural_repository_port import (
    ProjetoCulturalRepositoryPort,
)
from apps.backend.app.modules.society.cultura.application.ports.request_service_port import (
    RequestServicePort,
)
from apps.backend.app.modules.society.cultura.domain.enums import (
    FaseEditalCultural,
    StatusProjetoCultural,
    TipoEditalCultural,
)
from apps.backend.app.modules.society.cultura.domain.models.edital import Edital


class EditalService:
    def __init__(
        self,
        *,
        edital_repo: EditalRepositoryPort,
        projeto_repo: ProjetoCulturalRepositoryPort,
        request_service: RequestServicePort | None = None,
        minc_adapter=None,
        turismo_adapter=None,
    ) -> None:
        self.edital_repo = edital_repo
        self.projeto_repo = projeto_repo
        self.request_service = request_service
        self.minc_adapter = minc_adapter
        self.turismo_adapter = turismo_adapter

    async def publicar_edital(
        self,
        *,
        numero: str,
        titulo: str,
        tipo: TipoEditalCultural,
        orgao_responsavel_id: UUID,
        valor_total: Decimal,
        data_publicacao: datetime,
        data_inicio_inscricoes: datetime,
        data_fim_inscricoes: datetime,
        vagas: int,
        descricao: str,
        criterios: list[str],
        documentos_necessarios: list[str],
    ) -> Edital:
        existing = await self.edital_repo.get_by_numero(numero)
        if existing is not None:
            raise ValueError("Ja existe edital com este numero")
        edital = Edital.publicar(
            numero=numero,
            titulo=titulo,
            tipo=tipo,
            orgao_responsavel_id=orgao_responsavel_id,
            valor_total=valor_total,
            data_publicacao=data_publicacao,
            data_inicio_inscricoes=data_inicio_inscricoes,
            data_fim_inscricoes=data_fim_inscricoes,
            vagas=vagas,
            descricao=descricao,
            criterios=criterios,
            documentos_necessarios=documentos_necessarios,
        )
        saved = await self.edital_repo.save(edital)
        if self.request_service is not None:
            await self.request_service.create_request(
                request_type="PUBLICACAO_EDITAL_CULTURAL",
                entity_id=saved.id,
                numero_processo=saved.numero,
                metadata={"tipo": saved.tipo.value, "vagas": saved.vagas},
            )
        if self.minc_adapter is not None:
            await self.minc_adapter.publicar_edital(
                {
                    "id": str(saved.id),
                    "numero": saved.numero,
                    "titulo": saved.titulo,
                    "tipo": saved.tipo.value,
                    "valor_total": float(saved.valor_total),
                    "data_fim_inscricoes": saved.data_fim_inscricoes.isoformat(),
                }
            )
        if self.turismo_adapter is not None and saved.tipo.value in {"festival", "circulacao"}:
            await self.turismo_adapter.notificar_evento(
                {
                    "nome": saved.titulo,
                    "inicio": saved.data_inicio_inscricoes.isoformat(),
                    "fim": saved.data_fim_inscricoes.isoformat(),
                }
            )
        await event_bus.publish(
            EditalPublicadoEvent(
                edital_id=saved.id,
                numero=saved.numero,
                titulo=saved.titulo,
                tipo=saved.tipo.value,
                valor_total=float(saved.valor_total),
                data_fim_inscricoes=saved.data_fim_inscricoes.isoformat(),
            )
        )
        return saved

    async def buscar_edital(self, edital_id: UUID) -> Edital:
        item = await self.edital_repo.get_by_id(edital_id)
        if item is None:
            raise ValueError("Edital cultural nao encontrado")
        return item

    async def listar_editais(
        self,
        *,
        tipo: TipoEditalCultural | None = None,
        fase: FaseEditalCultural | None = None,
        data_inicio: datetime | None = None,
        data_fim: datetime | None = None,
        somente_ativos: bool = True,
    ) -> list[Edital]:
        if tipo is not None:
            items = await self.edital_repo.list_by_tipo(tipo)
        elif fase is not None:
            items = await self.edital_repo.list_by_fase(fase)
        elif data_inicio is not None and data_fim is not None:
            items = await self.edital_repo.list_by_periodo(data_inicio, data_fim)
        else:
            items = await self.edital_repo.list_all()
        if somente_ativos:
            return [item for item in items if item.ativo]
        return items

    async def abrir_inscricoes(self, edital_id: UUID) -> Edital:
        edital = await self.buscar_edital(edital_id)
        edital.abrir_inscricoes()
        return await self.edital_repo.save(edital)

    async def encerrar_inscricoes(self, edital_id: UUID) -> Edital:
        edital = await self.buscar_edital(edital_id)
        edital.encerrar_inscricoes()
        return await self.edital_repo.save(edital)

    async def inscrever_projeto(self, *, edital_id: UUID, projeto_id: UUID) -> Edital:
        edital = await self.buscar_edital(edital_id)
        projeto = await self.projeto_repo.get_by_id(projeto_id)
        if projeto is None:
            raise ValueError("Projeto cultural nao encontrado")
        edital.adicionar_inscricao(projeto.id)
        if projeto.status == StatusProjetoCultural.RASCUNHO:
            projeto.submeter()
            await self.projeto_repo.save(projeto)
        return await self.edital_repo.save(edital)

    async def selecionar_projetos(self, *, edital_id: UUID, projetos_ids: list[UUID]) -> Edital:
        edital = await self.buscar_edital(edital_id)
        projetos = []
        total_aprovado = Decimal("0")
        for projeto_id in projetos_ids:
            projeto = await self.projeto_repo.get_by_id(projeto_id)
            if projeto is None:
                raise ValueError(f"Projeto cultural nao encontrado: {projeto_id}")
            projetos.append(projeto)
            total_aprovado += projeto.valor_solicitado
        if total_aprovado > edital.valor_disponivel:
            raise ValueError("Valor total selecionado excede valor disponivel do edital")
        edital.publicar_resultado_final([projeto.id for projeto in projetos])
        edital.valor_disponivel -= total_aprovado
        saved_edital = await self.edital_repo.save(edital)
        for projeto in projetos:
            projeto.aprovar(valor_aprovado=projeto.valor_solicitado)
            await self.projeto_repo.save(projeto)
        return saved_edital

    async def remover_edital(self, edital_id: UUID) -> None:
        deleted = await self.edital_repo.delete(edital_id)
        if not deleted:
            raise ValueError("Edital cultural nao encontrado")
