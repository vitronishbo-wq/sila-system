from __future__ import annotations
from datetime import date, timedelta
from uuid import uuid4
import pytest
from apps.backend.app.modules.governance.cooperacao_internacional.application.services.acordo_service import AcordoService
from apps.backend.app.modules.governance.cooperacao_internacional.application.services.projeto_cooperacao_service import ProjetoCooperacaoService
from apps.backend.app.modules.governance.cooperacao_internacional.application.services.visto_service import VistoService
from apps.backend.app.modules.governance.cooperacao_internacional.domain.enums import CategoriaVisto, ModalidadeCooperacao, NaturezaJuridica, StatusAcordo, StatusVisto, TipoAcordo, TipoProjeto, TipoVisto
from apps.backend.app.modules.governance.cooperacao_internacional.infrastructure.persistence.outbox import InMemoryOutbox
from apps.backend.app.modules.governance.cooperacao_internacional.infrastructure.repositories.inmemory_acordo_repository import InMemoryAcordoRepository
from apps.backend.app.modules.governance.cooperacao_internacional.infrastructure.repositories.inmemory_projeto_repository import InMemoryProjetoCooperacaoRepository
from apps.backend.app.modules.governance.cooperacao_internacional.infrastructure.repositories.inmemory_visto_repository import InMemoryVistoRepository

@pytest.mark.asyncio
async def test_fluxo_acordo_com_eventos() -> None:
    repo = InMemoryAcordoRepository()
    outbox = InMemoryOutbox()
    service = AcordoService(acordo_repo=repo, outbox=outbox)
    acordo = await service.criar_acordo(titulo='Acordo de Cooperacao Tecnica Angola-Brasil', tipo=TipoAcordo.TRATADO, natureza=NaturezaJuridica.VINCULANTE, data_assinatura=date.today(), data_vigor=None, prazo_anos=5, objeto='Transferencia de conhecimento e formacao de quadros tecnicos')
    parte_a = uuid4()
    parte_b = uuid4()
    acordo = await service.assinar_acordo(acordo_id=acordo.id, local_assinatura='Luanda', partes=[{'entidade_id': parte_a, 'tipo_entidade': 'PAIS', 'data_adesao': date.today(), 'assinante': 'Ministro A', 'titulo_assinante': 'Ministro'}, {'entidade_id': parte_b, 'tipo_entidade': 'PAIS', 'data_adesao': date.today(), 'assinante': 'Ministro B', 'titulo_assinante': 'Ministro'}])
    assert acordo.status == StatusAcordo.ASSINADO
    await service.ratificar_acordo(acordo_id=acordo.id, data_ratificacao=date.today(), instrumento='Decreto X', parte_id=parte_a)
    acordo = await service.ratificar_acordo(acordo_id=acordo.id, data_ratificacao=date.today(), instrumento='Decreto Y', parte_id=parte_b)
    assert acordo.status == StatusAcordo.RATIFICADO
    acordo = await service.iniciar_vigor(acordo_id=acordo.id, data_vigor=date.today())
    assert acordo.status == StatusAcordo.EM_VIGOR
    eventos = await outbox.list_events()
    assert len(eventos) >= 3

@pytest.mark.asyncio
async def test_fluxo_projeto_e_visto() -> None:
    outbox = InMemoryOutbox()
    projeto_service = ProjetoCooperacaoService(projeto_repo=InMemoryProjetoCooperacaoRepository(), outbox=outbox)
    visto_service = VistoService(visto_repo=InMemoryVistoRepository(), outbox=outbox)
    projeto = await projeto_service.criar_projeto(titulo='Programa de Intercambio Cientifico CPLP', tipo=TipoProjeto.COOPERACAO_CIENTIFICA, modalidade=ModalidadeCooperacao.MULTILATERAL, acordo_base_id=None, orgao_responsavel_id=uuid4(), orgao_parceiro_id=uuid4(), pais_parceiro_id=uuid4(), data_inicio=date.today(), data_fim=date(date.today().year + 1, date.today().month, date.today().day), objetivo_geral='Fortalecer cooperacao cientifica entre universidades', objetivos_especificos=['Capacitacao', 'Pesquisa conjunta'], orcamento_total=500000.0, fonte_recursos='Fundo CPLP')
    projeto = await projeto_service.aprovar_projeto(projeto_id=projeto.id)
    assert projeto.status.value == 'aprovado'
    visto = await visto_service.solicitar_visto(tipo=TipoVisto.OFICIAL, categoria=CategoriaVisto.VITEM_II, solicitante_cpf='12345678900', solicitante_nome='Fulano Diplomata', solicitante_passaporte='P1234567', pais_origem_id=uuid4(), pais_destino_id=uuid4(), data_entrada_prevista=date.today(), data_saida_prevista=date.today() + timedelta(days=1), objetivo_viagem='Missao oficial de cooperacao', consulato_emissor_id=uuid4())
    visto = await visto_service.aprovar_visto(visto_id=visto.id, autoridade='Consul', validade_dias=120)
    visto = await visto_service.emitir_visto(visto_id=visto.id)
    assert visto.status == StatusVisto.EMITIDO