from __future__ import annotations
import asyncio
from datetime import date
from uuid import uuid4
import pytest
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.application.services.operadora_service import OperadoraService
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.domain.enums import StatusOutorga, TipoOperadora, TipoServico
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.tests._fakes import FakeRequestService, InMemoryOperadoraRepository

def test_cadastrar_operadora_sucesso() -> None:

    async def scenario() -> None:
        service = OperadoraService(operadora_repo=InMemoryOperadoraRepository(), request_service=FakeRequestService())
        result = await service.cadastrar_operadora(cnpj='12.345.678/0001-90', razao_social='Telecom SA', tipo=TipoOperadora.CONCESSIONARIA, servicos_autorizados=[TipoServico.TELEFONIA_MOVEL, TipoServico.INTERNET_MOVEL], endereco='Av. Marginal, 100', municipio='Luanda', provincia='Luanda', telefone='222123456', email='contato@telecom.ao', representante_legal='Joao Silva', representante_documento='12345678900', representante_cargo='Diretor')
        assert result.cnpj == '12.345.678/0001-90'
        assert result.status == StatusOutorga.REQUERIDA
    asyncio.run(scenario())

def test_cadastrar_operadora_falha_duplicada() -> None:

    async def scenario() -> None:
        repo = InMemoryOperadoraRepository()
        service = OperadoraService(operadora_repo=repo)
        payload = dict(cnpj='12.345.678/0001-90', razao_social='Telecom SA', tipo=TipoOperadora.CONCESSIONARIA, servicos_autorizados=[TipoServico.INTERNET_MOVEL], endereco='Av. A', municipio='Luanda', provincia='Luanda', telefone='222123456', email='contato@telecom.ao', representante_legal='Joao Silva', representante_documento='12345678900', representante_cargo='Diretor')
        await service.cadastrar_operadora(**payload)
        with pytest.raises(ValueError, match='CNPJ'):
            await service.cadastrar_operadora(**payload)
    asyncio.run(scenario())

def test_autorizar_operadora() -> None:

    async def scenario() -> None:
        service = OperadoraService(operadora_repo=InMemoryOperadoraRepository())
        operadora = await service.cadastrar_operadora(cnpj='98.765.432/0001-10', razao_social='Rede Movel SA', tipo=TipoOperadora.AUTORIZATARIA, servicos_autorizados=[TipoServico.TELEFONIA_MOVEL], endereco='Rua B', municipio='Benguela', provincia='Benguela', telefone='222999888', email='operacao@redemovel.ao', representante_legal='Maria Costa', representante_documento='99988877766', representante_cargo='Gestora')
        atualizado = await service.autorizar_operadora(operadora_id=operadora.id, outorga_id=uuid4(), data_autorizacao=date(2026, 3, 2), data_validade=date(2028, 3, 2))
        assert atualizado.status == StatusOutorga.DEFERIDA
    asyncio.run(scenario())