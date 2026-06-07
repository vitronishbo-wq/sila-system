"""Domain exceptions for Search subdomain"""


class SearchException(Exception):
    """Base exception for Search subdomain"""
    pass


class InvalidSearchQuery(SearchException):
    """Query de busca inválida"""
    pass


class SearchIndexNotAvailable(SearchException):
    """Índice de busca não disponível"""
    pass


class GeolocationError(SearchException):
    """Erro na busca geoespacial"""
    pass


class FilterParsingError(SearchException):
    """Erro ao processar filtros de busca"""
    pass
