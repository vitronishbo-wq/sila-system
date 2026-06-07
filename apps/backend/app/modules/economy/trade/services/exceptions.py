from __future__ import annotations


class EstabelecimentoComercialError(Exception):
    pass


class EstabelecimentoComercialAlreadyExistsError(EstabelecimentoComercialError):
    pass


class EstabelecimentoComercialNotFoundError(EstabelecimentoComercialError):
    pass


class InvalidEstabelecimentoComercialStateError(EstabelecimentoComercialError):
    pass
