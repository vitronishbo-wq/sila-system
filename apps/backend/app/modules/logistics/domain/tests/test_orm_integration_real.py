from __future__ import annotations
from datetime import datetime, timedelta
from decimal import Decimal
import os
from uuid import uuid4
import pytest
import pytest_asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from app.modules.logistics.domain.enums import ModalTransporte, StatusFrota, StatusReconciliacaoFinanceira, StatusViagem, TipoVeiculo, TipoTarifa, TipoViagem
from app.modules.logistics.domain.models import BilhetagemEletronica, FiscalizacaoTransporte, Frota, Linha, Manutencao, Tarifa, Veiculo, Viagem
from app.modules.logistics.infrastructure.repositories import SQLAlchemyBilhetagemRepository, SQLAlchemyFrotaRepository, SQLAlchemyLinhaRepository, SQLAlchemyVeiculoRepository, SQLAlchemyViagemRepository
TABLES = ['transportes_logistica_viagens', 'transportes_logistica_frotas', 'transportes_logistica_linhas', 'transportes_logistica_veiculos', 'transportes_logistica_bilhetagem_eventos']

def _get_database_url() -> str:
    url = os.environ.get('DATABASE_URL', 'postgresql+asyncpg://sila_user:Trumanmarcelo_1983@127.0.0.1:5432/sila_db')
    if 'sqlite' in url:
        raise RuntimeError('Testes ORM reais exigem PostgreSQL')
    if url.startswith('postgresql://'):
        return url.replace('postgresql://', 'postgresql+asyncpg://', 1)
    return url

@pytest_asyncio.fixture
async def db_session() -> AsyncSession:
    engine = create_async_engine(_get_database_url(), echo=False, poolclass=NullPool)
    async with engine.connect() as conn:
        trans = await conn.begin()
        factory = sessionmaker(bind=conn, class_=AsyncSession, expire_on_commit=False, autocommit=False)
        async with factory() as session:
            await session.begin()
            try:
                yield session
            finally:
                try:
                    await session.rollback()
                except Exception:
                    pass
        try:
            await trans.rollback()
        except Exception:
            pass
    await engine.dispose()

async def _assert_table_exists(db_session: AsyncSession, table_name: str) -> None:
    result = await db_session.execute(text('SELECT to_regclass(:table_name)'), {'table_name': table_name})
    assert result.scalar_one_or_none() is not None, f'Tabela fisica ausente: {table_name}. Execute migration 20260304_039_transportes_logistica_linhas_bilhetagem.'

@pytest.mark.asyncio
@pytest.mark.integration
async def test_repositories_transportes_logistica_roundtrip_orm_real(db_session: AsyncSession) -> None:
    for table_name in TABLES:
        await _assert_table_exists(db_session, table_name)
    viagem_repo = SQLAlchemyViagemRepository(db_session)
    frota_repo = SQLAlchemyFrotaRepository(db_session)
    linha_repo = SQLAlchemyLinhaRepository(db_session)
    veiculo_repo = SQLAlchemyVeiculoRepository(db_session)
    bilhetagem_repo = SQLAlchemyBilhetagemRepository(db_session)
    veiculo = await veiculo_repo.save(Veiculo.cadastrar(placa='LD-20-30-AA', tipo=TipoVeiculo.ONIBUS, marca='Mercedes', modelo='O500', ano_fabricacao=2021, ano_modelo=2022, proprietario_id=uuid4(), proprietario_tipo='cnpj', data_aquisicao=datetime.utcnow().date(), capacidade_passageiros=72, operadora_id=uuid4()))
    linha = Linha.criar(codigo=await linha_repo.next_codigo(), nome='Linha ORM Real', modal=ModalTransporte.RODOVIARIO, tipo_viagem=TipoViagem.URBANA, origem='Luanda', destino='Cacuaco', itinerario=[{'ordem': 1, 'ponto': 'Mutamba'}], extensao_km=Decimal('24.00'), tempo_estimado_minutos=65, dias_operacao=['seg', 'ter', 'qua'], horario_inicio='05:00', horario_fim='22:00', tarifa_base=Decimal('250.00'), operadora_id=uuid4())
    linha.adicionar_veiculo(veiculo_id=veiculo.id, placa=veiculo.placa)
    linha = await linha_repo.save(linha)
    saida = datetime.utcnow()
    chegada_prevista = saida + timedelta(hours=2)
    viagem = await viagem_repo.save(Viagem.programar(linha_id=linha.id, veiculo_id=veiculo.id, motorista_id=uuid4(), data_hora_saida=saida, data_hora_chegada_prevista=chegada_prevista, origem='Luanda', destino='Bengo', itinerario=[{'ordem': 1, 'ponto': 'Cacuaco'}]))
    viagem.iniciar()
    viagem.concluir(chegada_prevista)
    viagem.passageiros_embarcados = 95
    await viagem_repo.save(viagem)
    evento_bilhetagem = await bilhetagem_repo.save(BilhetagemEletronica.registrar_evento(codigo_bilhete='ORM-TICKET-001', viagem_id=viagem.id, tipo_tarifa=TipoTarifa.PUBLICA, valor_pago=Decimal('250.00'), forma_pagamento='cartao'))
    evento_bilhetagem.vincular_lancamento('REC-ORM-001')
    evento_bilhetagem.confirmar_reconciliacao('BANK-ORM-001')
    await bilhetagem_repo.save(evento_bilhetagem)
    frota = Frota.criar(codigo_frota=await frota_repo.next_codigo(), nome='Frota ORM Real', operadora_id=uuid4(), municipio='Luanda', provincia='Luanda')
    frota.adicionar_veiculo(veiculo_id=uuid4(), placa='LD-90-11-AA', tipo='onibus', capacidade=80)
    frota.registrar_manutencao(Manutencao.registrar(veiculo_id=uuid4(), tipo='preventiva', oficina='Oficina ORM', custo=Decimal('100000.00')))
    frota.atualizar_tarifa(Tarifa.definir(tipo=TipoTarifa.PUBLICA, valor=Decimal('250.00'), motivo='Atualizacao anual'))
    frota.registrar_fiscalizacao(FiscalizacaoTransporte.registrar(fiscal_id=uuid4(), conformidade=True, apontamentos='Frota regular'))
    frota.registrar_evento_auditoria(evento='frota_roundtrip_orm_real')
    frota = await frota_repo.save(frota)
    viagem_db = await viagem_repo.get_by_id(viagem.id)
    frota_db = await frota_repo.get_by_codigo(frota.codigo_frota)
    linha_db = await linha_repo.get_by_codigo(linha.codigo)
    veiculo_db = await veiculo_repo.get_by_placa(veiculo.placa)
    bilhetagem_db = await bilhetagem_repo.get_by_id(evento_bilhetagem.id)
    assert viagem_db is not None
    assert viagem_db.status == StatusViagem.CONCLUIDA
    assert frota_db is not None
    assert frota_db.status == StatusFrota.ATIVA
    assert linha_db is not None
    assert linha_db.codigo == linha.codigo
    assert len(linha_db.veiculos_ativos) == 1
    assert veiculo_db is not None
    assert veiculo_db.placa == veiculo.placa
    assert bilhetagem_db is not None
    assert bilhetagem_db.status_reconciliacao == StatusReconciliacaoFinanceira.CONFIRMADO
    assert len(frota_db.veiculos) == 1
    assert len(frota_db.manutencoes) == 1
    assert len(frota_db.tarifas) == 1
    assert len(frota_db.fiscalizacoes) == 1
    assert len(frota_db.trilha_auditoria) >= 1
