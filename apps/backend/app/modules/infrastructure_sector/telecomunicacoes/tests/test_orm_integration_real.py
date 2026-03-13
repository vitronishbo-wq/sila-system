from __future__ import annotations
import asyncio
from contextlib import asynccontextmanager
from datetime import date
from uuid import uuid4
import pytest
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from apps.backend.app.domain.db import AsyncSessionLocal, Base, engine
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.application.services.assinante_service import AssinanteService
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.application.services.espectro_service import EspectroService
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.application.services.indicador_qualidade_service import IndicadorQualidadeService
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.application.services.infraestrutura_service import InfraestruturaService
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.application.services.operadora_service import OperadoraService
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.application.services.outorga_espectro_service import OutorgaEspectroService
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.application.services.qualidade_servico_service import QualidadeServicoService
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.application.services.sla_service import SLAService
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.domain.enums import TipoEspectro, TipoInfraestrutura, TipoOperadora, TipoOutorga, TipoPlano, TipoServico
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.tests._fakes import FakeCitizenService

def _tables():
    from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.infrastructure.models.assinante_model import AssinanteModel
    from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.infrastructure.models.espectro_model import EspectroModel
    from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.infrastructure.models.indicador_qualidade_model import IndicadorQualidadeModel
    from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.infrastructure.models.infraestrutura_telco_model import InfraestruturaTelcoModel
    from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.infrastructure.models.operadora_model import OperadoraModel
    from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.infrastructure.models.outorga_espectro_model import OutorgaEspectroModel
    from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.infrastructure.models.qualidade_servico_model import QualidadeServicoModel
    from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.infrastructure.models.sla_model import SLAModel
    if not hasattr(OperadoraModel, '__table__'):
        pytest.skip('ORM mappers limpos por conftest global apos import de modelos; executar este teste sem tests/conftest ou revisar clear_mappers global.')
    return [OperadoraModel.__table__, AssinanteModel.__table__, InfraestruturaTelcoModel.__table__, OutorgaEspectroModel.__table__, EspectroModel.__table__, SLAModel.__table__, QualidadeServicoModel.__table__, IndicadorQualidadeModel.__table__]

async def _ensure_schema() -> None:
    async with engine.begin() as conn:
        try:
            await conn.run_sync(lambda sync_conn: Base.metadata.create_all(sync_conn, tables=_tables()))
        except IntegrityError as exc:
            if 'pg_type_typname_nsp_index' not in str(exc):
                raise
            await conn.execute(text('DROP TABLE IF EXISTS telecom_espectro CASCADE'))
            await conn.execute(text('DROP TABLE IF EXISTS telecom_indicadores_qualidade CASCADE'))
            await conn.execute(text('DROP TABLE IF EXISTS telecom_qualidade_servico CASCADE'))
            await conn.execute(text('DROP TABLE IF EXISTS telecom_slas CASCADE'))
            await conn.execute(text('DROP TABLE IF EXISTS telecom_outorgas_espectro CASCADE'))
            await conn.execute(text('DROP TABLE IF EXISTS telecom_infraestruturas CASCADE'))
            await conn.execute(text('DROP TABLE IF EXISTS telecom_assinantes CASCADE'))
            await conn.execute(text('DROP TABLE IF EXISTS telecom_operadoras CASCADE'))
            await conn.execute(text('DROP TYPE IF EXISTS telecom_espectro CASCADE'))
            await conn.execute(text('DROP TYPE IF EXISTS telecom_outorgas_espectro CASCADE'))
            await conn.execute(text('DROP TYPE IF EXISTS telecom_infraestruturas CASCADE'))
            await conn.execute(text('DROP TYPE IF EXISTS telecom_assinantes CASCADE'))
            await conn.execute(text('DROP TYPE IF EXISTS telecom_operadoras CASCADE'))
            await conn.run_sync(lambda sync_conn: Base.metadata.create_all(sync_conn, tables=_tables()))

