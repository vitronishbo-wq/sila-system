from __future__ import annotations


class EnergyBillingService:
    def __init__(self, payment_port: PaymentPort):
        self.payment_port = payment_port

    async def generate_invoice(self, customer_id: str, kwh_consumed: float):
        amount = self._calculate_tariff(kwh_consumed)
        payment_request = {
            "vendor_did": f"did:sila:energy:{customer_id}",
            "amount": amount,
            "currency": "Kz",
            "category": "UTILITY_REVENUE",
        }
        return await self.payment_port.request_funds(payment_request)

    def _calculate_tariff(self, kwh: float) -> float:
        return kwh * 0.45
