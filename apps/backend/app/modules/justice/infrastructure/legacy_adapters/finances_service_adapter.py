import asyncio
from typing import Any


class FinancesServiceAdapter:
    """Compatibility adapter for finance service calls."""

    def __init__(self, finances_service: Any = None):
        self.finances_service = finances_service

    def register_fee(self, payload: dict) -> dict:
        if self.finances_service and hasattr(self.finances_service, "register_fee"):
            result = self.finances_service.register_fee(payload)
            return result or {}
        return {}

    def get_balance(self, citizen_id: str) -> dict:
        if self.finances_service and hasattr(self.finances_service, "get_balance"):
            result = self.finances_service.get_balance(citizen_id)
            return result or {}
        return {}

    def create_invoice(self, payload: dict) -> dict:
        if self.finances_service and hasattr(self.finances_service, "create_invoice"):
            result = self.finances_service.create_invoice(payload)
            return result or {}
        return {}

    async def get_invoices_by_citizen(self, citizen_id) -> dict:
        if self.finances_service and hasattr(self.finances_service, "get_invoices_by_citizen"):
            result = self.finances_service.get_invoices_by_citizen(citizen_id)
            if asyncio.iscoroutine(result):
                result = await result
            if isinstance(result, dict):
                result.setdefault("citizen_id", str(citizen_id))
                result.setdefault("invoices", [])
                return result
            return {"citizen_id": str(citizen_id), "invoices": []}
        return {"citizen_id": str(citizen_id), "invoices": []}

    async def get_payments_by_citizen(self, citizen_id) -> dict:
        if self.finances_service and hasattr(self.finances_service, "get_payments_by_citizen"):
            result = self.finances_service.get_payments_by_citizen(citizen_id)
            if asyncio.iscoroutine(result):
                result = await result
            return result if isinstance(result, dict) else {}
        return {"citizen_id": str(citizen_id), "payments": []}
