import os

from foundation.orchestration.dlq import RabbitMQDeadLetterQueue, build_dead_letter_queue
from foundation.policies import policy_engine


def test_policy_defaults_are_registered():
    assert policy_engine.get_policy("MAX_TRANSFER_DISTANCE") == 50
    assert policy_engine.get_policy("MAX_PENDING_DEBT") == 0
    assert policy_engine.get_policy("TRANSFER_WINDOWS") == {"default": True, "2026": True}
    assert policy_engine.get_policy("GRADE_COMPATIBILITY") == {
        "9": (14, 14),
        "10": (15, 15),
        "11": (16, 16),
        "12": (17, 18),
    }


def test_build_dead_letter_queue_uses_rabbitmq_when_configured(monkeypatch):
    monkeypatch.setenv("DLQ_BUS", "rabbitmq")
    dlq = build_dead_letter_queue()
    assert isinstance(dlq, RabbitMQDeadLetterQueue)


def test_build_dead_letter_queue_defaults_to_file():
    os.environ.pop("DLQ_BUS", None)
    dlq = build_dead_letter_queue()
    assert dlq.__class__.__name__ == "FileDeadLetterQueue"
