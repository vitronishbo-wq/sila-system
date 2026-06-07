from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Optional
from uuid import UUID, uuid4

from apps.backend.app.core.events.domain_event import AuditableEvent


@dataclass
class PagamentoReferencia:
    reference: str
    entity: str = "12345"
    amount: float = 2500.0
    currency: str = "AOA"
    status: str = "PENDENTE"
    payment_id: Optional[str] = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))


class PagamentoMatriculaService:
    """Bridge between Educação wizard and the Payment module.

    Replaces inline dict payment with proper integration:
      1. gerar_referencia → creates a payment intent via Payment module
      2. confirmar_pagamento → confirms payment and publishes PaymentConfirmed
      3. After enrollment, publishes StudentEnrolled event
    """

    def __init__(self, educacao_service_port=None, event_bus=None):
        self._port = educacao_service_port
        self._event_bus = event_bus

    async def gerar_referencia(
        self,
        wizard_id: UUID,
        citizen_id: UUID,
        amount: float = 2500.0,
    ) -> PagamentoReferencia:
        payment_id = str(uuid4())
        ref = f"EDU-PAG-{wizard_id.hex[:8].upper()}-{datetime.now(UTC).strftime('%Y%m%d%H%M%S')}"
        referencia = PagamentoReferencia(
            reference=ref,
            amount=amount,
            payment_id=payment_id,
        )
        if self._port:
            await self._port.registrar_pagamento_propina(
                reference_id=str(wizard_id),
                payment_id=payment_id,
                amount=amount,
            )
        return referencia

    async def confirmar_pagamento(
        self,
        wizard_id: UUID,
        citizen_id: UUID,
        payment_ref: str,
        amount: float = 2500.0,
    ) -> PagamentoReferencia:
        referencia = PagamentoReferencia(
            reference=payment_ref,
            amount=amount,
            status="CONFIRMADO",
            payment_id=str(uuid4()),
        )
        if self._port:
            await self._port.registrar_pagamento_propina(
                reference_id=str(wizard_id),
                payment_id=referencia.payment_id,
                amount=amount,
            )
        if self._event_bus:
            event = AuditableEvent(
                aggregate_id=wizard_id,
                aggregate_type="WizardMatricula",
                event_type="PaymentConfirmed",
                metadata={
                    "payment_ref": payment_ref,
                    "citizen_id": str(citizen_id),
                    "amount": amount,
                    "currency": "AOA",
                    "timestamp": datetime.now(UTC).isoformat(),
                },
            )
            await self._event_bus.publish(event)
        return referencia

    async def publish_student_enrolled(
        self,
        wizard_id: UUID,
        student_id: UUID,
        institution_id: UUID,
        enrollment_id: UUID,
    ) -> None:
        if not self._event_bus:
            return
        event = AuditableEvent(
            aggregate_id=wizard_id,
            aggregate_type="WizardMatricula",
            event_type="StudentEnrolled",
            metadata={
                "student_id": str(student_id),
                "institution_id": str(institution_id),
                "enrollment_id": str(enrollment_id),
                "timestamp": datetime.now(UTC).isoformat(),
            },
        )
        await self._event_bus.publish(event)
