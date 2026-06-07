from __future__ import annotations

from apps.backend.app.core.exceptions import BaseRequestException
from fastapi import status


class EscolaNotFoundError(BaseRequestException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Escola não encontrada"

    def __init__(self, escola_id: str | None = None, **kwargs):
        msg = f"Escola {escola_id} nao encontrada" if escola_id else self.detail
        super().__init__(msg, **kwargs)


class MatriculaNotFoundError(BaseRequestException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Matricula não encontrada"

    def __init__(self, matricula_id: str | None = None, **kwargs):
        msg = f"Matricula {matricula_id} nao encontrada" if matricula_id else self.detail
        super().__init__(msg, **kwargs)


class CitizenNotFoundError(BaseRequestException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Cidadão não encontrado"

    def __init__(self, citizen_id: str | None = None, **kwargs):
        msg = f"Cidadao {citizen_id} nao encontrado" if citizen_id else self.detail
        super().__init__(msg, **kwargs)


class InvalidMatriculaStateError(BaseRequestException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Estado de matricula inválido"


class IdadeMinimaNaoAtendidaError(BaseRequestException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Idade minima nao atendida"


class MatriculaAlreadyExistsError(BaseRequestException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Matricula ja existe"


class TransferenciaDuplicadaError(BaseRequestException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Transferencia duplicada"


class TransferenciaEstadoInvalidoError(BaseRequestException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Estado de transferencia invalido"


class TransferenciaNotFoundError(BaseRequestException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Transferencia não encontrada"


class TurmaNotFoundError(BaseRequestException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Turma não encontrada"


class TurmaSemVagasError(BaseRequestException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Turma sem vagas"


__all__ = [
    "EscolaNotFoundError",
    "MatriculaNotFoundError",
    "CitizenNotFoundError",
    "IdadeMinimaNaoAtendidaError",
    "MatriculaAlreadyExistsError",
    "InvalidMatriculaStateError",
    "TransferenciaDuplicadaError",
    "TransferenciaEstadoInvalidoError",
    "TransferenciaNotFoundError",
    "TurmaNotFoundError",
    "TurmaSemVagasError",
]
