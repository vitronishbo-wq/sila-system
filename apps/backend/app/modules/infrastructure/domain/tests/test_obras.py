from __future__ import annotations
from datetime import date, timedelta
from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from apps.backend.app.modules.infrastructure.api.deps import get_obra_service
from apps.backend.app.modules.infrastructure.api.endpoints.obras import router as obras_router
from apps.backend.app.modules.infrastructure.application.services.obra_service import ObraService
from apps.backend.app.modules.infrastructure.domain.enums import NaturezaObra, StatusObra, TipoObra
from apps.backend.app.modules.infrastructure.domain.exceptions import ObraNotFoundError
from apps.backend.app.modules.infrastructure.infrastructure.repositories import SQLAlchemyObraRepository

@pytest.mark.asyncio
async def test_obra_service_fluxo_sucesso():
    service = ObraService(obra_repo=SQLAlchemyObraRepository())
    item = await service.criar(nome='Requalificacao Avenida Central', tipo=TipoObra.PAVIMENTACAO, natureza=NaturezaObra.NOVA, orgao_responsavel_id=uuid4(), orgao_responsavel_tipo='ministerio', valor_orcado=Decimal('2500000.00'), data_inicio_prevista=date.today(), data_fim_prevista=date.today() + timedelta(days=180), endereco='Avenida Central', bairro='Ingombota', municipio='Luanda', provincia='Luanda')
    assert item.status == StatusObra.PROJETO
    assert item.codigo_obra.startswith('OBR/')
    item = await service.iniciar_licitacao(item.codigo_obra)
    assert item.status == StatusObra.LICITACAO
    item = await service.contratar(item.codigo_obra, contrato_id=uuid4(), empreiteira_id=uuid4(), valor=Decimal('2300000.00'))
    assert item.status == StatusObra.CONTRATADA
    item = await service.iniciar_execucao(item.codigo_obra, data_inicio=date.today())
    assert item.status == StatusObra.EM_EXECUCAO
    item = await service.registrar_medicao_detalhada(item.codigo_obra, periodo_referencia='2026-03', valor_medido=Decimal('300000.00'), percentual_executado=Decimal('12.50'), fiscal_id=uuid4(), documentos=['medicao-marco.pdf'])
    assert len(item.medicoes) == 1
    assert item.percentual_executado == Decimal('12.50')
    item = await service.registrar_aditivo(item.codigo_obra, tipo='prazo', justificativa='Ajuste de cronograma por chuvas', prazo_adicional_dias=15)
    assert len(item.aditivos) == 1
    item = await service.registrar_fiscalizacao(item.codigo_obra, fiscal_id=uuid4(), conformidade=True, apontamentos='Execucao dentro das especificacoes')
    assert len(item.fiscalizacoes) == 1
    item = await service.atualizar_progresso(item.codigo_obra, percentual=Decimal('45.50'))
    assert item.percentual_executado == Decimal('45.50')
    item = await service.registrar_medicao(item.codigo_obra, valor=Decimal('500000.00'))
    assert item.valor_executado == Decimal('800000.00')
    item = await service.registrar_pagamento(item.codigo_obra, valor=Decimal('400000.00'))
    assert item.valor_pago == Decimal('400000.00')
    item = await service.concluir(item.codigo_obra, data_conclusao=date.today() + timedelta(days=170))
    assert item.status == StatusObra.CONCLUIDA
    item = await service.registrar_termo_recebimento(item.codigo_obra, tipo='definitivo', responsavel_id=uuid4(), data_termo=date.today() + timedelta(days=175))
    assert item.status == StatusObra.ENTREGUE
    assert len(item.termos_recebimento) == 1

