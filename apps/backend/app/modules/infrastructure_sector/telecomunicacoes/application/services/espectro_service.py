from __future__ import annotations
from uuid import UUID
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.application.ports.espectro_repository_port import EspectroRepositoryPort
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.application.ports.outorga_espectro_repository_port import OutorgaEspectroRepositoryPort
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.application.ports.request_service_port import RequestServicePort
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.domain.enums import StatusEspectro, TipoEspectro, TipoServico
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.domain.models.espectro import Espectro

class EspectroService:

    def __init__(self, *, espectro_repo: EspectroRepositoryPort, outorga_repo: OutorgaEspectroRepositoryPort, request_service: RequestServicePort | None=None) -> None:
        self.espectro_repo = espectro_repo
        self.outorga_repo = outorga_repo
        self.request_service = request_service

    async def registrar_espectro(self, *, tipo: TipoEspectro, frequencia_inicial_mhz: float, frequencia_final_mhz: float, servico_principal: TipoServico, municipio: str, provincia: str, outorga_id: UUID | None=None, observacoes: str | None=None) -> Espectro:
        if outorga_id is not None:
            outorga = await self.outorga_repo.get_by_id(outorga_id)
            if outorga is None:
                raise ValueError('Outorga informada nao encontrada')
        codigo = await self.espectro_repo.next_codigo()
        espectro = Espectro.registrar(codigo_espectro=codigo, tipo=tipo, frequencia_inicial_mhz=frequencia_inicial_mhz, frequencia_final_mhz=frequencia_final_mhz, servico_principal=servico_principal, municipio=municipio, provincia=provincia, outorga_id=outorga_id, observacoes=observacoes)
        saved = await self.espectro_repo.save(espectro)
        if self.request_service is not None:
            await self.request_service.create_request(request_type='REGISTRO_ESPECTRO_TELECOM', entity_id=saved.id, numero_processo=saved.codigo_espectro, metadata={'codigo_espectro': saved.codigo_espectro, 'tipo': saved.tipo.value, 'servico_principal': saved.servico_principal.value})
        return saved

    async def buscar_espectro(self, espectro_id: UUID) -> Espectro:
        espectro = await self.espectro_repo.get_by_id(espectro_id)
        if espectro is None:
            raise ValueError('Espectro nao encontrado')
        return espectro

    async def listar_espectros(self, *, tipo: TipoEspectro | None=None, municipio: str | None=None, somente_disponiveis: bool=False) -> list[Espectro]:
        if tipo is not None:
            return await self.espectro_repo.list_by_tipo(tipo)
        if municipio:
            return await self.espectro_repo.list_by_municipio(municipio)
        if somente_disponiveis:
            return await self.espectro_repo.list_by_status(StatusEspectro.DISPONIVEL)
        return await self.espectro_repo.list_all()

    async def vincular_outorga(self, *, espectro_id: UUID, outorga_id: UUID) -> Espectro:
        espectro = await self.buscar_espectro(espectro_id)
        outorga = await self.outorga_repo.get_by_id(outorga_id)
        if outorga is None:
            raise ValueError('Outorga nao encontrada')
        espectro.vincular_outorga(outorga_id)
        return await self.espectro_repo.save(espectro)

    async def atualizar_status(self, *, espectro_id: UUID, status: StatusEspectro) -> Espectro:
        espectro = await self.buscar_espectro(espectro_id)
        espectro.atualizar_status(status)
        return await self.espectro_repo.save(espectro)

    async def remover_espectro(self, espectro_id: UUID) -> None:
        deleted = await self.espectro_repo.delete(espectro_id)
        if not deleted:
            raise ValueError('Espectro nao encontrado')