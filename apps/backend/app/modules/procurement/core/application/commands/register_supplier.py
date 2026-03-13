from dataclasses import dataclass

@dataclass
class RegisterSupplier:
    name: str
    tax_id: str
    address: str