@pytest.mark.asyncio
async def test_obra_service_integra_adapters_em_criacao_e_execucao():
    urbanismo_adapter = SimpleNamespace(validar_conformidade_urbanistica=AsyncMock(return_value=True))
    workflow_adapter = SimpleNamespace(iniciar_fluxo=AsyncMock(return_value='WF-OBRA-001'), registrar_evento=AsyncMock(return_value=None))
    service_requests_adapter = SimpleNamespace(abrir_solicitacao=AsyncMock(return_value='SRQ-OBRA-001'))
    ambiente_adapter = SimpleNamespace(validar_licenca_ambiental=AsyncMock(return_value=True))
    transportes_adapter = SimpleNamespace(validar_impacto_viario=AsyncMock(return_value=True))
    aguas_adapter = SimpleNamespace(validar_capacidade_rede=AsyncMock(return_value=True))
    financas_adapter = SimpleNamespace(reservar_dotacao=AsyncMock(return_value=True))
    service = ObraService(obra_repo=SQLAlchemyObraRepository(), financas_publicas_adapter=financas_adapter, ambiente_adapter=ambiente_adapter, urbanismo_habitacao_adapter=urbanismo_adapter, transportes_adapter=transportes_adapter, aguas_saneamento_adapter=aguas_adapter, workflow_adapter=workflow_adapter, service_requests_adapter=service_requests_adapter)
    item = await service.criar(nome='Requalificacao Avenida Circular', tipo=TipoObra.PAVIMENTACAO, natureza=NaturezaObra.NOVA, orgao_responsavel_id=uuid4(), orgao_responsavel_tipo='ministerio', valor_orcado=Decimal('1200000.00'), data_inicio_prevista=date.today(), data_fim_prevista=date.today() + timedelta(days=120), endereco='Avenida Circular', bairro='Maianga', municipio='Luanda', provincia='Luanda')
    assert 'service_request_id:SRQ-OBRA-001' in (item.observacoes or '')
    assert 'workflow_id:WF-OBRA-001' in (item.observacoes or '')
    item = await service.iniciar_licitacao(item.codigo_obra)
    assert item.status == StatusObra.LICITACAO
    item = await service.contratar(item.codigo_obra, contrato_id=uuid4(), empreiteira_id=uuid4(), valor=Decimal('1000000.00'))
    assert item.status == StatusObra.CONTRATADA
    item = await service.iniciar_execucao(item.codigo_obra, data_inicio=date.today())
    assert item.status == StatusObra.EM_EXECUCAO
    urbanismo_adapter.validar_conformidade_urbanistica.assert_awaited_once()
    service_requests_adapter.abrir_solicitacao.assert_awaited_once()
    workflow_adapter.iniciar_fluxo.assert_awaited_once()
    workflow_adapter.registrar_evento.assert_awaited()
    ambiente_adapter.validar_licenca_ambiental.assert_awaited_once()
    transportes_adapter.validar_impacto_viario.assert_awaited_once()
    aguas_adapter.validar_capacidade_rede.assert_awaited_once()

