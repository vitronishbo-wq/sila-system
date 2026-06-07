"""Domain exceptions for Discovery subdomain"""
from typing import Any


class DiscoveryException(Exception):
    """Base exception for Discovery subdomain"""
    pass


class OpportunityNotFound(DiscoveryException):
    """Oportunidade educacional não encontrada"""
    pass


class InstitutionNotFound(DiscoveryException):
    """Instituição não encontrada"""
    pass


class VacancyExhausted(DiscoveryException):
    """Vagas esgotadas para o programa"""
    pass


class InvalidDiscoveryFilter(DiscoveryException):
    """Filtro de busca inválido"""
    pass
