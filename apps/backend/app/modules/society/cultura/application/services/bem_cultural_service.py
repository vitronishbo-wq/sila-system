from __future__ import annotations
from decimal import Decimal
from uuid import UUID, uuid4
from apps.backend.app.modules.society.cultura.application.events import BemTombadoEvent, event_bus
from apps.backend.app.modules.society.cultura.application.ports.bem_cultural_repository_port import BemCulturalRepositoryPort
from apps.backend.app.modules.society.cultura.application.ports.request_service_port import RequestServicePort
from apps.backend.app.modules.society.cultura.domain.enums import StatusTombamento, TipoPatrimonio
from apps.backend.app.modules.society.cultura.domain.models.bem_cultural import BemCultural

class BemCulturalService:

    def __init__(self, *, bem_repo: BemCulturalRepositoryPort, request_service: RequestServicePort | None=None) -> None:
        self.bem_repo = bem_repo
        self.request_service = request_service

    async def cadastrar_bem(self, *, nome: str, tipo: TipoPatrimonio, descricao: str, localizacao: str, municipio: str, provincia: str, coordenadas_lat: Decimal | None=None, coordenadas_long: Decimal | None=None, observacoes: str | None=None) -> BemCultural:
        registro = await self.bem_repo.next_registro()
        bem = BemCultural.cadastrar(registro=registro, nome=nome, tipo=tipo, descricao=descricao, localizacao=localizacao, municipio=municipio, provincia=provincia, coordenadas_lat=coordenadas_lat, coordenadas_long=coordenadas_long, observacoes=observacoes)
        saved = await self.bem_repo.save(bem)
        if self.request_service is not None:
            await self.request_service.create_request(request_type='CADASTRO_BEM_CULTURAL', entity_id=saved.id, metadata={'registro_ipat': saved.registro_ipat, 'tipo': saved.tipo.value, 'municipio': saved.municipio}, numero_processo=saved.registro_ipat)
        return saved

    async def buscar_bem(self, bem_id: UUID) -> BemCultural:
        item = await self.bem_repo.get_by_id(bem_id)
        if item is None:
            raise ValueError('Bem cultural nao encontrado')
        return item

    async def listar_bens(self, *, tipo: TipoPatrimonio | None=None, municipio: str | None=None, status_tombamento: StatusTombamento | None=None, somente_ativos: bool=True) -> list[BemCultural]:
        if tipo is not None:
            itens = await self.bem_repo.list_by_tipo(tipo)
        elif municipio is not None:
            itens = await self.bem_repo.list_by_municipio(municipio)
        elif status_tombamento is not None:
            itens = await self.bem_repo.list_by_status_tombamento(status_tombamento)
        else:
            itens = await self.bem_repo.list_all()
        if somente_ativos:
            return [item for item in itens if item.ativo]
        return itens

    async def atualizar_bem(self, *, bem_id: UUID, nome: str | None=None, tipo: TipoPatrimonio | None=None, descricao: str | None=None, localizacao: str | None=None, municipio: str | None=None, provincia: str | None=None, coordenadas_lat: Decimal | None=None, coordenadas_long: Decimal | None=None, ativo: bool | None=None, observacoes: str | None=None) -> BemCultural:
        item = await self.buscar_bem(bem_id)
        item.atualizar(nome=nome, tipo=tipo, descricao=descricao, localizacao=localizacao, municipio=municipio, provincia=provincia, coordenadas_lat=coordenadas_lat, coordenadas_long=coordenadas_long, ativo=ativo, observacoes=observacoes)
        return await self.bem_repo.save(item)

    async def tombar_bem(self, bem_id: UUID) -> BemCultural:
        item = await self.buscar_bem(bem_id)
        if item.status_tombamento == StatusTombamento.TOMBADO:
            return item
        item.tombar(uuid4())
        saved = await self.bem_repo.save(item)
        await event_bus.publish(BemTombadoEvent(bem_id=saved.id, nome=saved.nome, tipo=saved.tipo.value, nivel_tombamento='MUNICIPAL'))
        return saved

    async def remover_bem(self, bem_id: UUID) -> None:
        deleted = await self.bem_repo.delete(bem_id)
        if not deleted:
            raise ValueError('Bem cultural nao encontrado')