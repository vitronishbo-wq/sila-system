from __future__ import annotations
from decimal import Decimal
from uuid import UUID
from apps.backend.app.modules.resources.pescas.application.ports import CitizenServicePort, EmbarcacaoRepositoryPort, RequestServicePort
from apps.backend.app.modules.resources.pescas.domain.enums import TipoEmbarcacao
from apps.backend.app.modules.resources.pescas.domain.models.embarcacao import Embarcacao

class EmbarcacaoService:

    def __init__(self, embarcacao_repo: EmbarcacaoRepositoryPort, citizen_service: CitizenServicePort, request_service: RequestServicePort):
        self.embarcacao_repo = embarcacao_repo
        self.citizen_service = citizen_service
        self.request_service = request_service

    async def cadastrar_embarcacao(self, *, nome: str, tipo: TipoEmbarcacao, comprimento: Decimal, arqueacao_bruta: Decimal, porto_registro: str, proprietario_id: UUID) -> Embarcacao:
        if not await self.citizen_service.is_citizen_active(proprietario_id):
            raise ValueError('Proprietario nao encontrado')
        numero_inscricao = await self.embarcacao_repo.next_inscricao(porto_registro)
        item = Embarcacao.cadastrar(nome=nome, numero_inscricao=numero_inscricao, tipo=tipo, comprimento=comprimento, arqueacao_bruta=arqueacao_bruta, porto_registro=porto_registro, proprietario_id=proprietario_id)
        saved = await self.embarcacao_repo.save(item)
        await self.request_service.create_request(request_type='CADASTRO_EMBARCACAO', entity_id=saved.id, citizen_id=proprietario_id, numero_processo=numero_inscricao, metadata={'nome': nome, 'tipo': tipo.value})
        return saved

    async def buscar_embarcacao(self, embarcacao_id: UUID) -> Embarcacao:
        item = await self.embarcacao_repo.get_by_id(embarcacao_id)
        if not item:
            raise ValueError('Embarcacao nao encontrada')
        return item

    async def listar_embarcacoes(self, proprietario_id: UUID) -> list[Embarcacao]:
        return await self.embarcacao_repo.list_by_proprietario(proprietario_id)