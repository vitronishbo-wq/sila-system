"""Domain exceptions for CooperacaoInternacional module"""
from apps.backend.core.exceptions.factory import ExceptionFactory
exc = ExceptionFactory.create_module_exceptions('CooperacaoInternacional')
CooperacaoInternacionalException = exc.Base
CooperacaoInternacionalNotFound = exc.NotFound
CooperacaoInternacionalValidationError = exc.ValidationError
CooperacaoInternacionalInvalidStateError = exc.InvalidStateError
__all__ = ['CooperacaoInternacionalException', 'CooperacaoInternacionalNotFound', 'CooperacaoInternacionalValidationError', 'CooperacaoInternacionalInvalidStateError']