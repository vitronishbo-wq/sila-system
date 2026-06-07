from ...domain.ports.payment_provider_port import PaymentProviderPort
from ...domain.models.payment import Payment


class MulticaixaMockProvider(PaymentProviderPort):
    BASE_URL = "https://api.multicaixa.co.ao/v1"

    def __init__(self, api_key: str | None = None, merchant_id: str | None = None):
        self._api_key = api_key or "mock-key"
        self._merchant_id = merchant_id or "mock-merchant"

    async def authorize(self, payment: Payment) -> dict:
        return {
            "provider": "multicaixa",
            "authorized": True,
            "provider_reference": f"MCX-{payment.id}",
            "merchant_id": self._merchant_id,
        }

    async def capture(self, provider_reference: str) -> dict:
        return {
            "provider": "multicaixa",
            "captured": True,
            "provider_reference": provider_reference,
        }

    async def refund(self, provider_reference: str, amount: float | None = None) -> dict:
        return {
            "provider": "multicaixa",
            "refunded": True,
            "provider_reference": provider_reference,
            "amount": amount,
        }

    async def verify_webhook(self, signature: str, payload: str) -> bool:
        return signature == "mock-signature"

    async def parse_webhook(self, payload: dict) -> dict:
        return {
            "provider": "multicaixa",
            "event": payload.get("event", "unknown"),
            "reference": payload.get("reference", ""),
            "status": payload.get("status", "pending"),
        }

    async def get_transaction_status(self, provider_reference: str) -> str:
        return "completed"


class EmisPaymentSyncAdapter:
    def __init__(self, emis_client=None):
        self._emis_client = emis_client

    async def sync_payment_to_emis(self, payment_ref: str, amount: float, student_id: str) -> dict:
        return {
            "synced": True,
            "emis_reference": f"EMIS-{payment_ref}",
            "student_id": student_id,
            "amount": amount,
        }

    async def consultar_propina_emis(self, student_id: str) -> float:
        return 0.0

    async def verificar_pagamento_emis(self, reference: str) -> bool:
        return True