@pytest.mark.asyncio
async def test_obra_service_modo_outbox_nao_chama_adapters_externos_diretamente():
    urbanismo_adapter = SimpleNamespace(validar_conformidade_urbanistica=AsyncMock(return_value=True))
    workflow_adapter = SimpleNamespace(iniciar_fluxo=AsyncMock(return_value='WF-OBRA-OUTBOX-001'), registrar_evento=AsyncMock(return_value=None))
    service_requests_adapter = SimpleNamespace(abrir_solicitacao=AsyncMock(return_value='SRQ-OBRA-OUTBOX-001'))
    ambiente_adapter = SimpleNamespace(validar_licenca_ambiental=AsyncMock(return_value=True))
    transportes_adapter = SimpleNamespace(validar_impacto_viario=AsyncMock(return_value=True))
    aguas_adapter = SimpleNamespace(validar_capacidade_rede=AsyncMock(return_value=True))
    financas_adapter = SimpleNamespace(reservar_dotacao=AsyncMock(return_value=True))
    outbox_repo = SimpleNamespace(save=AsyncMock(return_value=uuid4()))
    service = ObraService(obra_repo=SQLAlchemyObraRepository(), financas_publicas_adapter=financas_adapter, ambiente_adapter=ambiente_adapter, urbanismo_habitacao_adapter=urbanismo_adapter, transportes_adapter=transportes_adapter, aguas_saneamento_adapter=aguas_adapter, workflow_adapter=workflow_adapter, service_requests_adapter=service_requests_adapter, outbox_repo=outbox_repo)
    item = await service.criar(nome='Obra Modo Outbox', tipo=TipoObra.PAVIMENTACAO, natureza=NaturezaObra.NOVA, orgao_responsavel_id=uuid4(), orgao_responsavel_tipo='ministerio', valor_orcado=Decimal('1200000.00'), data_inicio_prevista=date.today(), data_fim_prevista=date.today() + timedelta(days=120), endereco='Avenida Outbox', bairro='Maianga', municipio='Luanda', provincia='Luanda', tenant_id='tenant-obras', correlation_id='corr-obras-001')
    item = await service.iniciar_licitacao(item.codigo_obra)
    item = await service.contratar(item.codigo_obra, contrato_id=uuid4(), empreiteira_id=uuid4(), valor=Decimal('1000000.00'))
    await service.iniciar_execucao(item.codigo_obra, data_inicio=date.today(), tenant_id='tenant-obras', correlation_id='corr-obras-002')
    financas_adapter.reservar_dotacao.assert_not_awaited()
    urbanismo_adapter.validar_conformidade_urbanistica.assert_not_awaited()
    ambiente_adapter.validar_licenca_ambiental.assert_not_awaited()
    transportes_adapter.validar_impacto_viario.assert_not_awaited()
    aguas_adapter.validar_capacidade_rede.assert_not_awaited()
    service_requests_adapter.abrir_solicitacao.assert_not_awaited()
    workflow_adapter.iniciar_fluxo.assert_not_awaited()
    workflow_adapter.registrar_evento.assert_not_awaited()
    assert outbox_repo.save.await_count >= 2

def test_endpoint_criar_obra_retorna_201():
    mock_item = SimpleNamespace(id=uuid4(), codigo_obra='OBR/2026/000001', nome='Requalificacao Avenida Central', tipo=TipoObra.PAVIMENTACAO, natureza=NaturezaObra.NOVA, status=StatusObra.PROJETO, orgao_responsavel_id=uuid4(), orgao_responsavel_tipo='ministerio', valor_orcado=Decimal('2500000.00'), data_inicio_prevista=date(2026, 3, 1), data_fim_prevista=date(2026, 8, 28), endereco='Avenida Central', bairro='Ingombota', municipio='Luanda', provincia='Luanda', prazo_original_dias=180, data_cadastro=date(2026, 3, 1), descricao=None, gestor_responsavel_id=None, fiscal_responsavel_id=None, empreiteira_id=None, contrato_id=None, projeto_id=None, valor_contratado=None, valor_executado=None, valor_pago=None, data_inicio_real=None, data_fim_real=None, data_entrega=None, coordenadas_lat=None, coordenadas_long=None, imovel_id=None, percentual_executado=Decimal('0.00'), prazo_adicionado_dias=0, dias_corridos=0, dias_atraso=0, data_atualizacao=None, observacoes=None)
    service = SimpleNamespace(criar=AsyncMock(return_value=mock_item))
    app = FastAPI()
    app.include_router(obras_router, prefix='/obras-publicas')
    app.dependency_overrides[get_obra_service] = lambda: service
    client = TestClient(app)
    response = client.post('/obras-publicas/obras/', json={'nome': 'Requalificacao Avenida Central', 'tipo': 'pavimentacao', 'natureza': 'nova', 'orgao_responsavel_id': str(uuid4()), 'orgao_responsavel_tipo': 'ministerio', 'valor_orcado': '2500000.00', 'data_inicio_prevista': '2026-03-01', 'data_fim_prevista': '2026-08-28', 'endereco': 'Avenida Central', 'bairro': 'Ingombota', 'municipio': 'Luanda', 'provincia': 'Luanda'})
    assert response.status_code == 201
    assert response.json()['codigo_obra'] == 'OBR/2026/000001'

