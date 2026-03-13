from __future__ import annotations
import asyncio
from uuid import uuid4
import pytest
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.application.services.assinante_service import AssinanteService
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.application.services.operadora_service import OperadoraService
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.domain.enums import StatusAssinante, TipoOperadora, TipoPlano, TipoServico
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.tests._fakes import FakeCitizenService, FakeRequestService, InMemoryAssinanteRepository, InMemoryOperadoraRepository

def test_cadastrar_assinante_sucesso() -> None:

    async def scenario() -> None:
        operadora_repo = InMemoryOperadoraRepository()
        operadora_service = OperadoraService(operadora_repo=operadora_repo)
        assinante_service = AssinanteService(assinante_repo=InMemoryAssinanteRepository(), operadora_repo=operadora_repo, citizen_service=FakeCitizenService(active=True), request_service=FakeRequestService())
        operadora = await operadora_service.cadastrar_operadora(cnpj='11.111.111/0001-11', razao_social='Conecta SA', tipo=TipoOperadora.PROVEDOR, servicos_autorizados=[TipoServico.INTERNET_FIXA], endereco='Rua C', municipio='Luanda', provincia='Luanda', telefone='222111111', email='contato@conecta.ao', representante_legal='Paulo Reis', representante_documento='11122233344', representante_cargo='CEO')
        assinante = await assinante_service.cadastrar_assinante(operadora_id=operadora.id, tipo_plano=TipoPlano.POS_PAGO, servico_principal=TipoServico.INTERNET_FIXA, municipio='Luanda', provincia='Luanda', citizen_id=uuid4())
        assert assinante.codigo_assinante.startswith('ASS/')
        assert assinante.status == StatusAssinante.ATIVO
    asyncio.run(scenario())

def test_cadastrar_assinante_falha_servico_nao_autorizado() -> None:

    async def scenario() -> None:
        operadora_repo = InMemoryOperadoraRepository()
        operadora_service = OperadoraService(operadora_repo=operadora_repo)
        assinante_service = AssinanteService(assinante_repo=InMemoryAssinanteRepository(), operadora_repo=operadora_repo, citizen_service=FakeCitizenService(active=True))
        operadora = await operadora_service.cadastrar_operadora(cnpj='22.222.222/0001-22', razao_social='Dados SA', tipo=TipoOperadora.PROVEDOR, servicos_autorizados=[TipoServico.INTERNET_FIXA], endereco='Rua D', municipio='Huambo', provincia='Huambo', telefone='222222222', email='contato@dados.ao', representante_legal='Luis Neto', representante_documento='22233344455', representante_cargo='Gerente')
        with pytest.raises(ValueError, match='autorizado'):
            await assinante_service.cadastrar_assinante(operadora_id=operadora.id, tipo_plano=TipoPlano.PRE_PAGO, servico_principal=TipoServico.TELEFONIA_MOVEL, municipio='Huambo', provincia='Huambo')
    asyncio.run(scenario())

def test_atualizar_status_assinante() -> None:

    async def scenario() -> None:
        operadora_repo = InMemoryOperadoraRepository()
        operadora_service = OperadoraService(operadora_repo=operadora_repo)
        assinante_repo = InMemoryAssinanteRepository()
        assinante_service = AssinanteService(assinante_repo=assinante_repo, operadora_repo=operadora_repo, citizen_service=FakeCitizenService(active=True))
        operadora = await operadora_service.cadastrar_operadora(cnpj='33.333.333/0001-33', razao_social='Mobile SA', tipo=TipoOperadora.AUTORIZATARIA, servicos_autorizados=[TipoServico.TELEFONIA_MOVEL], endereco='Rua E', municipio='Lobito', provincia='Benguela', telefone='222333333', email='contato@mobile.ao', representante_legal='Carla Gomes', representante_documento='33344455566', representante_cargo='Diretora')
        assinante = await assinante_service.cadastrar_assinante(operadora_id=operadora.id, tipo_plano=TipoPlano.CONTROLE, servico_principal=TipoServico.TELEFONIA_MOVEL, municipio='Lobito', provincia='Benguela')
        atualizado = await assinante_service.atualizar_status(assinante_id=assinante.id, status=StatusAssinante.SUSPENSO)
        assert atualizado.status == StatusAssinante.SUSPENSO
        assert atualizado.ativo is False
    asyncio.run(scenario())