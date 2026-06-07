from __future__ import annotations

from fastapi import HTTPException, status

from apps.backend.app.modules.society.familia.domain.exceptions import (
    BiologicalCoherenceError,
    CitizenAlreadyInActiveFamilyError,
    ExclusiveMarriageError,
    FamilyDomainError,
    HeadMustBeAdultError,
    MinorRequiresGuardianError,
    ValidationError,
)


def to_http_error(exc: Exception) -> HTTPException:
    if isinstance(exc, CitizenAlreadyInActiveFamilyError):
        return HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))
    if isinstance(
        exc,
        (
            HeadMustBeAdultError,
            BiologicalCoherenceError,
            ExclusiveMarriageError,
            MinorRequiresGuardianError,
            ValidationError,
            FamilyDomainError,
        ),
    ):
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
    return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))
