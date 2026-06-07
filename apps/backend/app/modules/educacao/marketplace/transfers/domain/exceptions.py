"""Domain exceptions for Transfers subdomain"""


class TransferException(Exception):
    """Base exception for Transfers subdomain"""
    pass


class TransferNotEligible(TransferException):
    """Cidadão não elegível para transferência"""
    pass


class SourceInstitutionInvalid(TransferException):
    """Instituição de origem inválida"""
    pass


class DestinationInstitutionInvalid(TransferException):
    """Instituição de destino inválida"""
    pass


class CurriculumIncompatible(TransferException):
    """Currículo incompatível para transferência"""
    pass


class TransferRequestDuplicate(TransferException):
    """Solicitação de transferência duplicada"""
    pass
