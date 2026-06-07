from __future__ import annotations


class SegurancaSocialError(Exception):
    pass


class BeneficiarioAlreadyExistsError(SegurancaSocialError):
    pass


class BeneficiarioNotFoundError(SegurancaSocialError):
    pass


class BeneficiarioNotEligibleError(SegurancaSocialError):
    pass


class CandidatoEmpregoRequiredError(SegurancaSocialError):
    pass


class CitizenNotFoundError(SegurancaSocialError):
    pass


class PensaoAlreadyExistsError(SegurancaSocialError):
    pass


class PensaoNotFoundError(SegurancaSocialError):
    pass
