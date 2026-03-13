class SaudeDomainError(Exception):
    """Base exception for saude domain."""


class PatientNotFoundError(SaudeDomainError):
    pass


class MedicalRecordNotFoundError(SaudeDomainError):
    pass


class VaccineDoseNotFoundError(SaudeDomainError):
    pass
