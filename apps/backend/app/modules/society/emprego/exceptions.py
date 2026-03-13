"""Domain/application exceptions for emprego module."""

class EmpregoError(Exception):
    pass

class CitizenNotFoundError(EmpregoError):
    pass

class CandidatoAlreadyExistsError(EmpregoError):
    pass

class CandidatoNotFoundError(EmpregoError):
    pass