from __future__ import annotations


class AguasSaneamentoError(Exception):
    pass


class AbastecimentoAlreadyExistsError(AguasSaneamentoError):
    pass

class AbastecimentoNotFoundError(AguasSaneamentoError):
    pass

class ConsumoAlreadyExistsError(AguasSaneamentoError):
    pass

class ConsumoNotFoundError(AguasSaneamentoError):
    pass

class FaturaAlreadyExistsError(AguasSaneamentoError):
    pass

class FaturaNotFoundError(AguasSaneamentoError):
    pass

class InfraestruturaAlreadyExistsError(AguasSaneamentoError):
    pass

class InfraestruturaNotFoundError(AguasSaneamentoError):
    pass

class OutorgaAlreadyExistsError(AguasSaneamentoError):
    pass

class OutorgaNotFoundError(AguasSaneamentoError):
    pass