def test_endpoint_criar_obra_propaga_tenant_e_correlation():
    mock_item = SimpleNamespace(id=uuid4(), codigo_obra='OBR/2026/000001', nome='Requalificacao Avenida Central', tipo=TipoObra.PAVIMENTACAO, natureza=NaturezaObra.NOVA, status=StatusObra.PROJETO, orgao_responsavel_id=uuid4(), orgao_responsavel_tipo='ministerio', valor_orcado=Decimal('2500000.00'), data_inicio_prevista=date(2026, 3, 1), data_fim_prevista=date(2026, 8, 28), endereco='Avenida Central', bairro='Ingombota', municipio='Luanda', provincia='Luanda', prazo_original_dias=180, data_cadastro=date(2026, 3, 1), percentual_executado=Decimal('0.00'), prazo_adicionado_dias=0, dias_corridos=0, dias_atraso=0, descricao=None, gestor_responsavel_id=None, fiscal_responsavel_id=None, empreiteira_id=None, contrato_id=None, projeto_id=None, valor_contratado=None, valor_executado=None, valor_pago=None, data_inicio_real=None, data_fim_real=None, data_entrega=None, coordenadas_lat=None, coordenadas_long=None, imovel_id=None, data_atualizacao=None, observacoes=None, medicoes=[], aditivos=[], fiscalizacoes=[], termos_recebimento=[], trilha_auditoria=[])
    service = SimpleNamespace(criar=AsyncMock(return_value=mock_item))
    app = FastAPI()
    app.include_router(obras_router, prefix='/obras-publicas')
    app.dependency_overrides[get_obra_service] = lambda: service
    client = TestClient(app)
    response = client.post('/obras-publicas/obras/', headers={'X-Tenant-ID': 'tenant-obras', 'X-Correlation-ID': 'corr-obras-123'}, json={'nome': 'Requalificacao Avenida Central', 'tipo': 'pavimentacao', 'natureza': 'nova', 'orgao_responsavel_id': str(uuid4()), 'orgao_responsavel_tipo': 'ministerio', 'valor_orcado': '2500000.00', 'data_inicio_prevista': '2026-03-01', 'data_fim_prevista': '2026-08-28', 'endereco': 'Avenida Central', 'bairro': 'Ingombota', 'municipio': 'Luanda', 'provincia': 'Luanda'})
    assert response.status_code == 201
    service.criar.assert_awaited_once()
    called_kwargs = service.criar.await_args.kwargs
    assert called_kwargs['tenant_id'] == 'tenant-obras'
    assert called_kwargs['correlation_id'] == 'corr-obras-123'

def test_endpoint_obter_obra_retorna_404():
    service = SimpleNamespace(obter_por_codigo=AsyncMock(side_effect=ObraNotFoundError('Obra nao encontrada')))
    app = FastAPI()
    app.include_router(obras_router, prefix='/obras-publicas')
    app.dependency_overrides[get_obra_service] = lambda: service
    client = TestClient(app)
    response = client.get('/obras-publicas/obras/OBR/2026/999999')
    assert response.status_code == 404
    assert response.json()['detail'] == 'Obra nao encontrada'

