from __future__ import annotations


class GestaoFundiariaError(Exception):
    pass


class DesapropriacaoAlreadyExistsError(GestaoFundiariaError):
    pass

class DesapropriacaoNotFoundError(GestaoFundiariaError):
    pass

class GeorreferenciamentoAlreadyExistsError(GestaoFundiariaError):
    pass

class GeorreferenciamentoNotFoundError(GestaoFundiariaError):
    pass

class ImovelAlreadyExistsError(GestaoFundiariaError):
    pass

class ImovelNotFoundError(GestaoFundiariaError):
    pass

class MatriculaImovelAlreadyExistsError(GestaoFundiariaError):
    pass

class MatriculaImovelNotFoundError(GestaoFundiariaError):
    pass

class OneracaoAlreadyExistsError(GestaoFundiariaError):
    pass

class OneracaoNotFoundError(GestaoFundiariaError):
    pass

class ProprietarioAlreadyExistsError(GestaoFundiariaError):
    pass

class ProprietarioNotFoundError(GestaoFundiariaError):
    pass
