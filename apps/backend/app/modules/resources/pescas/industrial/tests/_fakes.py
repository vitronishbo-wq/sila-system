from __future__ import annotations
from datetime import date
from uuid import UUID
from app.modules.resources.pescas.industrial.application.ports.inspecao_sanitaria_industrial_repository_port import InspecaoSanitariaIndustrialRepositoryPort
from app.modules.resources.pescas.industrial.application.ports.lote_producao_repository_port import LoteProducaoRepositoryPort
from app.modules.resources.pescas.industrial.application.ports.produto_processado_repository_port import ProdutoProcessadoRepositoryPort
from app.modules.resources.pescas.industrial.application.ports.unidade_processamento_repository_port import UnidadeProcessamentoRepositoryPort
from app.modules.resources.pescas.industrial.domain.enums import MercadoDestino, StatusInspecao, StatusLoteProducao, TipoProcessamento, TipoProdutoProcessado
from app.modules.resources.pescas.industrial.domain.models.inspecao_sanitaria_industrial import InspecaoSanitariaIndustrial
from app.modules.resources.pescas.industrial.domain.models.lote_producao import LoteProducao
from app.modules.resources.pescas.industrial.domain.models.produto_processado import ProdutoProcessado
from app.modules.resources.pescas.industrial.domain.models.unidade_processamento import UnidadeProcessamento

class InMemoryUnidadeRepository(UnidadeProcessamentoRepositoryPort):

    def __init__(self) -> None:
        self._items: dict[UUID, UnidadeProcessamento] = {}

    async def save(self, unidade: UnidadeProcessamento) -> UnidadeProcessamento:
        self._items[unidade.id] = unidade
        return unidade

    async def get_by_id(self, unidade_id: UUID) -> UnidadeProcessamento | None:
        return self._items.get(unidade_id)

    async def get_by_cnpj(self, cnpj: str) -> UnidadeProcessamento | None:
        normalized = cnpj.strip()
        for item in self._items.values():
            if item.cnpj == normalized:
                return item
        return None

    async def list_by_municipio(self, municipio: str) -> list[UnidadeProcessamento]:
        normalized = municipio.strip().lower()
        values = [item for item in self._items.values() if item.municipio.lower() == normalized]
        return sorted(values, key=lambda item: item.razao_social)

    async def list_by_tipo(self, tipo: TipoProcessamento) -> list[UnidadeProcessamento]:
        values = [item for item in self._items.values() if tipo in item.tipo_processamento]
        return sorted(values, key=lambda item: item.razao_social)

    async def list_all(self) -> list[UnidadeProcessamento]:
        return sorted(self._items.values(), key=lambda item: item.razao_social)

    async def delete(self, unidade_id: UUID) -> bool:
        return self._items.pop(unidade_id, None) is not None

class InMemoryProdutoRepository(ProdutoProcessadoRepositoryPort):

    def __init__(self) -> None:
        self._items: dict[UUID, ProdutoProcessado] = {}

    async def save(self, produto: ProdutoProcessado) -> ProdutoProcessado:
        self._items[produto.id] = produto
        return produto

    async def get_by_id(self, produto_id: UUID) -> ProdutoProcessado | None:
        return self._items.get(produto_id)

    async def get_by_codigo(self, codigo_produto: str) -> ProdutoProcessado | None:
        normalized = codigo_produto.strip()
        for item in self._items.values():
            if item.codigo_produto == normalized:
                return item
        return None

    async def list_all(self) -> list[ProdutoProcessado]:
        return sorted(self._items.values(), key=lambda item: item.codigo_produto)

    async def list_by_unidade(self, unidade_processamento_id: UUID) -> list[ProdutoProcessado]:
        values = [item for item in self._items.values() if item.unidade_processamento_id == unidade_processamento_id]
        return sorted(values, key=lambda item: item.codigo_produto)

    async def list_by_tipo(self, tipo_produto: TipoProdutoProcessado) -> list[ProdutoProcessado]:
        values = [item for item in self._items.values() if item.tipo_produto == tipo_produto]
        return sorted(values, key=lambda item: item.codigo_produto)

    async def list_by_destino(self, mercado_destino: MercadoDestino) -> list[ProdutoProcessado]:
        values = [item for item in self._items.values() if item.mercado_destino == mercado_destino]
        return sorted(values, key=lambda item: item.codigo_produto)

    async def delete(self, produto_id: UUID) -> bool:
        return self._items.pop(produto_id, None) is not None

    async def next_codigo(self) -> str:
        year = date.today().year
        prefix = f'PRD/{year}/'
        count = sum((1 for item in self._items.values() if item.codigo_produto.startswith(prefix)))
        return f'{prefix}{count + 1:05d}'

