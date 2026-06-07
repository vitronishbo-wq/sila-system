"""Domain exceptions for Recommendation subdomain"""


class RecommendationException(Exception):
    """Base exception for Recommendation subdomain"""
    pass


class InsufficientUserData(RecommendationException):
    """Dados do cidadão insuficientes para recomendação"""
    pass


class RecommendationEngineError(RecommendationException):
    """Erro no motor de recomendação"""
    pass


class ModelNotAvailable(RecommendationException):
    """Modelo de ML não disponível"""
    pass
