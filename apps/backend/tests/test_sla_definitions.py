from apps.backend.app.core.audit import SLA_DEFINITIONS, evaluate_sla_status


def test_education_operation_sla_definitions_exist() -> None:
    assert "EDUCATION_ELIGIBILITY_CHECK" in SLA_DEFINITIONS
    assert "EDUCATION_TRANSFER" in SLA_DEFINITIONS
    assert "EDUCATION_ENROLLMENT" in SLA_DEFINITIONS
    assert "EDUCATION_CERTIFICATE" in SLA_DEFINITIONS


def test_education_operation_sla_thresholds() -> None:
    eligibility = SLA_DEFINITIONS["EDUCATION_ELIGIBILITY_CHECK"]
    assert eligibility["target_sla_seconds"] == 0.5
    assert eligibility["warning_threshold_seconds"] == 0.25
    assert eligibility["critical_threshold_seconds"] == 1.0

    transfer = SLA_DEFINITIONS["EDUCATION_TRANSFER"]
    assert transfer["target_sla_seconds"] == 3.0
    assert transfer["warning_threshold_seconds"] == 1.5
    assert transfer["critical_threshold_seconds"] == 5.0

    enrollment = SLA_DEFINITIONS["EDUCATION_ENROLLMENT"]
    assert enrollment["target_sla_seconds"] == 2.0

    certificate = SLA_DEFINITIONS["EDUCATION_CERTIFICATE"]
    assert certificate["target_sla_seconds"] == 2.0


def test_education_operation_sla_evaluation() -> None:
    assert evaluate_sla_status(0.2, "EDUCATION_ELIGIBILITY_CHECK") == "OK"
    assert evaluate_sla_status(0.4, "EDUCATION_ELIGIBILITY_CHECK") == "WARNING"
    assert evaluate_sla_status(0.8, "EDUCATION_ELIGIBILITY_CHECK") == "CRITICAL"
    assert evaluate_sla_status(1.5, "EDUCATION_ELIGIBILITY_CHECK") == "BREACHED"