async def _clear_data(session: AsyncSession) -> None:
    await session.execute(text('DELETE FROM telecom_indicadores_qualidade'))
    await session.execute(text('DELETE FROM telecom_qualidade_servico'))
    await session.execute(text('DELETE FROM telecom_slas'))
    await session.execute(text('DELETE FROM telecom_espectro'))
    await session.execute(text('DELETE FROM telecom_outorgas_espectro'))
    await session.execute(text('DELETE FROM telecom_infraestruturas'))
    await session.execute(text('DELETE FROM telecom_assinantes'))
    await session.execute(text('DELETE FROM telecom_operadoras'))
    await session.commit()

@asynccontextmanager
async def _session_scope():
    await _ensure_schema()
    async with AsyncSessionLocal() as session:
        await _clear_data(session)
        try:
            yield session
        finally:
            await _clear_data(session)

@pytest.mark.integration
def test_fluxo_real_orm_telecom_completo_com_qualidade_sla_indicadores() -> None:

    async def scenario() -> None:
        async with _session_scope() as session:
            from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.infrastructure.repositories.sqlalchemy_assinante_repository import SQLAlchemyAssinanteRepository
            from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.infrastructure.repositories.sqlalchemy_espectro_repository import SQLAlchemyEspectroRepository
            from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.infrastructure.repositories.sqlalchemy_indicador_qualidade_repository import SQLAlchemyIndicadorQualidadeRepository
            from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.infrastructure.repositories.sqlalchemy_infraestrutura_repository import SQLAlchemyInfraestruturaRepository
            from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.infrastructure.repositories.sqlalchemy_operadora_repository import SQLAlchemyOperadoraRepository
            from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.infrastructure.repositories.sqlalchemy_outorga_espectro_repository import SQLAlchemyOutorgaEspectroRepository
            from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.infrastructure.repositories.sqlalchemy_qualidade_servico_repository import SQLAlchemyQualidadeServicoRepository
            from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.infrastructure.repositories.sqlalchemy_sla_repository import SQLAlchemySLARepository
            operadora_repo = SQLAlchemyOperadoraRepository(session)
            assinante_repo = SQLAlchemyAssinanteRepository(session)
            infraestrutura_repo = SQLAlchemyInfraestruturaRepository(session)
            outorga_repo = SQLAlchemyOutorgaEspectroRepository(session)
            espectro_repo = SQLAlchemyEspectroRepository(session)
            sla_repo = SQLAlchemySLARepository(session)
            qualidade_repo = SQLAlchemyQualidadeServicoRepository(session)
            indicador_repo = SQLAlchemyIndicadorQualidadeRepository(session)
            operadora_service = OperadoraService(operadora_repo=operadora_repo)
            assinante_service = AssinanteService(assinante_repo=assinante_repo, operadora_repo=operadora_repo, citizen_service=FakeCitizenService(active=True))
            infraestrutura_service = InfraestruturaService(infraestrutura_repo=infraestrutura_repo, operadora_repo=operadora_repo)
            outorga_service = OutorgaEspectroService(outorga_repo=outorga_repo, operadora_repo=operadora_repo)
            espectro_service = EspectroService(espectro_repo=espectro_repo, outorga_repo=outorga_repo)
            sla_service = SLAService(sla_repo=sla_repo, operadora_repo=operadora_repo)
            qualidade_service = QualidadeServicoService(qualidade_repo=qualidade_repo, sla_repo=sla_repo, operadora_repo=operadora_repo, assinante_repo=assinante_repo)
            indicador_service = IndicadorQualidadeService(indicador_repo=indicador_repo, qualidade_repo=qualidade_repo, operadora_repo=operadora_repo)
            operadora = await operadora_service.cadastrar_operadora(cnpj='44.444.444/0001-44', razao_social='Fibra Angola SA', tipo=TipoOperadora.PROVEDOR, servicos_autorizados=[TipoServico.INTERNET_FIXA, TipoServico.INTERNET_MOVEL], endereco='Avenida Digital, 1', municipio='Luanda', provincia='Luanda', telefone='222444444', email='operacao@fibra.ao', representante_legal='Rita Almeida', representante_documento='44455566677', representante_cargo='Diretora')
            assinante = await assinante_service.cadastrar_assinante(operadora_id=operadora.id, tipo_plano=TipoPlano.EMPRESARIAL, servico_principal=TipoServico.INTERNET_FIXA, municipio='Luanda', provincia='Luanda', citizen_id=uuid4(), contrato_numero='CTR-2026-0001', valor_mensal=85000.0)
            infraestrutura = await infraestrutura_service.cadastrar_infraestrutura(operadora_id=operadora.id, tipo=TipoInfraestrutura.FIBRA_OPTICA, identificador='FIB-LDA-ORM', municipio='Luanda', provincia='Luanda', data_implantacao=date.today())
            outorga = await outorga_service.emitir_outorga(operadora_id=operadora.id, tipo_outorga=TipoOutorga.AUTORIZACAO, faixa_inicio_mhz=3400.0, faixa_fim_mhz=3600.0, data_outorga=date.today())
            espectro = await espectro_service.registrar_espectro(tipo=TipoEspectro.BANDA_LARGA, frequencia_inicial_mhz=3400.0, frequencia_final_mhz=3600.0, servico_principal=TipoServico.INTERNET_MOVEL, municipio='Luanda', provincia='Luanda', outorga_id=outorga.id)
            sla = await sla_service.criar_sla(operadora_id=operadora.id, nome='SLA Integra Telecom', servico=TipoServico.INTERNET_FIXA, disponibilidade_min_percentual=99.0, latencia_max_ms=60.0, jitter_max_ms=20.0, perda_pacotes_max_percentual=1.0, velocidade_download_min_mbps=100.0, velocidade_upload_min_mbps=50.0, data_inicio=date.today())
            medicao = await qualidade_service.registrar_medicao(operadora_id=operadora.id, assinante_id=assinante.id, sla_id=sla.id, servico=TipoServico.INTERNET_FIXA, data_medicao=date.today(), disponibilidade_percentual=99.3, latencia_ms=40.0, jitter_ms=15.0, perda_pacotes_percentual=0.4, velocidade_download_mbps=180.0, velocidade_upload_mbps=90.0)
            indicador = await indicador_service.gerar_indicador_operadora(operadora_id=operadora.id, referencia_ano=date.today().year, referencia_mes=date.today().month)
            fetched_operadora = await operadora_service.buscar_operadora(operadora.id)
            fetched_assinante = await assinante_service.buscar_assinante(assinante.id)
            fetched_infra = await infraestrutura_service.buscar_infraestrutura(infraestrutura.id)
            fetched_outorga = await outorga_service.buscar_outorga(outorga.id)
            fetched_espectro = await espectro_service.buscar_espectro(espectro.id)
            fetched_sla = await sla_service.buscar_sla(sla.id)
            fetched_medicao = await qualidade_service.buscar_medicao(medicao.id)
            fetched_indicador = await indicador_service.buscar_indicador(indicador.id)
            assert fetched_operadora.cnpj == '44.444.444/0001-44'
            assert fetched_assinante.codigo_assinante.startswith('ASS/')
            assert fetched_infra.codigo_infra.startswith('INF/')
            assert fetched_outorga.numero_outorga.startswith('OUT/')
            assert fetched_espectro.codigo_espectro.startswith('ESP/')
            assert fetched_espectro.outorga_id == fetched_outorga.id
            assert fetched_sla.codigo_sla.startswith('SLA/')
            assert fetched_medicao.codigo_medicao.startswith('QLT/')
            assert fetched_indicador.codigo_indicador.startswith('IND/')
            assert fetched_indicador.total_medicoes >= 1
    asyncio.run(scenario())