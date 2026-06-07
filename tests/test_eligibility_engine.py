import pytest

from foundation.eligibility.evaluator import Evaluator


def make_request(**kwargs):
    req = {
        "student_id": "s1",
        "target_school": "school-1",
        "target_class": "9",
        "academic_year": "2026",
    }
    req.update(kwargs)
    return req


def test_eligible_transfer():
    ev = Evaluator()
    req = make_request(date_of_birth="2012-05-01", debts=[], sanctions=[], institution_capacity={"available": 3})
    out = ev.evaluate(req)
    assert out["eligible"] is True
    assert out["score"] >= 80


def test_blocked_by_debt():
    ev = Evaluator()
    req = make_request(date_of_birth="2012-05-01", debts=[{"amount": 10.0}], sanctions=[], institution_capacity={"available": 2})
    out = ev.evaluate(req)
    assert out["eligible"] is False
    assert "pending_debt" in out["reasons"]


def test_blocked_by_vacancy():
    ev = Evaluator()
    req = make_request(date_of_birth="2012-05-01", debts=[], sanctions=[], institution_capacity={"available": 0})
    out = ev.evaluate(req)
    assert out["eligible"] is False
    assert "no_vacancy" in out["reasons"]


def test_blocked_by_age():
    ev = Evaluator()
    # Too young for class 9
    req = make_request(date_of_birth="2018-01-01", debts=[], sanctions=[], institution_capacity={"available": 2})
    out = ev.evaluate(req)
    assert out["eligible"] is False
    assert "age_incompatible" in out["reasons"]
