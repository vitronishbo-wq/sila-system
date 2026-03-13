from __future__ import annotations
from datetime import date
from decimal import Decimal
from uuid import UUID
from app.modules.society.juventude.application.ports.estagio_juvenil_repository_port import EstagioJuvenilRepositoryPort
from app.modules.society.juventude.application.ports.jovem_repository_port import JovemRepositoryPort
from app.modules.society.juventude.application.ports.request_service_port import RequestServicePort
from app.modules.society.juventude.domain.enums import AreaInteresse, StatusEstagio
from app.modules.society.juventude.domain.models.estagio_juvenil import EstagioJuvenil

class EstagioJuvenilService:

    def __init__(self, *, estagio_repo: EstagioJuvenilRepositoryPort, jovem_repo: JovemRepositoryPort, request_service: RequestServicePort | None=None) -> None:
        self.estagio_repo = estagio_repo
        self.jovem_repo = jovem_repo
        self.request_service = request_service

    async def registrar_estagio(self, *, jovem_id: UUID, instituicao: str, area_interesse: AreaInteresse, cargo: str, carga_horaria_semanal: int, data_inicio: date, bolsa_auxilio: Decimal | None=None, data_fim: date | None=None, observacoes: str | None=None) -> EstagioJuvenil:
        jovem = await self.jovem_repo.get_by_id(jovem_id)
        if jovem is None:
            raise ValueError('Jovem nao encontrado para estagio')
        codigo = await self.estagio_repo.next_codigo()
        estagio = EstagioJuvenil.registrar(codigo_estagio=codigo, jovem_id=jovem_id, instituicao=instituicao, area_interesse=area_interesse, cargo=cargo, carga_horaria_semanal=carga_horaria_semanal, data_inicio=data_inicio, bolsa_auxilio=bolsa_auxilio, data_fim=data_fim, observacoes=observacoes)
        saved = await self.estagio_repo.save(estagio)
        if self.request_service is not None:
            await self.request_service.create_request(request_type='REGISTRO_ESTAGIO_JUVENTUDE', entity_id=saved.id, citizen_id=jovem.citizen_id, numero_processo=saved.codigo_estagio, metadata={'codigo_estagio': saved.codigo_estagio, 'instituicao': saved.instituicao, 'status': saved.status.value})
        return saved

    async def buscar_estagio(self, estagio_id: UUID) -> EstagioJuvenil:
        item = await self.estagio_repo.get_by_id(estagio_id)
        if item is None:
            raise ValueError('Estagio nao encontrado')
        return item

    async def listar_estagios(self, *, jovem_id: UUID | None=None, status: StatusEstagio | None=None) -> list[EstagioJuvenil]:
        if jovem_id is not None:
            return await self.estagio_repo.list_by_jovem(jovem_id)
        if status is not None:
            return await self.estagio_repo.list_by_status(status)
        return await self.estagio_repo.list_all()

    async def atualizar_status(self, *, estagio_id: UUID, status: StatusEstagio) -> EstagioJuvenil:
        estagio = await self.buscar_estagio(estagio_id)
        estagio.atualizar_status(status)
        return await self.estagio_repo.save(estagio)

    async def remover_estagio(self, estagio_id: UUID) -> None:
        deleted = await self.estagio_repo.delete(estagio_id)
        if not deleted:
            raise ValueError('Estagio nao encontrado')