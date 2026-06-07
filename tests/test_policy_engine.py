import pytest

from foundation.eligibility.rules import TransferWindowRule
from foundation.policies import policy_engine


def test_default_policies_are_registered():
    assert policy_engine.get_policy("MAX_TRANSFER_DISTANCE") == 50
    assert policy_engine.get_policy("MAX_PENDING_DEBT") == 0
    assert isinstance(policy_engine.get_policy("TRANSFER_WINDOWS"), dict)
    assert policy_engine.get_policy("TRANSFER_WINDOWS")["2026"]["enabled"] is True
    assert policy_engine.get_policy("TRANSFER_WINDOWS")["2027"]["start_date"] == "2027-03-01"
    assert policy_engine.get_policy("TRANSFER_WINDOWS")["2028"]["end_date"] == "2028-05-31"
    assert policy_engine.get_policy("TRANSFER_WINDOWS")["2026"]["regions"]["south"]["enabled"] is False
    assert policy_engine.get_policy("TRANSFER_WINDOWS")["2026"]["regions"]["north"]["semesters"]["1"]["enabled"] is True
    assert policy_engine.get_policy("TRANSFER_WINDOWS")["2029"]["enabled"] is True
    assert policy_engine.get_policy("TRANSFER_WINDOWS")["2030"]["end_date"] == "2030-05-31"
    assert tuple(policy_engine.get_policy("GRADE_COMPATIBILITY")["1"]) == (6, 7)
    assert tuple(policy_engine.get_policy("GRADE_COMPATIBILITY")["10"]) == (15, 15)


def test_transfer_window_period_support():
    rule = TransferWindowRule()
    original_window = policy_engine.get_policy("TRANSFER_WINDOWS")
    try:
        policy_engine.register_policy(
            "TRANSFER_WINDOWS",
            {
                "default": False,
                "2026": {
                    "enabled": True,
                    "start_date": "2000-01-01",
                    "end_date": "2099-12-31",
                    "semesters": {
                        "1": {
                            "enabled": True,
                            "start_date": "2000-01-01",
                            "end_date": "2099-12-31",
                        }
                    },
                    "regions": {
                        "north": {
                            "enabled": True,
                            "start_date": "2000-01-01",
                            "end_date": "2099-12-31",
                        },
                        "south": {
                            "enabled": False,
                            "start_date": "2000-01-01",
                            "end_date": "2099-12-31",
                        },
                    },
                },
            },
            overwrite=True,
        )

        assert rule.evaluate({"academic_year": 2026}) == (True, "within_window")
        assert rule.evaluate({"academic_year": 2026, "semester": 1}) == (True, "within_window")
        assert rule.evaluate({"academic_year": 2026, "region": "north"}) == (True, "within_window")
        assert rule.evaluate({"academic_year": 2026, "region": "south"}) == (False, "transfer_window_closed")
        assert rule.evaluate({"academic_year": 2026, "region": "north", "semester": 1}) == (True, "within_window")
        assert rule.evaluate({"academic_year": 2025}) == (False, "transfer_window_closed")
    finally:
        policy_engine.register_policy("TRANSFER_WINDOWS", original_window, overwrite=True)


def test_policy_update_changes_value():
    policy_engine.update_policy("MAX_PENDING_DEBT", 100)
    assert policy_engine.get_policy("MAX_PENDING_DEBT") == 100


def test_unknown_policy_returns_default():
    assert policy_engine.get_policy("NON_EXISTENT_POLICY", "fallback") == "fallback"
