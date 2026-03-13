from __future__ import annotations
from datetime import date
from decimal import Decimal
from uuid import UUID
from apps.backend.app.modules.resources.florestas.application.ports.plano_manejo_florestal_repository_port import PlanoManejoFlorestalRepositoryPort
from apps.backend.app.modules.resources.florestas.application.ports.unidade_manejo_repository_port import UnidadeManejoRepositoryPort
from apps.backend.app.modules.resources.florestas.domain.models.plano_manejo_florestal import PlanoManejoFlorestal

class PlanoManejoService:

    def __init__(self, plano_repo: PlanoManejoFlorestalRepositoryPort, unidade_repo: UnidadeManejoRepositoryPort):
        self.plano_repo = plano_repo
        self.unidade_repo = unidade_repo

    async def submeter_plano(self, *, unidade_manejo_id: UUID, responsavel_tecnico_id: UUID, responsavel_tecnico_registro: str, volume_anual_estimado_m3: Decimal, ciclo_corte_anos: int, area_anual_ha: Decimal) -> PlanoManejoFlorestal:
        unidade = await self.unidade_repo.get_by_id(unidade_manejo_id)
        if not unidade:
            raise ValueError('Unidade de manejo nao encontrada')
        numero = f'PMFS-{unidade.codigo_um}-{date.today().year}'
        plano = PlanoManejoFlorestal.submeter(numero_pmfs=numero, unidade_manejo_id=unidade_manejo_id, responsavel_tecnico_id=responsavel_tecnico_id, responsavel_tecnico_registro=responsavel_tecnico_registro, volume_anual_estimado_m3=volume_anual_estimado_m3, ciclo_corte_anos=ciclo_corte_anos, area_anual_ha=area_anual_ha)
        return await self.plano_repo.save(plano)

    async def listar_planos(self, unidade_manejo_id: UUID) -> list[PlanoManejoFlorestal]:
        return await self.plano_repo.list_by_unidade(unidade_manejo_id)