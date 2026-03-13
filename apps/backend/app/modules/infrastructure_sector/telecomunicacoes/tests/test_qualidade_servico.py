from __future__ import annotations
import asyncio
from datetime import date
from uuid import uuid4
import pytest
from app.modules.infrastructure_sector.telecomunicacoes.application.services.assinante_service import AssinanteService
from app.modules.infrastructure_sector.telecomunicacoes.application.services.operadora_service import OperadoraService
from app.modules.infrastructure_sector.telecomunicacoes.application.services.qualidade_servico_service import QualidadeServicoService
from app.modules.infrastructure_sector.telecomunicacoes.application.services.sla_service import SLAService
from app.modules.infrastructure_sector.telecomunicacoes.domain.enums import StatusQualidadeServico, TipoOperadora, TipoPlano, TipoServico
from app.modules.infrastructure_sector.telecomunicacoes.tests._fakes import FakeCitizenService, InMemoryAssinanteRepository, InMemoryOperadoraRepository, InMemoryQualidadeServicoRepository, InMemorySLARepository

def test_registrar_medicao_qualidade_sucesso() -> None:

    async def scenario() -> None:
        operadora_repo = InMemoryOperadoraRepository()
        assinante_repo = InMemoryAssinanteRepository()
        sla_repo = InMemorySLARepository()
        operadora_service = OperadoraService(operadora_repo=operadora_repo)
        assinante_service = AssinanteService(assinante_repo=assinante_repo, operadora_repo=operadora_repo, citizen_service=FakeCitizenService(active=True))
        sla_service = SLAService(sla_repo=sla_repo, operadora_repo=operadora_repo)
        qualidade_service = QualidadeServicoService(qualidade_repo=InMemoryQualidadeServicoRepository(), sla_repo=sla_repo, operadora_repo=operadora_repo, assinante_repo=assinante_repo)
        operadora = await operadora_service.cadastrar_operadora(cnpj='12.120.120/0001-12', razao_social='Qualidade Fibra SA', tipo=TipoOperadora.PROVEDOR, servicos_autorizados=[TipoServico.INTERNET_FIXA], endereco='Rua QoS', municipio='Luanda', provincia='Luanda', telefone='222121212', email='qos@fibra.ao', representante_legal='Paula QoS', representante_documento='11144477700', representante_cargo='Diretora')
        assinante = await assinante_service.cadastrar_assinante(operadora_id=operadora.id, tipo_plano=TipoPlano.POS_PAGO, servico_principal=TipoServico.INTERNET_FIXA, municipio='Luanda', provincia='Luanda', citizen_id=uuid4())
        sla = await sla_service.criar_sla(operadora_id=operadora.id, nome='SLA Residencial', servico=TipoServico.INTERNET_FIXA, disponibilidade_min_percentual=99.0, latencia_max_ms=60.0, jitter_max_ms=25.0, perda_pacotes_max_percentual=1.0, velocidade_download_min_mbps=100.0, velocidade_upload_min_mbps=50.0, data_inicio=date.today())
        medicao = await qualidade_service.registrar_medicao(operadora_id=operadora.id, assinante_id=assinante.id, sla_id=sla.id, servico=TipoServico.INTERNET_FIXA, data_medicao=date.today(), disponibilidade_percentual=99.4, latencia_ms=40.0, jitter_ms=15.0, perda_pacotes_percentual=0.4, velocidade_download_mbps=180.0, velocidade_upload_mbps=90.0)
        assert medicao.codigo_medicao.startswith('QLT/')
        assert medicao.status == StatusQualidadeServico.CONFORME
    asyncio.run(scenario())

def test_registrar_medicao_falha_assinante_de_outra_operadora() -> None:

    async def scenario() -> None:
        operadora_repo = InMemoryOperadoraRepository()
        assinante_repo = InMemoryAssinanteRepository()
        operadora_service = OperadoraService(operadora_repo=operadora_repo)
        assinante_service = AssinanteService(assinante_repo=assinante_repo, operadora_repo=operadora_repo, citizen_service=FakeCitizenService(active=True))
        qualidade_service = QualidadeServicoService(qualidade_repo=InMemoryQualidadeServicoRepository(), sla_repo=InMemorySLARepository(), operadora_repo=operadora_repo, assinante_repo=assinante_repo)
        operadora_a = await operadora_service.cadastrar_operadora(cnpj='11.100.100/0001-11', razao_social='Operadora A', tipo=TipoOperadora.PROVEDOR, servicos_autorizados=[TipoServico.INTERNET_FIXA], endereco='Rua A', municipio='Luanda', provincia='Luanda', telefone='222100100', email='a@telco.ao', representante_legal='A', representante_documento='11111111111', representante_cargo='A')
        operadora_b = await operadora_service.cadastrar_operadora(cnpj='22.200.200/0001-22', razao_social='Operadora B', tipo=TipoOperadora.PROVEDOR, servicos_autorizados=[TipoServico.INTERNET_FIXA], endereco='Rua B', municipio='Luanda', provincia='Luanda', telefone='222200200', email='b@telco.ao', representante_legal='B', representante_documento='22222222222', representante_cargo='B')
        assinante = await assinante_service.cadastrar_assinante(operadora_id=operadora_b.id, tipo_plano=TipoPlano.POS_PAGO, servico_principal=TipoServico.INTERNET_FIXA, municipio='Luanda', provincia='Luanda', citizen_id=uuid4())
        with pytest.raises(ValueError, match='nao pertence'):
            await qualidade_service.registrar_medicao(operadora_id=operadora_a.id, assinante_id=assinante.id, servico=TipoServico.INTERNET_FIXA, data_medicao=date.today(), disponibilidade_percentual=98.0, latencia_ms=55.0, jitter_ms=18.0, perda_pacotes_percentual=0.9, velocidade_download_mbps=110.0, velocidade_upload_mbps=45.0)
    asyncio.run(scenario())

def test_atualizar_status_medicao() -> None:

    async def scenario() -> None:
        operadora_repo = InMemoryOperadoraRepository()
        operadora_service = OperadoraService(operadora_repo=operadora_repo)
        qualidade_repo = InMemoryQualidadeServicoRepository()
        qualidade_service = QualidadeServicoService(qualidade_repo=qualidade_repo, sla_repo=InMemorySLARepository(), operadora_repo=operadora_repo, assinante_repo=InMemoryAssinanteRepository())
        operadora = await operadora_service.cadastrar_operadora(cnpj='33.300.300/0001-33', razao_social='Operadora QLT', tipo=TipoOperadora.AUTORIZATARIA, servicos_autorizados=[TipoServico.TELEFONIA_MOVEL], endereco='Rua Q', municipio='Benguela', provincia='Benguela', telefone='222300300', email='qlt@operadora.ao', representante_legal='Q', representante_documento='33333333333', representante_cargo='Q')
        medicao = await qualidade_service.registrar_medicao(operadora_id=operadora.id, servico=TipoServico.TELEFONIA_MOVEL, data_medicao=date.today(), disponibilidade_percentual=80.0, latencia_ms=200.0, jitter_ms=90.0, perda_pacotes_percentual=8.0, velocidade_download_mbps=5.0, velocidade_upload_mbps=2.0)
        atualizada = await qualidade_service.atualizar_status(medicao_id=medicao.id, status=StatusQualidadeServico.ALERTA)
        assert atualizada.status == StatusQualidadeServico.ALERTA
        assert atualizada.ativo is True
    asyncio.run(scenario())