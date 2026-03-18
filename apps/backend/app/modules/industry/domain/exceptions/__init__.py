class IndustriaError(Exception):
    pass

class EstabelecimentoIndustrialAlreadyExistsError(IndustriaError):
    pass

class EstabelecimentoIndustrialNotFoundError(IndustriaError):
    pass

class InvalidEstabelecimentoIndustrialStateError(IndustriaError):
    pass
__all__ = ['IndustriaError', 'EstabelecimentoIndustrialAlreadyExistsError', 'EstabelecimentoIndustrialNotFoundError', 'InvalidEstabelecimentoIndustrialStateError']