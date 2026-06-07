"""Energy domain exception surface."""


class EnergyDomainError(Exception):
    """Base exception for the energy domain."""


class UsinaAlreadyExistsError(EnergyDomainError):
    """Raised when a usina already exists for the provided key."""


class UsinaNotFoundError(EnergyDomainError):
    """Raised when a usina cannot be found."""


class InvalidUsinaStateError(EnergyDomainError):
    """Raised when a usina state transition is invalid."""


class CentralGeradoraNotFoundError(EnergyDomainError):
    """Raised when a central geradora cannot be found."""


class InvalidCentralGeradoraStateError(EnergyDomainError):
    """Raised when a central geradora state transition is invalid."""


class LinhaTransmissaoNotFoundError(EnergyDomainError):
    """Raised when a linha de transmissao cannot be found."""


class InvalidLinhaTransmissaoStateError(EnergyDomainError):
    """Raised when a linha de transmissao state transition is invalid."""


class SubestacaoNotFoundError(EnergyDomainError):
    """Raised when a subestacao cannot be found."""


class InvalidSubestacaoStateError(EnergyDomainError):
    """Raised when a subestacao state transition is invalid."""


class ConsumoNotFoundError(EnergyDomainError):
    """Raised when a consumo cannot be found."""


class FaturaEnergiaAlreadyExistsError(EnergyDomainError):
    """Raised when an active fatura already exists for a consumo."""


class FaturaEnergiaNotFoundError(EnergyDomainError):
    """Raised when a fatura cannot be found."""


__all__ = [
    "CentralGeradoraNotFoundError",
    "ConsumoNotFoundError",
    "EnergyDomainError",
    "FaturaEnergiaAlreadyExistsError",
    "FaturaEnergiaNotFoundError",
    "InvalidCentralGeradoraStateError",
    "InvalidLinhaTransmissaoStateError",
    "InvalidSubestacaoStateError",
    "InvalidUsinaStateError",
    "LinhaTransmissaoNotFoundError",
    "SubestacaoNotFoundError",
    "UsinaAlreadyExistsError",
    "UsinaNotFoundError",
]
