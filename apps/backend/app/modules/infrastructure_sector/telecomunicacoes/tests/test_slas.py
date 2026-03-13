from __future__ import annotations
import asyncio
from datetime import date
from uuid import uuid4
import pytest
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.application.services.operadora_service import OperadoraService
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.application.services.sla_service import SLAService
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.domain.enums import StatusSLA, TipoOperadora, TipoServico
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.tests._fakes import InMemoryOperadoraRepository, InMemorySLARepository

def test_criar_sla_sucesso() -> None:

    async def scenario() -> None:
        operadora_repo = InMemoryOperadoraRepository()
        operadora_service = OperadoraService(operadora_repo=operadora_repo)
        sla_service = SLAService(sla_repo=InMemorySLARepository(), operadora_repo=operadora_repo)
        operadora = await operadora_service.cadastrar_operadora(cnpj='99.999.999/0001-99', razao_social='Conecta Fibra SA', tipo=TipoOperadora.PROVEDOR, servicos_autorizados=[TipoServico.INTERNET_FIXA], endereco='Rua SLA', municipio='Luanda', provincia='Luanda', telefone='222999999', email='sla@conecta.ao', representante_legal='Rui SLA', representante_documento='11122233300', representante_cargo='Diretor')
        sla = await sla_service.criar_sla(operadora_id=operadora.id, nome='SLA Premium Fibra', servico=TipoServico.INTERNET_FIXA, disponibilidade_min_percentual=99.5, latencia_max_ms=50.0, jitter_max_ms=20.0, perda_pacotes_max_percentual=1.0, velocidade_download_min_mbps=200.0, velocidade_upload_min_mbps=100.0, data_inicio=date.today())
        assert sla.codigo_sla.startswith('SLA/')
        assert sla.status == StatusSLA.ATIVO
    asyncio.run(scenario())

def test_criar_sla_falha_operadora_inexistente() -> None:

    async def scenario() -> None:
        service = SLAService(sla_repo=InMemorySLARepository(), operadora_repo=InMemoryOperadoraRepository())
        with pytest.raises(ValueError, match='Operadora'):
            await service.criar_sla(operadora_id=uuid4(), nome='SLA Invalido', servico=TipoServico.INTERNET_FIXA, disponibilidade_min_percentual=99.0, latencia_max_ms=80.0, jitter_max_ms=30.0, perda_pacotes_max_percentual=2.0, velocidade_download_min_mbps=50.0, velocidade_upload_min_mbps=10.0, data_inicio=date.today())
    asyncio.run(scenario())

def test_atualizar_status_sla() -> None:

    async def scenario() -> None:
        operadora_repo = InMemoryOperadoraRepository()
        operadora_service = OperadoraService(operadora_repo=operadora_repo)
        sla_repo = InMemorySLARepository()
        sla_service = SLAService(sla_repo=sla_repo, operadora_repo=operadora_repo)
        operadora = await operadora_service.cadastrar_operadora(cnpj='90.111.222/0001-90', razao_social='SLA Telecom', tipo=TipoOperadora.AUTORIZATARIA, servicos_autorizados=[TipoServico.TELEFONIA_MOVEL], endereco='Av. Teste', municipio='Benguela', provincia='Benguela', telefone='222000111', email='teste@sla.ao', representante_legal='Carla SLA', representante_documento='99988877700', representante_cargo='Gestora')
        sla = await sla_service.criar_sla(operadora_id=operadora.id, nome='SLA Movel Basico', servico=TipoServico.TELEFONIA_MOVEL, disponibilidade_min_percentual=97.0, latencia_max_ms=120.0, jitter_max_ms=40.0, perda_pacotes_max_percentual=3.0, velocidade_download_min_mbps=15.0, velocidade_upload_min_mbps=5.0, data_inicio=date.today())
        atualizado = await sla_service.atualizar_status(sla_id=sla.id, status=StatusSLA.SUSPENSO)
        assert atualizado.status == StatusSLA.SUSPENSO
        assert atualizado.ativo is False
    asyncio.run(scenario())