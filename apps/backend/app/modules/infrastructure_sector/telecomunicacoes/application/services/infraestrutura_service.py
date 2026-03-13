from __future__ import annotations
from datetime import date
from uuid import UUID
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.application.ports.infraestrutura_repository_port import InfraestruturaRepositoryPort
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.application.ports.operadora_repository_port import OperadoraRepositoryPort
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.application.ports.request_service_port import RequestServicePort
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.domain.enums import StatusInfraestrutura, TipoInfraestrutura
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.domain.models.infraestrutura_telco import InfraestruturaTelco

class InfraestruturaService:

    def __init__(self, *, infraestrutura_repo: InfraestruturaRepositoryPort, operadora_repo: OperadoraRepositoryPort, request_service: RequestServicePort | None=None) -> None:
        self.infraestrutura_repo = infraestrutura_repo
        self.operadora_repo = operadora_repo
        self.request_service = request_service

    async def cadastrar_infraestrutura(self, *, operadora_id: UUID, tipo: TipoInfraestrutura, identificador: str, municipio: str, provincia: str, data_implantacao: date, latitude: float | None=None, longitude: float | None=None, capacidade: str | None=None, observacoes: str | None=None) -> InfraestruturaTelco:
        operadora = await self.operadora_repo.get_by_id(operadora_id)
        if operadora is None:
            raise ValueError('Operadora nao encontrada para infraestrutura')
        codigo = await self.infraestrutura_repo.next_codigo()
        infraestrutura = InfraestruturaTelco.cadastrar(codigo_infra=codigo, operadora_id=operadora_id, tipo=tipo, identificador=identificador, municipio=municipio, provincia=provincia, data_implantacao=data_implantacao, latitude=latitude, longitude=longitude, capacidade=capacidade, observacoes=observacoes)
        saved = await self.infraestrutura_repo.save(infraestrutura)
        if self.request_service is not None:
            await self.request_service.create_request(request_type='CADASTRO_INFRAESTRUTURA_TELECOM', entity_id=saved.id, numero_processo=saved.codigo_infra, metadata={'codigo_infra': saved.codigo_infra, 'operadora_id': str(saved.operadora_id), 'tipo': saved.tipo.value})
        return saved

    async def buscar_infraestrutura(self, infraestrutura_id: UUID) -> InfraestruturaTelco:
        infraestrutura = await self.infraestrutura_repo.get_by_id(infraestrutura_id)
        if infraestrutura is None:
            raise ValueError('Infraestrutura nao encontrada')
        return infraestrutura

    async def listar_infraestruturas(self, *, operadora_id: UUID | None=None, municipio: str | None=None, somente_ativas: bool=False) -> list[InfraestruturaTelco]:
        if operadora_id is not None:
            return await self.infraestrutura_repo.list_by_operadora(operadora_id)
        if municipio:
            return await self.infraestrutura_repo.list_by_municipio(municipio)
        if somente_ativas:
            return await self.infraestrutura_repo.list_ativas()
        return await self.infraestrutura_repo.list_all()

    async def atualizar_status(self, *, infraestrutura_id: UUID, status: StatusInfraestrutura) -> InfraestruturaTelco:
        infraestrutura = await self.buscar_infraestrutura(infraestrutura_id)
        infraestrutura.atualizar_status(status)
        return await self.infraestrutura_repo.save(infraestrutura)

    async def remover_infraestrutura(self, infraestrutura_id: UUID) -> None:
        deleted = await self.infraestrutura_repo.delete(infraestrutura_id)
        if not deleted:
            raise ValueError('Infraestrutura nao encontrada')