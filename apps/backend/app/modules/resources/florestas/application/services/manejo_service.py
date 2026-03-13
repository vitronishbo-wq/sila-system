from __future__ import annotations
from decimal import Decimal
from uuid import UUID
from app.modules.resources.florestas.application.ports.unidade_manejo_repository_port import UnidadeManejoRepositoryPort
from app.modules.resources.florestas.domain.enums import TipoCicloCorte, TipoManejo
from app.modules.resources.florestas.domain.models.unidade_manejo import UnidadeManejo

class ManejoService:

    def __init__(self, unidade_repo: UnidadeManejoRepositoryPort):
        self.unidade_repo = unidade_repo

    async def cadastrar_unidade(self, *, nome: str, area_total_ha: Decimal, tipo_manejo: TipoManejo, ciclo_corte: TipoCicloCorte, operador_id: UUID, imovel_id: UUID) -> UnidadeManejo:
        codigo = await self.unidade_repo.next_codigo(operador_id)
        unidade = UnidadeManejo.cadastrar(nome=nome, area_total_ha=area_total_ha, tipo_manejo=tipo_manejo, ciclo_corte=ciclo_corte, operador_id=operador_id, imovel_id=imovel_id, codigo_um=codigo)
        return await self.unidade_repo.save(unidade)

    async def buscar_unidade(self, unidade_id: UUID) -> UnidadeManejo:
        unidade = await self.unidade_repo.get_by_id(unidade_id)
        if not unidade:
            raise ValueError('Unidade de manejo nao encontrada')
        return unidade

    async def listar_unidades(self, operador_id: UUID) -> list[UnidadeManejo]:
        return await self.unidade_repo.list_by_operador(operador_id)