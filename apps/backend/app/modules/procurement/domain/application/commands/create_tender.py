from dataclasses import dataclass
from uuid import UUID
from ...domain.value_objects.procurement_method import ProcurementMethod

@dataclass
class CreateTender:
    title: str
    description: str
    budget_program_id: UUID
    estimated_value: float
    method: ProcurementMethod