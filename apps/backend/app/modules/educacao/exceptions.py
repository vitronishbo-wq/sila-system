"""Domain/application exceptions for educacao module."""


class EducacaoError(Exception):
    """Base exception for education workflows."""


class CitizenNotFoundError(EducacaoError):
    pass


class EscolaNotFoundError(EducacaoError):
    pass


class MatriculaAlreadyExistsError(EducacaoError):
    pass


class InvalidMatriculaStateError(EducacaoError):
    pass

