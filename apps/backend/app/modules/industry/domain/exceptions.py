from __future__ import annotations


class IndustryError(Exception):
    pass


class EstabelecimentoIndustrialAlreadyExistsError(IndustryError):
    pass

class EstabelecimentoIndustrialNotFoundError(IndustryError):
    pass

class InvalidEstabelecimentoIndustrialStateError(IndustryError):
    pass
