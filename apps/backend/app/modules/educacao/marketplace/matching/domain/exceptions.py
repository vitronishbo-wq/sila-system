"""Domain exceptions for Matching subdomain"""


class MatchingException(Exception):
    """Base exception for Matching subdomain"""
    pass


class CitizenProfileIncomplete(MatchingException):
    """Perfil do cidadão incompleto para matching"""
    pass


class NoMatchesFound(MatchingException):
    """Nenhuma oportunidade compatível encontrada"""
    pass


class MatchingEngineError(MatchingException):
    """Erro no motor de matching automático"""
    pass


class EligibilityValidationFailed(MatchingException):
    """Validação de elegibilidade falhou"""
    pass
