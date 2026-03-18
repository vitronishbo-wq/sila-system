class EnergyException(Exception):
    pass

class CentralGeradoraNotFoundError(EnergyException):
    pass

class InvalidCentralGeradoraStateError(EnergyException):
    pass

class SubestacaoNotFoundError(EnergyException):
    pass

class InvalidSubestacaoStateError(EnergyException):
    pass

class LinhaTransmissaoNotFoundError(EnergyException):
    pass

class InvalidLinhaTransmissaoStateError(EnergyException):
    pass
__all__ = ['EnergyException', 'CentralGeradoraNotFoundError', 'InvalidCentralGeradoraStateError', 'SubestacaoNotFoundError', 'InvalidSubestacaoStateError', 'LinhaTransmissaoNotFoundError', 'InvalidLinhaTransmissaoStateError', 'ConsumoNotFoundError', 'FaturaEnergiaAlreadyExistsError', 'FaturaEnergiaNotFoundError', 'UsinaAlreadyExistsError', 'UsinaNotFoundError', 'InvalidUsinaStateError']

class ConsumoNotFoundError(EnergyException):
    pass

class FaturaEnergiaAlreadyExistsError(EnergyException):
    pass

class FaturaEnergiaNotFoundError(EnergyException):
    pass

class UsinaAlreadyExistsError(EnergyException):
    pass

class UsinaNotFoundError(EnergyException):
    pass

class InvalidUsinaStateError(EnergyException):
    pass