def test_endpoint_event_stream_e_rehydrate_com_codigo_path():
    service = SimpleNamespace(obter_event_stream=AsyncMock(return_value=[{'id': str(uuid4()), 'aggregate_id': 'obra-1', 'aggregate_type': 'Obra', 'event_type': 'ObraIniciadaEvent', 'event_data': {'obra_id': 'obra-1'}, 'version': 1, 'tenant_id': 'tenant-obras', 'region_code': 'A', 'correlation_id': 'corr-1', 'created_at': '2026-03-05T00:00:00+00:00'}]), rehidratar_estado_obra=AsyncMock(return_value={'obra_id': 'obra-1', 'codigo_obra': 'OBR/2026/000001', 'status': 'EM_EXECUCAO', 'valor_total': '1000.00', 'valor_executado': '250.00', 'event_count': 1}))
    app = FastAPI()
    app.include_router(obras_router, prefix='/obras-publicas')
    app.dependency_overrides[get_obra_service] = lambda: service
    client = TestClient(app)
    stream_response = client.get('/obras-publicas/obras/OBR/2026/000001/event-stream', headers={'X-Tenant-ID': 'tenant-obras'})
    rehydrate_response = client.get('/obras-publicas/obras/OBR/2026/000001/rehydrate', headers={'X-Tenant-ID': 'tenant-obras'})
    assert stream_response.status_code == 200
    assert stream_response.json()[0]['event_type'] == 'ObraIniciadaEvent'
    assert rehydrate_response.status_code == 200
    assert rehydrate_response.json()['status'] == 'EM_EXECUCAO'
    service.obter_event_stream.assert_awaited_once_with('OBR/2026/000001', tenant_id='tenant-obras')
    service.rehidratar_estado_obra.assert_awaited_once_with('OBR/2026/000001', tenant_id='tenant-obras')

def test_endpoint_criar_obra_sem_adapter_critico_retorna_503():
    service = SimpleNamespace(criar=AsyncMock())
    service.has_urbanismo_habitacao_adapter = lambda: False
    service.has_workflow_adapter = lambda: True
    service.has_service_requests_adapter = lambda: True
    app = FastAPI()
    app.include_router(obras_router, prefix='/obras-publicas')
    app.dependency_overrides[get_obra_service] = lambda: service
    client = TestClient(app)
    response = client.post('/obras-publicas/obras/', json={'nome': 'Requalificacao Avenida Central', 'tipo': 'pavimentacao', 'natureza': 'nova', 'orgao_responsavel_id': str(uuid4()), 'orgao_responsavel_tipo': 'ministerio', 'valor_orcado': '2500000.00', 'data_inicio_prevista': '2026-03-01', 'data_fim_prevista': '2026-08-28', 'endereco': 'Avenida Central', 'bairro': 'Ingombota', 'municipio': 'Luanda', 'provincia': 'Luanda'})
    assert response.status_code == 503
    assert 'Urbanismo Habitacao indisponivel' in response.json()['detail']
    service.criar.assert_not_awaited()

def test_endpoint_iniciar_execucao_sem_adapter_critico_retorna_503():
    service = SimpleNamespace(iniciar_execucao=AsyncMock())
    service.has_ambiente_adapter = lambda: True
    service.has_transportes_adapter = lambda: False
    service.has_aguas_saneamento_adapter = lambda: True
    app = FastAPI()
    app.include_router(obras_router, prefix='/obras-publicas')
    app.dependency_overrides[get_obra_service] = lambda: service
    client = TestClient(app)
    response = client.post('/obras-publicas/obras/OBR/2026/000001/iniciar-execucao', json={'data_inicio': '2026-03-20'})
    assert response.status_code == 503
    assert 'Transportes indisponivel' in response.json()['detail']
    service.iniciar_execucao.assert_not_awaited()

