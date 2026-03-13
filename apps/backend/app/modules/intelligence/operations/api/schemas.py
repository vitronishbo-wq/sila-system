from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field

class ServiceCatalogItemResponse(BaseModel):
    id: UUID
    code: str
    name: str
    description: str
    price: float
    estimated_days: int
    workflow_definition_key: str
    required_documents: list[str]
    visibility: str
    version: int
    module_slug: str | None
    module_title: str | None
    is_essential: bool
    icon_slug: str | None
    active: bool

class OrderCreateRequest(BaseModel):
    service_id: UUID

class OrderDocumentInput(BaseModel):
    filename: str = Field(..., min_length=1, max_length=255)
    content_type: str = Field(..., min_length=1, max_length=120)
    size_bytes: int = Field(..., gt=0)
    uri: str | None = Field(default=None, max_length=500)

class OrderAttachDocumentsRequest(BaseModel):
    documents: list[OrderDocumentInput]

class OrderDocumentResponse(BaseModel):
    id: UUID
    filename: str
    content_type: str
    size_bytes: int
    uri: str | None
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class PaymentResponse(BaseModel):
    id: UUID
    order_id: UUID
    reference: str
    amount: float
    status: str
    provider: str
    created_at: datetime
    confirmed_at: datetime | None
    model_config = ConfigDict(from_attributes=True)

class OrderResponse(BaseModel):
    id: UUID
    citizen_id: UUID
    service_id: UUID
    workflow_instance_id: UUID
    total_amount: float
    status: str
    status_history: list[dict]
    created_at: datetime
    updated_at: datetime
    submitted_at: datetime | None
    completed_at: datetime | None
    receipt_number: str | None
    documents: list[OrderDocumentResponse]
    payments: list[PaymentResponse]
    model_config = ConfigDict(from_attributes=True)

class ReceiptResponse(BaseModel):
    receipt_number: str
    order_id: str
    citizen_id: str
    service_id: str
    amount: float
    status: str
    issued_at: str