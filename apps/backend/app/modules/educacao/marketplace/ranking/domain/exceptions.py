"""Domain exceptions for Ranking subdomain"""


class RankingException(Exception):
    """Base exception for Ranking subdomain"""
    pass


class InstitutionNotFound(RankingException):
    """Instituição não encontrada para ranking"""
    pass


class InvalidRankingMetrics(RankingException):
    """Métricas de ranking inválidas"""
    pass


class RankingCalculationFailed(RankingException):
    """Cálculo de ranking falhou"""
    pass