class InMemoryLoteRepository(LoteProducaoRepositoryPort):

    def __init__(self) -> None:
        self._items: dict[UUID, LoteProducao] = {}

    async def save(self, lote: LoteProducao) -> LoteProducao:
        self._items[lote.id] = lote
        return lote

    async def get_by_id(self, lote_id: UUID) -> LoteProducao | None:
        return self._items.get(lote_id)

    async def get_by_codigo(self, codigo_lote: str) -> LoteProducao | None:
        normalized = codigo_lote.strip()
        for item in self._items.values():
            if item.codigo_lote == normalized:
                return item
        return None

    async def list_all(self) -> list[LoteProducao]:
        return sorted(self._items.values(), key=lambda item: item.codigo_lote)

    async def list_by_unidade(self, unidade_processamento_id: UUID) -> list[LoteProducao]:
        values = [item for item in self._items.values() if item.unidade_processamento_id == unidade_processamento_id]
        return sorted(values, key=lambda item: item.codigo_lote)

    async def list_by_produto(self, produto_processado_id: UUID) -> list[LoteProducao]:
        values = [item for item in self._items.values() if item.produto_processado_id == produto_processado_id]
        return sorted(values, key=lambda item: item.codigo_lote)

    async def list_by_status(self, status: StatusLoteProducao) -> list[LoteProducao]:
        values = [item for item in self._items.values() if item.status == status]
        return sorted(values, key=lambda item: item.codigo_lote)

    async def list_by_periodo(self, data_inicio: date, data_fim: date) -> list[LoteProducao]:
        values = [item for item in self._items.values() if item.data_producao >= data_inicio and item.data_producao <= data_fim]
        return sorted(values, key=lambda item: (item.data_producao, item.codigo_lote))

    async def delete(self, lote_id: UUID) -> bool:
        return self._items.pop(lote_id, None) is not None

    async def next_codigo(self) -> str:
        year = date.today().year
        prefix = f'LOT/{year}/'
        count = sum((1 for item in self._items.values() if item.codigo_lote.startswith(prefix)))
        return f'{prefix}{count + 1:05d}'

class InMemoryInspecaoRepository(InspecaoSanitariaIndustrialRepositoryPort):

    def __init__(self) -> None:
        self._items: dict[UUID, InspecaoSanitariaIndustrial] = {}

    async def save(self, inspecao: InspecaoSanitariaIndustrial) -> InspecaoSanitariaIndustrial:
        self._items[inspecao.id] = inspecao
        return inspecao

    async def get_by_id(self, inspecao_id: UUID) -> InspecaoSanitariaIndustrial | None:
        return self._items.get(inspecao_id)

    async def get_by_codigo(self, codigo_inspecao: str) -> InspecaoSanitariaIndustrial | None:
        normalized = codigo_inspecao.strip()
        for item in self._items.values():
            if item.codigo_inspecao == normalized:
                return item
        return None

    async def list_all(self) -> list[InspecaoSanitariaIndustrial]:
        return sorted(self._items.values(), key=lambda item: item.codigo_inspecao)

    async def list_by_unidade(self, unidade_processamento_id: UUID) -> list[InspecaoSanitariaIndustrial]:
        values = [item for item in self._items.values() if item.unidade_processamento_id == unidade_processamento_id]
        return sorted(values, key=lambda item: item.codigo_inspecao)

    async def list_by_status(self, status: StatusInspecao) -> list[InspecaoSanitariaIndustrial]:
        values = [item for item in self._items.values() if item.status == status]
        return sorted(values, key=lambda item: item.codigo_inspecao)

    async def list_by_lote(self, lote_producao_id: UUID) -> list[InspecaoSanitariaIndustrial]:
        values = [item for item in self._items.values() if item.lote_producao_id == lote_producao_id]
        return sorted(values, key=lambda item: item.codigo_inspecao)

    async def list_by_periodo(self, data_inicio: date, data_fim: date) -> list[InspecaoSanitariaIndustrial]:
        values = [item for item in self._items.values() if item.data_agendada >= data_inicio and item.data_agendada <= data_fim]
        return sorted(values, key=lambda item: (item.data_agendada, item.codigo_inspecao))

    async def delete(self, inspecao_id: UUID) -> bool:
        return self._items.pop(inspecao_id, None) is not None

    async def next_codigo(self) -> str:
        year = date.today().year
        prefix = f'INS/{year}/'
        count = sum((1 for item in self._items.values() if item.codigo_inspecao.startswith(prefix)))
        return f'{prefix}{count + 1:05d}'