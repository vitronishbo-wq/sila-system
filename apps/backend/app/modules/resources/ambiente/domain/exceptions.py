from __future__ import annotations


class AmbienteError(Exception):
    pass


class AutoInfracaoNotFoundError(AmbienteError):
    pass

class CARAlreadyExistsError(AmbienteError):
    pass

class CARNotFoundError(AmbienteError):
    pass

class CondicionanteNotFoundError(AmbienteError):
    pass

class EmbargoNotFoundError(AmbienteError):
    pass

class EstudoNotFoundError(AmbienteError):
    pass

class FiscalizacaoNotFoundError(AmbienteError):
    pass

class ImovelNotFoundError(AmbienteError):
    pass

class LicencaAlreadyExistsError(AmbienteError):
    pass

class LicencaNotFoundError(AmbienteError):
    pass

class MultaNotFoundError(AmbienteError):
    pass

class ProprietarioAlreadyExistsError(AmbienteError):
    pass

class ProprietarioNotFoundError(AmbienteError):
    pass
