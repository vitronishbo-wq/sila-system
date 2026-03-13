from __future__ import annotations
from uuid import UUID
from app.modules.public_security.application.ports.laudo_pericial_repository_port import LaudoPericialRepositoryPort
from app.modules.public_security.application.ports.policial_repository_port import PolicialRepositoryPort
from app.modules.public_security.application.ports.prova_pericial_repository_port import ProvaPericialRepositoryPort
from app.modules.public_security.application.ports.request_service_port import RequestServicePort
from app.modules.public_security.domain.enums import StatusLaudo, StatusProva, TipoLaudo
from app.modules.public_security.domain.models.laudo_pericial import LaudoPericial

class LaudoPericialService:

    def __init__(self, *, laudo_repo: LaudoPericialRepositoryPort, prova_repo: ProvaPericialRepositoryPort, policial_repo: PolicialRepositoryPort, request_service: RequestServicePort | None=None) -> None:
        self.laudo_repo = laudo_repo
        self.prova_repo = prova_repo
        self.policial_repo = policial_repo
        self.request_service = request_service

    async def emitir_laudo(self, *, prova_id: UUID, tipo_laudo: TipoLaudo, perito_id: UUID, conclusao: str, resumo: str | None=None, arquivo_url: str | None=None, observacoes: str | None=None, citizen_id: UUID | None=None) -> LaudoPericial:
        prova = await self.prova_repo.get_by_id(prova_id)
        if prova is None:
            raise ValueError('Prova pericial nao encontrada para emissao de laudo')
        perito = await self.policial_repo.get_by_id(perito_id)
        if perito is None:
            raise ValueError('Perito responsavel nao encontrado')
        numero_laudo = await self.laudo_repo.next_numero()
        laudo = LaudoPericial.emitir(numero_laudo=numero_laudo, prova_id=prova_id, tipo_laudo=tipo_laudo, perito_id=perito_id, conclusao=conclusao, resumo=resumo, arquivo_url=arquivo_url, observacoes=observacoes)
        saved = await self.laudo_repo.save(laudo)
        prova.atualizar_status(StatusProva.VALIDADA, 'Laudo pericial emitido')
        await self.prova_repo.save(prova)
        if self.request_service is not None:
            await self.request_service.create_request(request_type='EMISSAO_LAUDO_PERICIAL', entity_id=saved.id, numero_processo=saved.numero_laudo, citizen_id=citizen_id, metadata={'numero_laudo': saved.numero_laudo, 'prova_id': str(saved.prova_id), 'tipo_laudo': saved.tipo_laudo.value})
        return saved

    async def buscar_laudo(self, laudo_id: UUID) -> LaudoPericial:
        laudo = await self.laudo_repo.get_by_id(laudo_id)
        if laudo is None:
            raise ValueError('Laudo pericial nao encontrado')
        return laudo

    async def listar_laudos(self, *, prova_id: UUID | None=None, tipo: TipoLaudo | None=None, status: StatusLaudo | None=None) -> list[LaudoPericial]:
        if prova_id is not None:
            return await self.laudo_repo.list_by_prova(prova_id)
        if tipo is not None:
            return await self.laudo_repo.list_by_tipo(tipo)
        if status is not None:
            return await self.laudo_repo.list_by_status(status)
        return await self.laudo_repo.list_all()

    async def atualizar_status(self, *, laudo_id: UUID, status: StatusLaudo, observacoes: str | None=None) -> LaudoPericial:
        laudo = await self.buscar_laudo(laudo_id)
        laudo.atualizar_status(status, observacoes)
        return await self.laudo_repo.save(laudo)

    async def remover_laudo(self, laudo_id: UUID) -> None:
        deleted = await self.laudo_repo.delete(laudo_id)
        if not deleted:
            raise ValueError('Laudo pericial nao encontrado')