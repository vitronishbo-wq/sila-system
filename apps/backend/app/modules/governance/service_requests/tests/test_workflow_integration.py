"""Test workflow integration"""
import pytest
from uuid import uuid4
from app.modules.governance.service_requests.integrations.workflow_client import WorkflowClient

@pytest.mark.asyncio
async def test_start_workflow():
    """Test starting workflow"""
    client = WorkflowClient()
    response = await client.start_workflow(definition_key='SERVICE_REQUEST_WORKFLOW', business_key=str(uuid4()), variables={'service_type': 'DOCUMENT_REQUEST'}, actor_id=uuid4())
    assert response is not None
    assert response['definition_key'] == 'SERVICE_REQUEST_WORKFLOW'
    assert response['status'] == 'ACTIVE'

@pytest.mark.asyncio
async def test_workflow_transition():
    """Test workflow transition"""
    client = WorkflowClient()
    success = await client.send_transition(instance_id=uuid4(), transition='APPROVE', actor_id=uuid4())
    assert success is True

@pytest.mark.asyncio
async def test_get_workflow_instance():
    """Test getting workflow instance"""
    client = WorkflowClient()
    instance = await client.get_instance(uuid4())
    assert instance is not None
    assert instance['status'] == 'ACTIVE'