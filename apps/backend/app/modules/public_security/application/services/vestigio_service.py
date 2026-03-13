from __future__ import annotations
from uuid import UUID
from app.modules.public_security.application.ports.cadeia_custodia_repository_port import CadeiaCustodiaRepositoryPort
from app.modules.public_security.application.ports.policial_repository_port import PolicialRepositoryPort
from app.modules.public_security.application.ports.request_service_port import RequestServicePort
from app.modules.public_security.application.ports.vestigio_repository_port import VestigioRepositoryPort
from app.modules.public_security.domain.enums import StatusVestigio, TipoVestigio
from app.modules.public_security.domain.models.vestigio import Vestigio

class VestigioService:

    def __init__(self, *, vestigio_repo: VestigioRepositoryPort, cadeia_repo: CadeiaCustodiaRepositoryPort, policial_repo: PolicialRepositoryPort, request_service: RequestServicePort | None=None) -> None:
        self.vestigio_repo = vestigio_repo
        self.cadeia_repo = cadeia_repo
        self.policial_repo = policial_repo
        self.request_service = request_service

    async def registrar_vestigio(self, *, cadeia_custodia_id: UUID, tipo: TipoVestigio, descricao: str, localizacao: str, coletado_por_id: UUID | None=None, observacoes: str | None=None, citizen_id: UUID | None=None) -> Vestigio:
        cadeia = await self.cadeia_repo.get_by_id(cadeia_custodia_id)
        if cadeia is None:
            raise ValueError('Cadeia de custodia nao encontrada para registro de vestigio')
        if coletado_por_id is not None:
            coletor = await self.policial_repo.get_by_id(coletado_por_id)
            if coletor is None:
                raise ValueError('Responsavel pela coleta do vestigio nao encontrado')
        codigo = await self.vestigio_repo.next_codigo()
        vestigio = Vestigio.registrar(codigo_vestigio=codigo, cadeia_custodia_id=cadeia_custodia_id, ocorrencia_id=cadeia.ocorrencia_id, tipo=tipo, descricao=descricao, localizacao=localizacao, coletado_por_id=coletado_por_id, observacoes=observacoes)
        saved = await self.vestigio_repo.save(vestigio)
        if self.request_service is not None:
            await self.request_service.create_request(request_type='REGISTRO_VESTIGIO', entity_id=saved.id, numero_processo=saved.codigo_vestigio, citizen_id=citizen_id, metadata={'codigo_vestigio': saved.codigo_vestigio, 'cadeia_custodia_id': str(saved.cadeia_custodia_id), 'ocorrencia_id': str(saved.ocorrencia_id), 'tipo': saved.tipo.value})
        return saved

    async def buscar_vestigio(self, vestigio_id: UUID) -> Vestigio:
        vestigio = await self.vestigio_repo.get_by_id(vestigio_id)
        if vestigio is None:
            raise ValueError('Vestigio nao encontrado')
        return vestigio

    async def listar_vestigios(self, *, cadeia_custodia_id: UUID | None=None, status: StatusVestigio | None=None) -> list[Vestigio]:
        if cadeia_custodia_id is not None:
            return await self.vestigio_repo.list_by_cadeia(cadeia_custodia_id)
        if status is not None:
            return await self.vestigio_repo.list_by_status(status)
        return await self.vestigio_repo.list_all()

    async def atualizar_status(self, *, vestigio_id: UUID, status: StatusVestigio, observacoes: str | None=None) -> Vestigio:
        vestigio = await self.buscar_vestigio(vestigio_id)
        vestigio.atualizar_status(status, observacoes)
        return await self.vestigio_repo.save(vestigio)

    async def remover_vestigio(self, vestigio_id: UUID) -> None:
        deleted = await self.vestigio_repo.delete(vestigio_id)
        if not deleted:
            raise ValueError('Vestigio nao encontrado')