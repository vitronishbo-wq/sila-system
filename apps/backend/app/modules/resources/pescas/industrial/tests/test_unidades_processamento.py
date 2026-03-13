from __future__ import annotations
import asyncio
from decimal import Decimal
from uuid import uuid4
from apps.backend.app.modules.resources.pescas.industrial.application.services.unidade_processamento_service import UnidadeProcessamentoService
from apps.backend.app.modules.resources.pescas.industrial.domain.enums import ClassificacaoIndustrial, TipoProcessamento
from apps.backend.app.modules.resources.pescas.industrial.tests._fakes import InMemoryUnidadeRepository

class _FakePescasService:

    async def armador_exists(self, armador_id):
        return True

class _FakeIndustriaService:

    async def cnpj_ativo(self, cnpj: str) -> bool:
        return True

class _FakeRequestService:

    async def create_request(self, **kwargs):
        return uuid4()

def test_cadastrar_unidade_sucesso() -> None:

    async def scenario() -> None:
        repo = InMemoryUnidadeRepository()
        service = UnidadeProcessamentoService(unidade_repo=repo, pescas_service=_FakePescasService(), industria_service=_FakeIndustriaService(), request_service=_FakeRequestService())
        result = await service.cadastrar_unidade(cnpj='12.345.678/0001-90', razao_social='Fabrica Atlantico', tipo_processamento=[TipoProcessamento.FILETAGEM, TipoProcessamento.CONGELADO], classificacao=ClassificacaoIndustrial.TIPO_A, capacidade_kg_dia=Decimal('12000'), area_total_m2=Decimal('3500'), area_producao_m2=Decimal('1500'), area_armazenagem_m2=Decimal('1200'), numero_funcionarios=85, endereco='Zona Industrial Porto', municipio='Benguela', provincia='Benguela', armador_id=uuid4())
        assert result.cnpj == '12.345.678/0001-90'
        assert result.classificacao == ClassificacaoIndustrial.TIPO_A
    asyncio.run(scenario())

def test_listar_unidade_por_tipo() -> None:

    async def scenario() -> None:
        repo = InMemoryUnidadeRepository()
        service = UnidadeProcessamentoService(unidade_repo=repo, pescas_service=_FakePescasService(), industria_service=_FakeIndustriaService())
        await service.cadastrar_unidade(cnpj='22.222.222/0001-22', razao_social='Unidade Sul', tipo_processamento=[TipoProcessamento.CONGELADO], classificacao=ClassificacaoIndustrial.TIPO_B, capacidade_kg_dia=Decimal('2000'), area_total_m2=Decimal('500'), area_producao_m2=Decimal('250'), area_armazenagem_m2=Decimal('150'), numero_funcionarios=20, endereco='Rua 1', municipio='Namibe', provincia='Namibe')
        await service.cadastrar_unidade(cnpj='33.333.333/0001-33', razao_social='Unidade Norte', tipo_processamento=[TipoProcessamento.FILETAGEM], classificacao=ClassificacaoIndustrial.TIPO_C, capacidade_kg_dia=Decimal('3000'), area_total_m2=Decimal('700'), area_producao_m2=Decimal('300'), area_armazenagem_m2=Decimal('200'), numero_funcionarios=30, endereco='Rua 2', municipio='Luanda', provincia='Luanda')
        congelados = await service.listar_unidades_por_tipo(TipoProcessamento.CONGELADO)
        assert len(congelados) == 1
        assert congelados[0].razao_social == 'Unidade Sul'
    asyncio.run(scenario())