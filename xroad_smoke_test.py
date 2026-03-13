#!/usr/bin/env python3
"""
Smoke test for SILA X-Road protocol validation.

Tests:
1. Envelope creation and serialization
2. Policy validation
3. Replay attack prevention
4. Trust score enforcement
"""

import sys
import os
import asyncio

sys.path.insert(0, os.path.join(os.getcwd(), 'apps/backend'))

from app.modules.xroad.domain.envelope import (
    SILAEnvelope,
    OriginMinistry,
    ServiceType,
    MessageStatus,
)
from app.modules.xroad.application.xroad_service import XRoadInterconnect


async def test_envelope_creation():
    """Test 1: Create and validate SILA envelope."""
    print("🧪 Test 1: Envelope Creation")

    envelope = SILAEnvelope(
        sender_service=OriginMinistry.MINJUS,
        receiver_service=OriginMinistry.MINSA,
        service_type=ServiceType.VERIFY_BIRTH_NOTICE,
        payload={
            'citizen_nif': '123456789',
            'birth_certificate_id': 'BI_12345',
            'query_reason': 'IDENTITY_DOCUMENT_ISSUANCE',
        },
    )

    assert envelope.message_id is not None, "❌ message_id not generated"
    assert len(envelope.message_id) == 36, "❌ message_id invalid UUID format"
    assert envelope.sender_service == OriginMinistry.MINJUS, "❌ sender_service mismatch"
    assert envelope.receiver_service == OriginMinistry.MINSA, "❌ receiver_service mismatch"

    print(f"  ✓ Envelope created: {envelope.message_id}")
    print(f"  ✓ Service type: {envelope.service_type.value}")
    return True


async def test_xroad_initialization():
    """Test 2: X-Road service initialization and policy loading."""
    print("\n🧪 Test 2: X-Road Initialization")

    xroad = XRoadInterconnect()

    assert xroad.policies is not None, "❌ Policies not loaded"
    assert len(xroad.policies) > 0, "❌ No policies defined"

    print(f"  ✓ X-Road service initialized")
    print(f"  ✓ Policies loaded: {len(xroad.policies)}")

    for (sender, receiver), policy in list(xroad.policies.items())[:2]:
        print(f"    - {sender.value} → {receiver.value}: {len(policy.allowed_service_types)} services")

    return True


async def test_envelope_validation():
    """Test 3: Envelope validation workflow."""
    print("\n🧪 Test 3: Envelope Validation")

    xroad = XRoadInterconnect()

    # Valid envelope with high trust score
    envelope = SILAEnvelope(
        sender_service=OriginMinistry.MINJUS,
        receiver_service=OriginMinistry.MINSA,
        service_type=ServiceType.VERIFY_BIRTH_NOTICE,
        trust_score=0.90,
        signature='<mock-signature>',
        payload={'citizen_nif': '123456789'},
    )

    is_valid, reason = await xroad.validate_envelope(envelope)
    assert is_valid, f"❌ Valid envelope rejected: {reason}"
    print(f"  ✓ Valid envelope accepted")

    # Invalid: Low trust score
    envelope_low_trust = SILAEnvelope(
        sender_service=OriginMinistry.MINJUS,
        receiver_service=OriginMinistry.MINSA,
        service_type=ServiceType.VERIFY_BIRTH_NOTICE,
        trust_score=0.50,  # Below 0.80 threshold
        signature='<mock-signature>',
        payload={},
    )

    is_valid, reason = await xroad.validate_envelope(envelope_low_trust)
    assert not is_valid, "❌ Low trust envelope should be rejected"
    assert 'trust' in reason.lower(), "❌ Reason should mention trust score"
    print(f"  ✓ Low trust envelope rejected: {reason}")

    # Invalid: Policy violation
    envelope_forbidden = SILAEnvelope(
        sender_service=OriginMinistry.MINJUS,
        receiver_service=OriginMinistry.MINFIN,  # No policy between MINJUS and MINFIN
        service_type=ServiceType.VERIFY_BIRTH_NOTICE,
        trust_score=0.90,
        signature='<mock-signature>',
        payload={},
    )

    is_valid, reason = await xroad.validate_envelope(envelope_forbidden)
    assert not is_valid, "❌ Policy violation should be rejected"
    assert 'policy' in reason.lower(), "❌ Reason should mention policy"
    print(f"  ✓ Policy violation rejected: {reason}")

    return True


async def test_replay_attack_prevention():
    """Test 4: Replay attack detection."""
    print("\n🧪 Test 4: Replay Attack Prevention")

    xroad = XRoadInterconnect()

    envelope = SILAEnvelope(
        message_id='test-replay-123',
        sender_service=OriginMinistry.MINJUS,
        receiver_service=OriginMinistry.MINSA,
        service_type=ServiceType.VERIFY_BIRTH_NOTICE,
        trust_score=0.90,
        signature='<mock-signature>',
        payload={},
    )

    # First exchange
    response1 = await xroad.exchange(envelope)
    assert response1.status == MessageStatus.PROCESSED, "❌ First exchange should succeed"
    print(f"  ✓ First exchange processed: {response1.audit_record_id}")

    # Replay attempt with same message_id
    response2 = await xroad.exchange(envelope)
    assert response2.status == MessageStatus.REPLAY_BLOCKED, "❌ Replay should be blocked"
    assert 'replay' in response2.error.lower(), "❌ Error should mention replay"
    print(f"  ✓ Replay attack blocked: {response2.error}")

    return True


async def test_service_discovery():
    """Test 5: Service discovery endpoint."""
    print("\n🧪 Test 5: Service Discovery")

    xroad = XRoadInterconnect()
    services = await xroad.list_services()

    assert services['available_services'], "❌ No services available"
    assert len(services['available_services']) >= 8, "❌ Not enough services"
    assert services['interop_policy_count'] > 0, "❌ No policies"

    print(f"  ✓ Available services: {len(services['available_services'])}")
    print(f"  ✓ Interop policies: {services['interop_policy_count']}")

    for service in services['available_services'][:5]:
        print(f"    - {service}")

    return True


async def main():
    """Run all smoke tests."""
    print("=" * 70)
    print("🚀 SILA X-Road Protocol Validation")
    print("=" * 70)

    tests = [
        test_envelope_creation,
        test_xroad_initialization,
        test_envelope_validation,
        test_replay_attack_prevention,
        test_service_discovery,
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            result = await test()
            if result:
                passed += 1
        except Exception as e:
            print(f"  ❌ Test failed: {str(e)}")
            import traceback
            traceback.print_exc()
            failed += 1

    print("\n" + "=" * 70)
    print(f"📊 Results: {passed} passed, {failed} failed")

    if failed == 0:
        print("✅ SILA X-Road: Protocolo de Envelope Validado")
        print("=" * 70)
        return 0
    else:
        print("❌ Some tests failed")
        print("=" * 70)
        return 1


if __name__ == '__main__':
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
