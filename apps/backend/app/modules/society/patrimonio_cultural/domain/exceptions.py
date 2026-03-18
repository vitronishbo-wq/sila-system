"""Domain exceptions for PatrimonioCultural module"""
from apps.backend.core.exceptions.factory import ExceptionFactory
exc = ExceptionFactory.create_module_exceptions('PatrimonioCultural')
PatrimonioCulturalException = exc.Base
PatrimonioCulturalNotFound = exc.NotFound
PatrimonioCulturalValidationError = exc.ValidationError
PatrimonioCulturalInvalidStateError = exc.InvalidStateError


class UNESCOPreconditionError(PatrimonioCulturalValidationError):
    """Precondicao UNESCO nao atendida para patrimonio cultural."""


class AssetAlreadyClassifiedError(PatrimonioCulturalValidationError):
    """Ativo patrimonial ja classificado."""


class AssetNotFoundError(PatrimonioCulturalNotFound):
    """Ativo patrimonial nao encontrado."""


class InvalidClassificationAuthorityError(PatrimonioCulturalValidationError):
    """Autoridade de classificacao invalida."""


class PatrimonioDomainError(PatrimonioCulturalException):
    """Erro generico do dominio de patrimonio cultural."""


class ProtectedAssetModificationError(PatrimonioCulturalValidationError):
    """Modificacao de ativo protegido nao permitida."""


__all__ = [
    'PatrimonioCulturalException',
    'PatrimonioCulturalNotFound',
    'PatrimonioCulturalValidationError',
    'PatrimonioCulturalInvalidStateError',
    'UNESCOPreconditionError',
    'AssetAlreadyClassifiedError',
    'AssetNotFoundError',
    'InvalidClassificationAuthorityError',
    'PatrimonioDomainError',
    'ProtectedAssetModificationError',
]
