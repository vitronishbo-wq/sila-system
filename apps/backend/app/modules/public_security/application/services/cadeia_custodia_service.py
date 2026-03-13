from __future__ import annotations
from uuid import UUID
from app.modules.public_security.application.ports.cadeia_custodia_repository_port import CadeiaCustodiaRepositoryPort
from app.modules.public_security.application.ports.policial_repository_port import PolicialRepositoryPort
from app.modules.public_security.application.ports.prova_pericial_repository_port import ProvaPericialRepositoryPort
from app.modules.public_security.application.ports.request_service_port import RequestServicePort
from app.modules.public_security.domain.enums import StatusCadeiaCustodia
from app.modules.public_security.domain.models.cadeia_custodia import CadeiaCustodia

class CadeiaCustodiaService:

    def __init__(self, *, cadeia_repo: CadeiaCustodiaRepositoryPort, prova_repo: ProvaPericialRepositoryPort, policial_repo: PolicialRepositoryPort, request_service: RequestServicePort | None=None) -> None:
        self.cadeia_repo = cadeia_repo
        self.prova_repo = prova_repo
        self.policial_repo = policial_repo
        self.request_service = request_service

    async def iniciar_cadeia(self, *, prova_id: UUID, local_atual: str, responsavel_id: UUID, observacoes: str | None=None, citizen_id: UUID | None=None) -> CadeiaCustodia:
        prova = await self.prova_repo.get_by_id(prova_id)
        if prova is None:
            raise ValueError('Prova pericial nao encontrada para iniciar cadeia de custodia')
        responsavel = await self.policial_repo.get_by_id(responsavel_id)
        if responsavel is None:
            raise ValueError('Responsavel da cadeia de custodia nao encontrado')
        existente = await self.cadeia_repo.get_by_prova(prova_id)
        if existente is not None:
            raise ValueError('Ja existe cadeia de custodia para a prova informada')
        codigo = await self.cadeia_repo.next_codigo()
        cadeia = CadeiaCustodia.iniciar(codigo_cadeia=codigo, prova_id=prova_id, ocorrencia_id=prova.ocorrencia_id, local_atual=local_atual, responsavel_id=responsavel_id, observacoes=observacoes)
        saved = await self.cadeia_repo.save(cadeia)
        prova.vincular_cadeia_custodia(saved.id)
        await self.prova_repo.save(prova)
        if self.request_service is not None:
            await self.request_service.create_request(request_type='INICIO_CADEIA_CUSTODIA', entity_id=saved.id, numero_processo=saved.codigo_cadeia, citizen_id=citizen_id, metadata={'codigo_cadeia': saved.codigo_cadeia, 'prova_id': str(saved.prova_id), 'ocorrencia_id': str(saved.ocorrencia_id)})
        return saved

    async def buscar_cadeia(self, cadeia_id: UUID) -> CadeiaCustodia:
        cadeia = await self.cadeia_repo.get_by_id(cadeia_id)
        if cadeia is None:
            raise ValueError('Cadeia de custodia nao encontrada')
        return cadeia

    async def listar_cadeias(self, *, status: StatusCadeiaCustodia | None=None) -> list[CadeiaCustodia]:
        if status is not None:
            return await self.cadeia_repo.list_by_status(status)
        return await self.cadeia_repo.list_all()

    async def registrar_movimentacao(self, *, cadeia_id: UUID, status: StatusCadeiaCustodia, local_atual: str, responsavel_id: UUID, observacao: str | None=None) -> CadeiaCustodia:
        cadeia = await self.buscar_cadeia(cadeia_id)
        responsavel = await self.policial_repo.get_by_id(responsavel_id)
        if responsavel is None:
            raise ValueError('Responsavel da movimentacao nao encontrado')
        cadeia.registrar_movimentacao(status=status, local_atual=local_atual, responsavel_id=responsavel_id, observacao=observacao)
        return await self.cadeia_repo.save(cadeia)

    async def remover_cadeia(self, cadeia_id: UUID) -> None:
        deleted = await self.cadeia_repo.delete(cadeia_id)
        if not deleted:
            raise ValueError('Cadeia de custodia nao encontrada')