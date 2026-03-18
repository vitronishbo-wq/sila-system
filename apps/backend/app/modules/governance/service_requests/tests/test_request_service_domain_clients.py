from __future__ import annotations
from unittest.mock import AsyncMock
from uuid import uuid4
import pytest
from apps.backend.app.modules.governance.service_requests.application.services.request_service import RequestService
from apps.backend.app.modules.governance.service_requests.domain.enums import RequestChannel, RequestPriority, ServiceType

@pytest.mark.asyncio
async def test_create_request_uses_identity_validation_first() -> None:
    repo = AsyncMock()
    repo.get_next_sequence.return_value = 1
    identidade_client = AsyncMock()
    identidade_client.validate_payload.return_value = (False, 'Cidadão inativo')
    educacao_client = AsyncMock()
    service = RequestService(db=AsyncMock(), repository=repo, identidade_client=identidade_client, educacao_client=educacao_client)
    with pytest.raises(ValueError, match='Cidadão inativo'):
        await service.create_request(citizen_id=uuid4(), created_by=uuid4(), service_type=ServiceType.EDUCATION_ENROLLMENT, title='Pedido de matrícula', description='Solicitação de matrícula escolar', channel=RequestChannel.WEB, priority=RequestPriority.MEDIUM, metadata={'turma_id': str(uuid4()), 'ano_letivo_id': str(uuid4())})
    identidade_client.validate_payload.assert_called_once()
    educacao_client.validate_payload.assert_not_called()
    repo.save.assert_not_called()

@pytest.mark.asyncio
async def test_create_request_rejects_invalid_domain_payload() -> None:
    repo = AsyncMock()
    repo.get_next_sequence.return_value = 1
    identidade_client = AsyncMock()
    identidade_client.validate_payload.return_value = (True, None)
    educacao_client = AsyncMock()
    educacao_client.validate_payload.return_value = (False, 'Turma sem vagas disponíveis')
    service = RequestService(db=AsyncMock(), repository=repo, identidade_client=identidade_client, educacao_client=educacao_client)
    with pytest.raises(ValueError, match='Turma sem vagas disponíveis'):
        await service.create_request(citizen_id=uuid4(), created_by=uuid4(), service_type=ServiceType.EDUCATION_ENROLLMENT, title='Pedido de matrícula', description='Solicitação de matrícula escolar', channel=RequestChannel.WEB, priority=RequestPriority.MEDIUM, metadata={'turma_id': str(uuid4()), 'ano_letivo_id': str(uuid4())})
    identidade_client.validate_payload.assert_called_once()
    educacao_client.validate_payload.assert_called_once()
    repo.save.assert_not_called()

@pytest.mark.asyncio
async def test_submit_request_dispatches_to_domain_client() -> None:
    store = {}

    async def save_side_effect(request):
        store[request.id] = request
        return request

    async def get_by_id_side_effect(request_id):
        return store.get(request_id)
    repo = AsyncMock()
    repo.get_next_sequence.return_value = 7
    repo.save.side_effect = save_side_effect
    repo.get_by_id.side_effect = get_by_id_side_effect
    identidade_client = AsyncMock()
    identidade_client.validate_payload.return_value = (True, None)
    educacao_client = AsyncMock()
    educacao_client.validate_payload.return_value = (True, None)
    educacao_client.submit.return_value = {'module': 'educacao', 'accepted': True, 'vaga_disponivel': True}
    service = RequestService(db=AsyncMock(), repository=repo, identidade_client=identidade_client, educacao_client=educacao_client)
    citizen_id = uuid4()
    request = await service.create_request(citizen_id=citizen_id, created_by=citizen_id, service_type=ServiceType.EDUCATION_ENROLLMENT, title='Pedido de matrícula', description='Solicitação de matrícula escolar', channel=RequestChannel.WEB, priority=RequestPriority.MEDIUM, metadata={'turma_id': str(uuid4()), 'ano_letivo_id': str(uuid4())})
    submitted = await service.submit_request(request.id, citizen_id)
    assert submitted.status.value == 'submitted'
    assert submitted.workflow_data['domain_dispatch']['module'] == 'educacao'
    educacao_client.submit.assert_called_once()