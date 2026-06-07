from __future__ import annotations


class PatrimonioDomainError(Exception):
    pass


class AssetAlreadyClassifiedError(PatrimonioDomainError):
    pass

class AssetNotFoundError(PatrimonioDomainError):
    pass

class InvalidClassificationAuthorityError(PatrimonioDomainError):
    pass

class ProtectedAssetModificationError(PatrimonioDomainError):
    pass

class UNESCOPreconditionError(PatrimonioDomainError):
    pass
