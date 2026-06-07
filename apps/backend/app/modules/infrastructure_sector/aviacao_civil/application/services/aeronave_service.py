from __future__ import annotations

from apps.backend.app.modules.infrastructure_sector.aviacao_civil.application.events import (
    AeronaveRegistradaEvent,
    event_bus,
)
from apps.backend.app.modules.infrastructure_sector.aviacao_civil.application.ports.aeronave_repository_port import (
    AeronaveRepositoryPort,
)
from apps.backend.app.modules.infrastructure_sector.aviacao_civil.domain.enums import (
    CategoriaAeronave,
    TipoAeronave,
)
from apps.backend.app.modules.infrastructure_sector.aviacao_civil.domain.models.aeronave import (
    Aeronave,
)
from apps.backend.app.modules.infrastructure_sector.aviacao_civil.infrastructure.adapters.anac_adapter import (
    AnacAdapter,
)
from apps.backend.app.modules.infrastructure_sector.aviacao_civil.infrastructure.persistence.outbox import (
    InMemoryOutbox,
)


class AeronaveService:
    def __init__(
        self,
        *,
        aeronave_repo: AeronaveRepositoryPort,
        outbox: InMemoryOutbox,
        anac_adapter: AnacAdapter | None = None,
    ) -> None:
        self.aeronave_repo = aeronave_repo
        self.outbox = outbox
        self.anac = anac_adapter

    async def registrar_aeronave(
        self,
        *,
        matricula: str,
        tipo: TipoAeronave,
        categoria: CategoriaAeronave,
        fabricante: str,
        modelo: str,
        numero_serie: str,
        ano_fabricacao: int,
        proprietario_cpf_cnpj: str,
        capacidade_passageiros: int = 0,
        autonomia_km: float = 0.0,
        peso_maximo_decolagem_kg: float = 0.0,
    ) -> Aeronave:
        existente = await self.aeronave_repo.get_by_matricula(matricula)
        if existente is not None:
            raise ValueError("Matricula ja registrada")
        aeronave = Aeronave(
            matricula=matricula,
            tipo=tipo,
            categoria=categoria,
            fabricante=fabricante,
            modelo=modelo,
            numero_serie=numero_serie,
            ano_fabricacao=ano_fabricacao,
            proprietario_cpf_cnpj=proprietario_cpf_cnpj,
            capacidade_passageiros=capacidade_passageiros,
            autonomia_km=autonomia_km,
            peso_maximo_decolagem_kg=peso_maximo_decolagem_kg,
        )
        await self.aeronave_repo.save(aeronave)
        evento = AeronaveRegistradaEvent(
            aeronave_id=aeronave.id,
            matricula=aeronave.matricula,
            modelo=aeronave.modelo,
            proprietario_cpf_cnpj=aeronave.proprietario_cpf_cnpj,
        )
        await self.outbox.append(evento)
        await event_bus.publish(evento)
        if self.anac is not None:
            await self.anac.registrar_aeronave(
                {
                    "aeronave_id": str(aeronave.id),
                    "matricula": aeronave.matricula,
                    "modelo": aeronave.modelo,
                    "fabricante": aeronave.fabricante,
                }
            )
        return aeronave

    async def buscar_aeronave(self, aeronave_id):
        aeronave = await self.aeronave_repo.get_by_id(aeronave_id)
        if aeronave is None:
            raise ValueError("Aeronave nao encontrada")
        return aeronave

    async def listar_aeronaves(self) -> list[Aeronave]:
        return await self.aeronave_repo.list_all()
