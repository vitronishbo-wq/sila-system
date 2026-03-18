"""Domain exceptions for DefesaConsumidor module"""
from apps.backend.core.exceptions.factory import ExceptionFactory
exc = ExceptionFactory.create_module_exceptions('DefesaConsumidor')
DefesaConsumidorException = exc.Base
DefesaConsumidorNotFound = exc.NotFound
DefesaConsumidorValidationError = exc.ValidationError
DefesaConsumidorInvalidStateError = exc.InvalidStateError


class ReclamacaoJaEncerradaException(DefesaConsumidorException):
    """Reclamacao ja encerrada no modulo DefesaConsumidor."""


class ReclamacaoNaoEncontradaException(DefesaConsumidorNotFound):
    """Reclamacao nao encontrada no modulo DefesaConsumidor."""


__all__ = [
    'DefesaConsumidorException',
    'DefesaConsumidorNotFound',
    'DefesaConsumidorValidationError',
    'DefesaConsumidorInvalidStateError',
    'ReclamacaoJaEncerradaException',
    'ReclamacaoNaoEncontradaException',
]
