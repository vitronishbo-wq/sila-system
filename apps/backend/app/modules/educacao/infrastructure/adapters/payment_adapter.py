from __future__ import annotations

from apps.backend.app.modules.payment.application.ports import EducacaoServicePort


class EducacaoPaymentAdapter(EducacaoServicePort):
    """Concrete adapter that the Payment module calls back into Educação.

    Implements EducacaoServicePort so PaymentService can notify Educação
    when a propina (tuition) payment is completed.
    """

    def __init__(self, wizard_repo=None, event_bus=None):
        self._wizard_repo = wizard_repo
        self._event_bus = event_bus

    async def registrar_pagamento_propina(
        self, reference_id: str, payment_id: str, amount: float
    ) -> None:
        """Called by PaymentService when a propina payment is registered."""
        if self._event_bus:
            from apps.backend.app.core.events.domain_event import AuditableEvent
            from uuid import UUID

            event = AuditableEvent(
                aggregate_id=UUID(reference_id) if reference_id else UUID(int=0),
                aggregate_type="WizardMatricula",
                event_type="PaymentConfirmed",
                metadata={
                    "reference_id": reference_id,
                    "payment_id": payment_id,
                    "amount": amount,
                    "currency": "AOA",
                    "origin": "payment_module",
                },
            )
            await self._event_bus.publish(event)
