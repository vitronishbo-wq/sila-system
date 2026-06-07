from __future__ import annotations


class DefesaConsumidorError(Exception):
    pass


class ReclamacaoJaEncerradaException(DefesaConsumidorError):
    pass

class ReclamacaoNaoEncontradaException(DefesaConsumidorError):
    pass
