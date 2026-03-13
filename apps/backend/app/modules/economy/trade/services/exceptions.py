"""Excecoes do modulo comercio_servicos."""

class ComercioServicosError(Exception):
    """Erro base do modulo."""

class EstabelecimentoComercialNotFoundError(ComercioServicosError):
    """Estabelecimento comercial nao encontrado."""

class EstabelecimentoComercialAlreadyExistsError(ComercioServicosError):
    """Estabelecimento comercial ja cadastrado."""

class InvalidEstabelecimentoComercialStateError(ComercioServicosError):
    """Transicao de estado invalida para estabelecimento comercial."""