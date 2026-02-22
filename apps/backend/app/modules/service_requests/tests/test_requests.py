"""Test requests"""
import pytest
from uuid import uuid4
from datetime import date

from app.modules.service_requests.domain.models.service_request import ServiceRequest
from app.modules.service_requests.domain.enums import RequestStatus, ServiceType, RequestPriority


@pytest.mark.asyncio
async def test_create_request():
    """Test creating a service request"""
    citizen_id = uuid4()
    created_by = uuid4()
    
    request = ServiceRequest(
        citizen_id=citizen_id,
        created_by=created_by,
        service_type="DOCUMENT_REQUEST",
        channel="WEB",
        priority="NORMAL",
        status=RequestStatus.RECEIVED,
        metadata={},
    )
    
    assert request.citizen_id == citizen_id
    assert request.created_by == created_by
    # Legacy "DOCUMENT_REQUEST" maps to ServiceType.IDENTITY_BI
    assert request.service_type == ServiceType.IDENTITY_BI
    assert request.priority == RequestPriority.MEDIUM
    assert request.status == RequestStatus.RECEIVED


@pytest.mark.asyncio
async def test_request_to_dict():
    """Test request serialization"""
    request = ServiceRequest(
        citizen_id=uuid4(),
        created_by=uuid4(),
        service_type="DOCUMENT_REQUEST",
        channel="WEB",
        priority="NORMAL",
        status=RequestStatus.RECEIVED,
        metadata={"notes": "test"},
    )
    
    data = request.to_dict()
    
    # Legacy values are mapped: "DOCUMENT_REQUEST" -> ServiceType.IDENTITY_BI (value: "IDENTIDADE_BI")
    assert data["service_type"] == "IDENTIDADE_BI"
    assert data["channel"] == "WEB"
    # Legacy priority "NORMAL" -> RequestPriority.MEDIUM (value: "MEDIA")
    assert data["priority"] == "MEDIA"
    assert data["metadata"]["notes"] == "test"


@pytest.mark.asyncio
async def test_request_status_transitions():
    """Test request status transitions"""
    request = ServiceRequest(
        citizen_id=uuid4(),
        created_by=uuid4(),
        service_type="DOCUMENT_REQUEST",
        channel="WEB",
        priority="NORMAL",
        status=RequestStatus.RECEIVED,
        metadata={},
    )
    
    assert request.status == RequestStatus.RECEIVED
    
    # Transition to accepted
    request.status = RequestStatus.ACCEPTED
    assert request.status == RequestStatus.ACCEPTED
