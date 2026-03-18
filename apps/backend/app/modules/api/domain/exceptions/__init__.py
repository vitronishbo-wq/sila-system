"""Domain exceptions module"""
from apps.backend.core.exceptions.domain_exception import DomainException
from .not_found_exception import EntityNotFoundException, AggregateNotFoundException
from .validation_exception import ValidationException, InvalidEntityException, BusinessRuleException, ValueObjectCreationException
__all__ = ['DomainException', 'EntityNotFoundException', 'AggregateNotFoundException', 'ValidationException', 'InvalidEntityException', 'BusinessRuleException', 'ValueObjectCreationException']