from __future__ import annotations
from uuid import UUID
from apps.backend.app.modules.civil_protection.application.ports.bombeiro_repository_port import BombeiroRepositoryPort
from apps.backend.app.modules.civil_protection.application.ports.despacho_repository_port import DespachoRepositoryPort
from apps.backend.app.modules.civil_protection.application.ports.ocorrencia_emergencial_repository_port import OcorrenciaEmergencialRepositoryPort
from apps.backend.app.modules.civil_protection.application.ports.request_service_port import RequestServicePort
from apps.backend.app.modules.civil_protection.domain.enums import StatusDespacho, StatusOcorrenciaEmergencial
from apps.backend.app.modules.civil_protection.domain.models.despacho import Despacho

class DespachoService:

    def __init__(self, *, despacho_repo: DespachoRepositoryPort, ocorrencia_repo: OcorrenciaEmergencialRepositoryPort, bombeiro_repo: BombeiroRepositoryPort, request_service: RequestServicePort | None=None) -> None:
        self.despacho_repo = despacho_repo
        self.ocorrencia_repo = ocorrencia_repo
        self.bombeiro_repo = bombeiro_repo
        self.request_service = request_service

    async def registrar_despacho(self, *, ocorrencia_id: UUID, bombeiro_responsavel_id: UUID | None=None, meio_deslocamento: str | None=None, observacoes: str | None=None, citizen_id: UUID | None=None) -> Despacho:
        ocorrencia = await self.ocorrencia_repo.get_by_id(ocorrencia_id)
        if ocorrencia is None:
            raise ValueError('Ocorrencia emergencial nao encontrada')
        if bombeiro_responsavel_id is not None:
            bombeiro = await self.bombeiro_repo.get_by_id(bombeiro_responsavel_id)
            if bombeiro is None:
                raise ValueError('Bombeiro responsavel nao encontrado')
            if bombeiro.corporacao_id != ocorrencia.corporacao_id:
                raise ValueError('Bombeiro responsavel nao pertence a corporacao da ocorrencia')
        codigo_despacho = await self.despacho_repo.next_codigo()
        despacho = Despacho.gerar(codigo_despacho=codigo_despacho, ocorrencia_id=ocorrencia.id, corporacao_id=ocorrencia.corporacao_id, bombeiro_responsavel_id=bombeiro_responsavel_id, meio_deslocamento=meio_deslocamento, observacoes=observacoes)
        saved = await self.despacho_repo.save(despacho)
        if ocorrencia.status == StatusOcorrenciaEmergencial.RECEBIDA:
            ocorrencia.atualizar_status(StatusOcorrenciaEmergencial.EM_ATENDIMENTO, 'Ocorrencia com despacho operacional registrado')
            await self.ocorrencia_repo.save(ocorrencia)
        if self.request_service is not None:
            await self.request_service.create_request(request_type='REGISTRO_DESPACHO', entity_id=saved.id, citizen_id=citizen_id, numero_processo=saved.codigo_despacho, metadata={'codigo_despacho': saved.codigo_despacho, 'ocorrencia_id': str(saved.ocorrencia_id), 'status': saved.status.value})
        return saved

    async def buscar_despacho(self, despacho_id: UUID) -> Despacho:
        despacho = await self.despacho_repo.get_by_id(despacho_id)
        if despacho is None:
            raise ValueError('Despacho nao encontrado')
        return despacho

    async def listar_despachos(self, *, ocorrencia_id: UUID | None=None, status: StatusDespacho | None=None) -> list[Despacho]:
        if ocorrencia_id is not None:
            return await self.despacho_repo.list_by_ocorrencia(ocorrencia_id)
        if status is not None:
            return await self.despacho_repo.list_by_status(status)
        return await self.despacho_repo.list_all()

    async def atualizar_status(self, *, despacho_id: UUID, status: StatusDespacho, observacoes: str | None=None) -> Despacho:
        despacho = await self.buscar_despacho(despacho_id)
        despacho.atualizar_status(status, observacoes)
        return await self.despacho_repo.save(despacho)

    async def remover_despacho(self, despacho_id: UUID) -> None:
        deleted = await self.despacho_repo.delete(despacho_id)
        if not deleted:
            raise ValueError('Despacho nao encontrado')