from __future__ import annotations
from datetime import datetime
import pytest
from app.modules.intelligence.defesa_consumidor.application.services.reclamacao_service import ReclamacaoService

class _FakeEventBus:

    def __init__(self):
        self.events = []

    async def publish(self, event_name: str, payload: dict) -> None:
        self.events.append((event_name, payload))

class _FakeRepo:

    def __init__(self):
        self._db = {}
        self._id = 1

    async def create(self, data):
        record = {'id': self._id, 'criado_em': datetime.utcnow(), 'atualizado_em': datetime.utcnow(), 'data_abertura': datetime.utcnow(), 'resolvido': False, 'data_resolucao': None, 'descricao_resposta': None, **data}
        self._db[self._id] = record
        self._id += 1
        return record

    async def get_by_id(self, reclamacao_id):
        return self._db.get(reclamacao_id)

    async def get_by_protocolo(self, protocolo):
        for rec in self._db.values():
            if rec['protocolo'] == protocolo:
                return rec
        return None

    async def list_by_consumidor(self, consumidor_id, limit=50, offset=0):
        return [r for r in self._db.values() if r['consumidor_id'] == consumidor_id][:limit]

    async def list_by_estabelecimento(self, estabelecimento_id, limit=50, offset=0):
        return [r for r in self._db.values() if r['estabelecimento_id'] == estabelecimento_id][:limit]

    async def list_by_status(self, status, limit=100, offset=0):
        return [r for r in self._db.values() if r['status'] == status][:limit]

    async def list_by_periodo(self, data_inicio, data_fim):
        return list(self._db.values())

    async def list_prioritarias(self, prioridade, limit=50):
        return [r for r in self._db.values() if r['prioridade'] == prioridade and (not r['resolvido'])][:limit]

    async def update(self, data):
        rec = self._db[data['id']]
        rec.update(data)
        rec['atualizado_em'] = datetime.utcnow()
        return rec

    async def delete(self, reclamacao_id):
        return self._db.pop(reclamacao_id, None) is not None

    async def count_by_status(self, status):
        return len([r for r in self._db.values() if r['status'] == status])

    async def count_total(self):
        return len(self._db)

@pytest.mark.asyncio
async def test_fluxo_reclamacao_basico():
    repo = _FakeRepo()
    events = _FakeEventBus()
    service = ReclamacaoService(repo, event_bus=events)
    created = await service.criar_reclamacao({'consumidor_id': 1, 'estabelecimento_id': 2, 'produto_servico': 'Notebook XY', 'descricao': 'Produto sem funcionar apos 3 dias', 'categoria': 'produto_defectuoso', 'valor_reclamado': 1500.0, 'prioridade': 'media'})
    assert created['id'] == 1
    assert created['status'] == 'aberta'
    updated = await service.atualizar_status(1, 'em_analise')
    assert updated['status'] == 'em_analise'
    escalada = await service.escalar_prioridade(1)
    assert escalada['prioridade'] == 'alta'
    encerrada = await service.finalizar_reclamacao(1, True, 'Resolvido')
    assert encerrada['resolvido'] is True
    assert encerrada['status'] == 'encerrada'
    assert len(events.events) >= 4