from __future__ import annotations
import asyncio
from datetime import date
from uuid import uuid4
import pytest
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.application.services.assinante_service import AssinanteService
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.application.services.indicador_qualidade_service import IndicadorQualidadeService
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.application.services.operadora_service import OperadoraService
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.application.services.qualidade_servico_service import QualidadeServicoService
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.domain.enums import StatusIndicadorQualidade, TipoOperadora, TipoPlano, TipoServico
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.tests._fakes import FakeCitizenService, InMemoryAssinanteRepository, InMemoryIndicadorQualidadeRepository, InMemoryOperadoraRepository, InMemoryQualidadeServicoRepository, InMemorySLARepository

def test_gerar_indicador_qualidade_sucesso() -> None:

    async def scenario() -> None:
        operadora_repo = InMemoryOperadoraRepository()
        assinante_repo = InMemoryAssinanteRepository()
        qualidade_repo = InMemoryQualidadeServicoRepository()
        operadora_service = OperadoraService(operadora_repo=operadora_repo)
        assinante_service = AssinanteService(assinante_repo=assinante_repo, operadora_repo=operadora_repo, citizen_service=FakeCitizenService(active=True))
        qualidade_service = QualidadeServicoService(qualidade_repo=qualidade_repo, sla_repo=InMemorySLARepository(), operadora_repo=operadora_repo, assinante_repo=assinante_repo)
        indicador_service = IndicadorQualidadeService(indicador_repo=InMemoryIndicadorQualidadeRepository(), qualidade_repo=qualidade_repo, operadora_repo=operadora_repo)
        operadora = await operadora_service.cadastrar_operadora(cnpj='44.400.400/0001-44', razao_social='Indicadores SA', tipo=TipoOperadora.PROVEDOR, servicos_autorizados=[TipoServico.INTERNET_FIXA], endereco='Rua IND', municipio='Luanda', provincia='Luanda', telefone='222400400', email='indicadores@telco.ao', representante_legal='Ana IND', representante_documento='44444444444', representante_cargo='Diretora')
        assinante = await assinante_service.cadastrar_assinante(operadora_id=operadora.id, tipo_plano=TipoPlano.POS_PAGO, servico_principal=TipoServico.INTERNET_FIXA, municipio='Luanda', provincia='Luanda', citizen_id=uuid4())
        await qualidade_service.registrar_medicao(operadora_id=operadora.id, assinante_id=assinante.id, servico=TipoServico.INTERNET_FIXA, data_medicao=date.today(), disponibilidade_percentual=99.0, latencia_ms=45.0, jitter_ms=10.0, perda_pacotes_percentual=0.5, velocidade_download_mbps=140.0, velocidade_upload_mbps=70.0)
        await qualidade_service.registrar_medicao(operadora_id=operadora.id, assinante_id=assinante.id, servico=TipoServico.INTERNET_FIXA, data_medicao=date.today(), disponibilidade_percentual=98.5, latencia_ms=50.0, jitter_ms=12.0, perda_pacotes_percentual=0.7, velocidade_download_mbps=130.0, velocidade_upload_mbps=65.0)
        indicador = await indicador_service.gerar_indicador_operadora(operadora_id=operadora.id, referencia_ano=date.today().year, referencia_mes=date.today().month)
        assert indicador.codigo_indicador.startswith('IND/')
        assert indicador.total_medicoes == 2
        assert indicador.status in {StatusIndicadorQualidade.BOM, StatusIndicadorQualidade.REGULAR, StatusIndicadorQualidade.CRITICO}
    asyncio.run(scenario())

def test_gerar_indicador_falha_sem_medicoes() -> None:

    async def scenario() -> None:
        operadora_repo = InMemoryOperadoraRepository()
        operadora_service = OperadoraService(operadora_repo=operadora_repo)
        indicador_service = IndicadorQualidadeService(indicador_repo=InMemoryIndicadorQualidadeRepository(), qualidade_repo=InMemoryQualidadeServicoRepository(), operadora_repo=operadora_repo)
        operadora = await operadora_service.cadastrar_operadora(cnpj='55.500.500/0001-55', razao_social='Sem Medicoes SA', tipo=TipoOperadora.PROVEDOR, servicos_autorizados=[TipoServico.INTERNET_FIXA], endereco='Rua Sem', municipio='Huambo', provincia='Huambo', telefone='222500500', email='sem@medicao.ao', representante_legal='Sem Dados', representante_documento='55555555555', representante_cargo='Gestor')
        with pytest.raises(ValueError, match='Nao existem medicoes'):
            await indicador_service.gerar_indicador_operadora(operadora_id=operadora.id, referencia_ano=date.today().year, referencia_mes=date.today().month)
    asyncio.run(scenario())

def test_listar_indicadores_por_status() -> None:

    async def scenario() -> None:
        operadora_repo = InMemoryOperadoraRepository()
        qualidade_repo = InMemoryQualidadeServicoRepository()
        indicador_repo = InMemoryIndicadorQualidadeRepository()
        operadora_service = OperadoraService(operadora_repo=operadora_repo)
        indicador_service = IndicadorQualidadeService(indicador_repo=indicador_repo, qualidade_repo=qualidade_repo, operadora_repo=operadora_repo)
        operadora = await operadora_service.cadastrar_operadora(cnpj='66.600.600/0001-66', razao_social='Lista Indicadores SA', tipo=TipoOperadora.AUTORIZATARIA, servicos_autorizados=[TipoServico.TELEFONIA_MOVEL], endereco='Rua Lista', municipio='Benguela', provincia='Benguela', telefone='222600600', email='lista@indicadores.ao', representante_legal='Lista', representante_documento='66666666666', representante_cargo='Diretora')
        qualidade_service = QualidadeServicoService(qualidade_repo=qualidade_repo, sla_repo=InMemorySLARepository(), operadora_repo=operadora_repo, assinante_repo=InMemoryAssinanteRepository())
        await qualidade_service.registrar_medicao(operadora_id=operadora.id, servico=TipoServico.TELEFONIA_MOVEL, data_medicao=date.today(), disponibilidade_percentual=60.0, latencia_ms=300.0, jitter_ms=120.0, perda_pacotes_percentual=10.0, velocidade_download_mbps=2.0, velocidade_upload_mbps=1.0)
        await indicador_service.gerar_indicador_operadora(operadora_id=operadora.id, referencia_ano=date.today().year, referencia_mes=date.today().month)
        itens = await indicador_service.listar_indicadores(status=StatusIndicadorQualidade.CRITICO)
        assert len(itens) >= 1
    asyncio.run(scenario())