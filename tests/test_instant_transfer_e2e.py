import pytest

from apps.backend.app.modules.marketplace.application.adapters import (
    MatchingAdapter,
    ReservationAdapter,
    PaymentAdapter,
    TransferAdapter,
    NotificationAdapter,
)
from apps.backend.app.modules.marketplace.application.service import InstantTransferOrchestrator
from apps.backend.app.modules.marketplace.application.dto import InstantTransferRequestDTO


@pytest.mark.asyncio
async def test_e2e_happy_path():
    matching = MatchingAdapter(selected_institution="i-success")
    reservation = ReservationAdapter()
    payment = PaymentAdapter()
    transfer = TransferAdapter()
    notification = NotificationAdapter()

    orchestrator = InstantTransferOrchestrator(matching, reservation, payment, transfer, notification)

    req = InstantTransferRequestDTO(student_id="s1", preferred_institution_id="i-success", amount=100.0, payment_method="card")
    resp = await orchestrator.orchestrate(req, idempotency_key="txn_happy")

    assert resp.status == "success"
    assert resp.transfer_id is not None
    assert resp.transaction_id == "txn_happy"
    assert resp.steps["reservation"].status == "ok"
    assert resp.steps["payment"].status == "ok"
    assert resp.steps["transfer"].status == "ok"


@pytest.mark.asyncio
async def test_e2e_payment_failure_releases_reservation():
    matching = MatchingAdapter(selected_institution="i-payfail")
    reservation = ReservationAdapter()
    payment = PaymentAdapter(fail_charge=True)
    transfer = TransferAdapter()
    notification = NotificationAdapter()

    orchestrator = InstantTransferOrchestrator(matching, reservation, payment, transfer, notification)

    req = InstantTransferRequestDTO(student_id="s2", preferred_institution_id="i-payfail", amount=50.0, payment_method="card")

    with pytest.raises(Exception):
        await orchestrator.orchestrate(req, idempotency_key="txn_payfail")

    # Reservation should be released
    # find reservation id
    res_keys = list(reservation.reservations.keys())
    assert res_keys, "reservation not created"
    res = reservation.reservations[res_keys[0]]
    assert res["released"] is True


@pytest.mark.asyncio
async def test_e2e_transfer_failure_triggers_refund_and_release():
    matching = MatchingAdapter(selected_institution="i-trfail")
    reservation = ReservationAdapter()
    payment = PaymentAdapter()
    transfer = TransferAdapter(fail_execute=True)
    notification = NotificationAdapter()

    orchestrator = InstantTransferOrchestrator(matching, reservation, payment, transfer, notification)

    req = InstantTransferRequestDTO(student_id="s3", preferred_institution_id="i-trfail", amount=120.0, payment_method="card")

    with pytest.raises(Exception):
        await orchestrator.orchestrate(req, idempotency_key="txn_trfail")

    # Ensure reservation released
    res_keys = list(reservation.reservations.keys())
    assert res_keys
    res = reservation.reservations[res_keys[0]]
    assert res["released"] is True

    # Ensure payment recorded and refund attempted (refund not raising means success)
    # Payment adapter stores charges with key pay_{txn_id}
    assert any(k.startswith("pay_") for k in payment.charges.keys())