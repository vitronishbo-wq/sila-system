from dataclasses import dataclass


@dataclass
class StudentIdentity:
    student_id: str
    national_id: str | None
    full_name: str
    date_of_birth: str | None
    academic_registry_id: str | None


def validate_identity(identity: StudentIdentity) -> bool:
    """Placeholder validation for academic identity.

    In later iterations this will call authoritative identity services
    and run KYC / document checks.
    """
    return bool(identity.student_id and identity.full_name)
