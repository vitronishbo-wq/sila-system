from __future__ import annotations


class ElectronicTollService:
    def __init__(self, payment_port: "PaymentPort"):
        self.payment_port = payment_port

    async def process_toll_passage(self, vehicle_did: str, gantry_id: str):
        toll_amount = self._get_toll_rate(gantry_id)

        return await self.payment_port.request_funds(
            {
                "vendor_did": vehicle_did,
                "amount": toll_amount,
                "currency": "Kz",
                "category": "TRANSPORT_TOLL",
            }
        )

    def _get_toll_rate(self, gantry_id: str) -> float:
        return 1500.00
