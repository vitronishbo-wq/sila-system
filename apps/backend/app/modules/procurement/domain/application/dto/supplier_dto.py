from dataclasses import dataclass

@dataclass
class SupplierDTO:
    id: str
    name: str
    tax_id: str