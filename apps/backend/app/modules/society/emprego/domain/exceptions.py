from __future__ import annotations


class EmpregoError(Exception):
    pass


class CandidatoAlreadyExistsError(EmpregoError):
    pass

class CandidatoNotFoundError(EmpregoError):
    pass

class CitizenNotFoundError(EmpregoError):
    pass
