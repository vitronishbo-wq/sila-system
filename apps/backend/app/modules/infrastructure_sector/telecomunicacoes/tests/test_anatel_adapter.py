from __future__ import annotations
import asyncio
import json
from datetime import datetime, timezone
from decimal import Decimal
from uuid import uuid4
import httpx
import pytest
from app.modules.infrastructure_sector.telecomunicacoes.application.events.definitions import QualidadeServicoAferidaEvent, ReclamacaoTelecomAbertaEvent
from app.modules.infrastructure_sector.telecomunicacoes.application.handlers.anatel_handler import AnatelHandler
from app.modules.infrastructure_sector.telecomunicacoes.infrastructure.adapters.anatel_adapter import AnatelAdapter

class FakeResponse:

    def __init__(self, *, status_code: int=200, json_body: dict | None=None, text_body: str='', content_type: str='application/json') -> None:
        self.status_code = status_code
        self.headers = {'content-type': content_type}
        self._json_body = json_body
        if json_body is not None:
            self.content = json.dumps(json_body).encode('utf-8')
            self.text = json.dumps(json_body)
        else:
            self.content = text_body.encode('utf-8')
            self.text = text_body

    def json(self):
        return self._json_body

    def raise_for_status(self) -> None:
        if self.status_code < 400:
            return
        request = httpx.Request('POST', 'http://anatel.local')
        response = httpx.Response(status_code=self.status_code, request=request)
        raise httpx.HTTPStatusError(message=f'status={self.status_code}', request=request, response=response)

class FakeHttpClient:

    def __init__(self, *, responses: list[FakeResponse] | None=None, error: Exception | None=None) -> None:
        self._responses = responses or []
        self._error = error
        self.calls: list[dict] = []

    async def request(self, *, method: str, url: str, json: dict, headers: dict, timeout: float):
        self.calls.append({'method': method, 'url': url, 'json': dict(json), 'headers': dict(headers), 'timeout': timeout})
        if self._error is not None:
            raise self._error
        if self._responses:
            return self._responses.pop(0)
        return FakeResponse(json_body={'status': 'accepted'})

def test_anatel_adapter_envia_reclamacao_com_circuit_breaker() -> None:

    async def scenario() -> None:
        client = FakeHttpClient(responses=[FakeResponse(json_body={'status': 'accepted', 'id': 'ANATEL-1'})])
        adapter = AnatelAdapter(base_url='http://anatel.local', api_key='secret-token', timeout_seconds=5.0, client=client)
        response = await adapter.registrar_reclamacao({'protocolo': 'REC/2026/0001', 'assinante_id': '9b8d4ab7-cc74-4705-ae93-8a23f8c8d910', 'prioridade': 'alta'})
        assert response['status'] == 'accepted'
        assert client.calls[0]['url'] == 'http://anatel.local/api/v1/reclamacoes'
        assert client.calls[0]['headers']['Authorization'] == 'Bearer secret-token'
    asyncio.run(scenario())

def test_anatel_adapter_abre_circuito_apos_falhas() -> None:

    async def scenario() -> None:
        request = httpx.Request('POST', 'http://anatel.local/api/v1/reclamacoes')
        client = FakeHttpClient(error=httpx.ConnectError('offline', request=request))
        adapter = AnatelAdapter(base_url='http://anatel.local', client=client, failure_threshold=2, recovery_timeout=60)
        payload = {'protocolo': 'REC/2026/0002', 'assinante_id': '406a08f6-88b0-43e2-a6cc-1f4122fd2d55', 'prioridade': 'media'}
        with pytest.raises(RuntimeError, match='comunicacao'):
            await adapter.registrar_reclamacao(payload)
        with pytest.raises(RuntimeError, match='comunicacao'):
            await adapter.registrar_reclamacao(payload)
        with pytest.raises(RuntimeError, match='Circuit OPEN'):
            await adapter.registrar_reclamacao(payload)
        assert len(client.calls) == 2
    asyncio.run(scenario())

def test_anatel_handler_publica_reclamacao_e_qualidade_nao_conforme() -> None:

    class StubAnatelAdapter:

        def __init__(self) -> None:
            self.reclamacoes: list[dict] = []
            self.qualidades: list[dict] = []

        async def registrar_reclamacao(self, payload: dict) -> dict:
            self.reclamacoes.append(payload)
            return {'status': 'accepted'}

        async def registrar_alerta_qualidade(self, payload: dict) -> dict:
            self.qualidades.append(payload)
            return {'status': 'accepted'}

    async def scenario() -> None:
        adapter = StubAnatelAdapter()
        handler = AnatelHandler(anatel_adapter=adapter)
        await handler.on_reclamacao_aberta(ReclamacaoTelecomAbertaEvent(event_id=uuid4(), timestamp=datetime.now(timezone.utc), reclamacao_id=uuid4(), protocolo='REC/2026/0099', assinante_id=uuid4(), tipo='cobertura', prioridade='alta'))
        await handler.on_qualidade_aferida(QualidadeServicoAferidaEvent(event_id=uuid4(), timestamp=datetime.now(timezone.utc), assinante_id=uuid4(), referencia='2026-03', download_mbps=Decimal('8.00'), upload_mbps=Decimal('1.50'), latencia_ms=Decimal('210.00'), conforme=False))
        await handler.on_qualidade_aferida(QualidadeServicoAferidaEvent(event_id=uuid4(), timestamp=datetime.now(timezone.utc), assinante_id=uuid4(), referencia='2026-03', download_mbps=Decimal('150.00'), upload_mbps=Decimal('50.00'), latencia_ms=Decimal('32.00'), conforme=True))
        assert len(handler.records) == 2
        assert len(adapter.reclamacoes) == 1
        assert len(adapter.qualidades) == 1
    asyncio.run(scenario())