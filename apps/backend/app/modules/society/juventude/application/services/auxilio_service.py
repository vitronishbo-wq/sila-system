from __future__ import annotations
from datetime import date
from decimal import Decimal
from uuid import UUID
from app.modules.society.juventude.application.ports.auxilio_repository_port import AuxilioRepositoryPort
from app.modules.society.juventude.application.ports.jovem_repository_port import JovemRepositoryPort
from app.modules.society.juventude.application.ports.request_service_port import RequestServicePort
from app.modules.society.juventude.domain.enums import StatusBeneficio, TipoAuxilio
from app.modules.society.juventude.domain.models.auxilio import Auxilio

class AuxilioService:

    def __init__(self, *, auxilio_repo: AuxilioRepositoryPort, jovem_repo: JovemRepositoryPort, request_service: RequestServicePort | None=None) -> None:
        self.auxilio_repo = auxilio_repo
        self.jovem_repo = jovem_repo
        self.request_service = request_service

    async def conceder_auxilio(self, *, jovem_id: UUID, tipo: TipoAuxilio, data_inicio: date, valor_mensal: Decimal | None=None, data_fim: date | None=None, observacoes: str | None=None) -> Auxilio:
        jovem = await self.jovem_repo.get_by_id(jovem_id)
        if jovem is None:
            raise ValueError('Jovem nao encontrado para concessao de auxilio')
        codigo = await self.auxilio_repo.next_codigo()
        auxilio = Auxilio.conceder(codigo_auxilio=codigo, jovem_id=jovem_id, tipo=tipo, data_inicio=data_inicio, valor_mensal=valor_mensal, data_fim=data_fim, observacoes=observacoes)
        saved = await self.auxilio_repo.save(auxilio)
        jovem.adicionar_auxilio(saved.id)
        await self.jovem_repo.save(jovem)
        if self.request_service is not None:
            await self.request_service.create_request(request_type='CONCESSAO_AUXILIO_JUVENTUDE', entity_id=saved.id, citizen_id=jovem.citizen_id, numero_processo=saved.codigo_auxilio, metadata={'codigo_auxilio': saved.codigo_auxilio, 'jovem_id': str(jovem_id), 'tipo': saved.tipo.value, 'status': saved.status.value})
        return saved

    async def buscar_auxilio(self, auxilio_id: UUID) -> Auxilio:
        auxilio = await self.auxilio_repo.get_by_id(auxilio_id)
        if auxilio is None:
            raise ValueError('Auxilio nao encontrado')
        return auxilio

    async def listar_auxilios(self, *, jovem_id: UUID | None=None, tipo: TipoAuxilio | None=None, status: StatusBeneficio | None=None) -> list[Auxilio]:
        if jovem_id is not None:
            return await self.auxilio_repo.list_by_jovem(jovem_id)
        if tipo is not None:
            return await self.auxilio_repo.list_by_tipo(tipo)
        if status is not None:
            return await self.auxilio_repo.list_by_status(status)
        return await self.auxilio_repo.list_all()

    async def atualizar_status(self, *, auxilio_id: UUID, status: StatusBeneficio, observacoes: str | None=None) -> Auxilio:
        auxilio = await self.buscar_auxilio(auxilio_id)
        auxilio.atualizar_status(status, observacoes)
        return await self.auxilio_repo.save(auxilio)

    async def remover_auxilio(self, auxilio_id: UUID) -> None:
        deleted = await self.auxilio_repo.delete(auxilio_id)
        if not deleted:
            raise ValueError('Auxilio nao encontrado')