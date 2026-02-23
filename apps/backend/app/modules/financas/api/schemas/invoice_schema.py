from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional
from app.modules.financas.domain.models.enums import InvoiceStatus

class InvoiceBase(BaseModel):
    """
    Atributos base para faturas, alinhados com as normas de governação pública.
    """
    citizen_id: str = Field(..., min_length=5, description="Identificador único do cidadão (FUC)")
    service_code: str = Field(..., min_length=2, description="Código interno do serviço público")
    service_name: str = Field(..., description="Nome descritivo do serviço prestado")
    request_id: Optional[str] = Field(None, description="UUID do pedido administrativo no Motor SILA")
    
    # Campos de Classificação Orçamental (Tesouro Nacional)
    revenue_code: str = Field(..., description="Código da Rubrica de Receita para classificação orçamental")
    cost_center: str = Field(..., description="Unidade Orçamental ou Centro de Custo emissor")
    
    amount: float = Field(..., gt=0, description="Valor total da fatura")
    currency: str = Field(default="AOA", pattern=r"^[A-Z]{3}$", description="Moeda em formato ISO 4217")
    due_date: datetime = Field(..., description="Data limite para pagamento sem penalizações")

class CreateInvoiceSchema(InvoiceBase):
    """Schema para a criação de novas faturas."""
    pass

class UpdateInvoiceSchema(BaseModel):
    """Schema para atualização parcial de dados da fatura."""
    status: Optional[InvoiceStatus] = None
    due_date: Optional[datetime] = None
    amount: Optional[float] = Field(None, gt=0)

class InvoiceResponse(InvoiceBase):
    """
    Schema de resposta completo para a API, mapeando todos os campos do modelo Invoice.
    Utilizado para visualização no dashboard e histórico do cidadão.
    """
    model_config = ConfigDict(from_attributes=True)

    id: str = Field(..., description="Identificador UUID interno da fatura")
    reference: str = Field(..., description="Referência única de pagamento (ex: SILA-2024-XXXX)")
    status: InvoiceStatus = Field(..., description="Estado atual do ciclo de vida da fatura")
    created_at: datetime = Field(..., description="Data de emissão da fatura")
    updated_at: datetime = Field(..., description="Data da última alteração de estado")
