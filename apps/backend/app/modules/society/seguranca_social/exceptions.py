"""Domain/application exceptions for seguranca_social module."""

class SegurancaSocialError(Exception):
    pass

class CitizenNotFoundError(SegurancaSocialError):
    pass

class BeneficiarioAlreadyExistsError(SegurancaSocialError):
    pass

class BeneficiarioNotFoundError(SegurancaSocialError):
    pass

class CandidatoEmpregoRequiredError(SegurancaSocialError):
    pass

class PensaoNotFoundError(SegurancaSocialError):
    pass

class BeneficiarioNotEligibleError(SegurancaSocialError):
    pass

class PensaoAlreadyExistsError(SegurancaSocialError):
    pass