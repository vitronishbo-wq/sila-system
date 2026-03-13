from __future__ import annotations
import asyncio
from decimal import Decimal
from apps.backend.app.modules.tourism.application.services.roteiro_service import RoteiroService
from apps.backend.app.modules.tourism.infrastructure.adapters.comercio_servicos_service_adapter import ComercioServicosServiceAdapter
from apps.backend.app.modules.tourism.infrastructure.adapters.transportes_logistica_service_adapter import TransportesLogisticaServiceAdapter
from apps.backend.app.modules.tourism.infrastructure.repositories.sqlalchemy_roteiro_repository import SQLAlchemyRoteiroRepository

class _FakeTransportesService:

    async def list_opcoes_transporte(self, *, origem: str, destino: str) -> list[str]:
        return ['rodoviario', 'ferroviario']

    async def estimate_tempo_viagem_horas(self, *, origem: str, destino: str, modal: str | None=None) -> float | None:
        return 4.0

class _FakeComercioService:

    async def list_parceiros_turisticos(self, *, municipio: str) -> list[str]:
        return [f'{municipio} Restaurante Centro', f'{municipio} Hotel Orla']

    async def agencia_cnpj_ativo(self, *, cnpj: str) -> bool:
        return True

def test_cadastrar_roteiro_com_integracao_cruzada() -> None:
    repo = SQLAlchemyRoteiroRepository()
    transportes = TransportesLogisticaServiceAdapter(_FakeTransportesService())
    comercio = ComercioServicosServiceAdapter(_FakeComercioService())
    service = RoteiroService(repository=repo, transportes_service=transportes, comercio_service=comercio)
    result = asyncio.run(service.cadastrar(titulo='Roteiro Serra e Praia', descricao='Combina trilha de serra e descanso na praia.', municipio_origem='Benguela', provincia_origem='Benguela', duracao_horas=10, pontos_parada=['Lobito', 'Baia Azul'], acessivel=False, valor_estimado=Decimal('15000')))
    assert result.codigo.startswith('RT/BENGUELA/')
    assert 'rodoviario' in (result.meios_transporte_sugeridos or [])
    assert any(('Benguela' in item for item in result.parceiros_comerciais or []))

def test_listar_roteiros_filtra_ativo() -> None:
    repo = SQLAlchemyRoteiroRepository()
    service = RoteiroService(repository=repo)
    item = asyncio.run(service.cadastrar(titulo='Roteiro Historico', descricao='Circuito por sitios historicos.', municipio_origem='Luanda', provincia_origem='Luanda', duracao_horas=6, acessivel=True))
    asyncio.run(service.atualizar(item.id, ativo=False, refresh_integracoes=False))
    ativos = asyncio.run(service.listar(ativo=True))
    inativos = asyncio.run(service.listar(ativo=False))
    assert len(ativos) == 0
    assert len(inativos) == 1
