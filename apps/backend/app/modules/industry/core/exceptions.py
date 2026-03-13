"""Excecoes do modulo industria."""

class IndustriaError(Exception):
    """Erro base do modulo."""

class EstabelecimentoIndustrialNotFoundError(IndustriaError):
    """Estabelecimento industrial nao encontrado."""

class EstabelecimentoIndustrialAlreadyExistsError(IndustriaError):
    """Estabelecimento industrial ja cadastrado."""

class InvalidEstabelecimentoIndustrialStateError(IndustriaError):
    """Transicao de estado invalida para estabelecimento industrial."""