def test_endpoint_fluxo_execucao_expandido_com_trilha_auditavel():
    urbanismo_adapter = SimpleNamespace(validar_conformidade_urbanistica=AsyncMock(return_value=True))
    workflow_adapter = SimpleNamespace(iniciar_fluxo=AsyncMock(return_value='WF-OBRA-E2E-001'), registrar_evento=AsyncMock(return_value=None))
    service_requests_adapter = SimpleNamespace(abrir_solicitacao=AsyncMock(return_value='SRQ-OBRA-E2E-001'))
    ambiente_adapter = SimpleNamespace(validar_licenca_ambiental=AsyncMock(return_value=True))
    transportes_adapter = SimpleNamespace(validar_impacto_viario=AsyncMock(return_value=True))
    aguas_adapter = SimpleNamespace(validar_capacidade_rede=AsyncMock(return_value=True))
    financas_adapter = SimpleNamespace(reservar_dotacao=AsyncMock(return_value=True))
    service = ObraService(obra_repo=SQLAlchemyObraRepository(), financas_publicas_adapter=financas_adapter, ambiente_adapter=ambiente_adapter, urbanismo_habitacao_adapter=urbanismo_adapter, transportes_adapter=transportes_adapter, aguas_saneamento_adapter=aguas_adapter, workflow_adapter=workflow_adapter, service_requests_adapter=service_requests_adapter)
    app = FastAPI()
    app.include_router(obras_router, prefix='/obras-publicas')
    app.dependency_overrides[get_obra_service] = lambda: service
    client = TestClient(app)
    create_response = client.post('/obras-publicas/obras/', json={'nome': 'Terminal Rodoviario Central', 'tipo': 'construcao', 'natureza': 'nova', 'orgao_responsavel_id': str(uuid4()), 'orgao_responsavel_tipo': 'ministerio', 'valor_orcado': '5000000.00', 'data_inicio_prevista': '2026-03-05', 'data_fim_prevista': '2026-11-30', 'endereco': 'Av. Principal', 'bairro': 'Centro', 'municipio': 'Luanda', 'provincia': 'Luanda'})
    assert create_response.status_code == 201
    codigo = create_response.json()['codigo_obra']
    licitacao_response = client.post(f'/obras-publicas/obras/{codigo}/iniciar-licitacao')
    assert licitacao_response.status_code == 200
    contratacao_response = client.post(f'/obras-publicas/obras/{codigo}/contratar', json={'contrato_id': str(uuid4()), 'empreiteira_id': str(uuid4()), 'valor_contratado': '4800000.00'})
    assert contratacao_response.status_code == 200
    execucao_response = client.post(f'/obras-publicas/obras/{codigo}/iniciar-execucao', json={'data_inicio': '2026-03-10'})
    assert execucao_response.status_code == 200
    medicao_response = client.post(f'/obras-publicas/obras/{codigo}/medicao-detalhada', json={'periodo_referencia': '2026-03', 'valor_medido': '350000.00', 'percentual_executado': '15.00', 'fiscal_id': str(uuid4()), 'documentos': ['medicao-2026-03.pdf'], 'observacoes': 'Primeira medicao validada'})
    assert medicao_response.status_code == 200
    aditivo_response = client.post(f'/obras-publicas/obras/{codigo}/aditivo', json={'tipo': 'prazo', 'justificativa': 'Interferencia de rede subterranea', 'prazo_adicional_dias': 20})
    assert aditivo_response.status_code == 200
    fiscalizacao_response = client.post(f'/obras-publicas/obras/{codigo}/fiscalizacao', json={'fiscal_id': str(uuid4()), 'conformidade': True, 'apontamentos': 'Sem nao conformidades'})
    assert fiscalizacao_response.status_code == 200
    conclusao_response = client.post(f'/obras-publicas/obras/{codigo}/concluir', json={'data_conclusao': '2026-11-20'})
    assert conclusao_response.status_code == 200
    termo_response = client.post(f'/obras-publicas/obras/{codigo}/termo-recebimento', json={'tipo': 'definitivo', 'responsavel_id': str(uuid4()), 'data_termo': '2026-11-25', 'observacoes': 'Obra recebida definitivamente'})
    assert termo_response.status_code == 200
    assert termo_response.json()['status'] == 'entregue'
    assert len(termo_response.json()['trilha_auditoria']) >= 7
    assert workflow_adapter.iniciar_fluxo.await_count == 1
    assert workflow_adapter.registrar_evento.await_count >= 7