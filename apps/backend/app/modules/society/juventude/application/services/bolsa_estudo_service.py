from __future__ import annotations
from datetime import date
from decimal import Decimal
from uuid import UUID
from apps.backend.app.modules.society.juventude.application.ports.bolsa_estudo_repository_port import BolsaEstudoRepositoryPort
from apps.backend.app.modules.society.juventude.application.ports.jovem_repository_port import JovemRepositoryPort
from apps.backend.app.modules.society.juventude.application.ports.request_service_port import RequestServicePort
from apps.backend.app.modules.society.juventude.domain.enums import TipoBolsa
from apps.backend.app.modules.society.juventude.domain.models.bolsa_estudo import BolsaEstudo

class BolsaEstudoService:

    def __init__(self, *, bolsa_repo: BolsaEstudoRepositoryPort, jovem_repo: JovemRepositoryPort, request_service: RequestServicePort | None=None) -> None:
        self.bolsa_repo = bolsa_repo
        self.jovem_repo = jovem_repo
        self.request_service = request_service

    async def conceder_bolsa(self, *, jovem_id: UUID, tipo: TipoBolsa, valor_mensal: Decimal, data_inicio: date, data_fim: date | None=None, observacoes: str | None=None) -> BolsaEstudo:
        jovem = await self.jovem_repo.get_by_id(jovem_id)
        if jovem is None:
            raise ValueError('Jovem nao encontrado para concessao de bolsa')
        codigo = await self.bolsa_repo.next_codigo()
        bolsa = BolsaEstudo.conceder(codigo_bolsa=codigo, jovem_id=jovem_id, tipo=tipo, valor_mensal=valor_mensal, data_inicio=data_inicio, data_fim=data_fim, observacoes=observacoes)
        saved = await self.bolsa_repo.save(bolsa)
        if self.request_service is not None:
            await self.request_service.create_request(request_type='CONCESSAO_BOLSA_JUVENTUDE', entity_id=saved.id, citizen_id=jovem.citizen_id, numero_processo=saved.codigo_bolsa, metadata={'codigo_bolsa': saved.codigo_bolsa, 'tipo': saved.tipo.value, 'valor_mensal': str(saved.valor_mensal)})
        return saved

    async def buscar_bolsa(self, bolsa_id: UUID) -> BolsaEstudo:
        item = await self.bolsa_repo.get_by_id(bolsa_id)
        if item is None:
            raise ValueError('Bolsa nao encontrada')
        return item

    async def listar_bolsas(self, *, jovem_id: UUID | None=None, apenas_ativas: bool | None=None) -> list[BolsaEstudo]:
        if jovem_id is not None:
            return await self.bolsa_repo.list_by_jovem(jovem_id)
        if apenas_ativas:
            return await self.bolsa_repo.list_ativas()
        return await self.bolsa_repo.list_all()

    async def encerrar_bolsa(self, *, bolsa_id: UUID, observacoes: str | None=None) -> BolsaEstudo:
        bolsa = await self.buscar_bolsa(bolsa_id)
        bolsa.encerrar(observacoes)
        return await self.bolsa_repo.save(bolsa)

    async def remover_bolsa(self, bolsa_id: UUID) -> None:
        deleted = await self.bolsa_repo.delete(bolsa_id)
        if not deleted:
            raise ValueError('Bolsa nao encontrada')