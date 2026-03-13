"""Domain/application exceptions for educacao module."""

class EducacaoError(Exception):
    """Base exception for education workflows."""

class CitizenNotFoundError(EducacaoError):
    pass

class EscolaNotFoundError(EducacaoError):
    pass

class TurmaNotFoundError(EducacaoError):
    pass

class MatriculaAlreadyExistsError(EducacaoError):
    pass

class InvalidMatriculaStateError(EducacaoError):
    pass

class IdadeMinimaNaoAtendidaError(EducacaoError):
    pass

class TurmaSemVagasError(EducacaoError):
    pass

class MatriculaNotFoundError(EducacaoError):
    pass

class TransferenciaNotFoundError(EducacaoError):
    pass

class TransferenciaDuplicadaError(EducacaoError):
    pass

class TransferenciaEstadoInvalidoError(EducacaoError):
    pass