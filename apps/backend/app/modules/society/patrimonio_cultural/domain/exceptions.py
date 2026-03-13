class PatrimonioDomainError(Exception):
    """Base exception for patrimonio cultural domain errors."""

class AssetAlreadyClassifiedError(PatrimonioDomainError):
    """Raised when a downgrade classification is requested."""

class InvalidClassificationAuthorityError(PatrimonioDomainError):
    """Raised when authority is invalid."""

class ProtectedAssetModificationError(PatrimonioDomainError):
    """Raised when modification requires protected status and is not allowed."""

class UNESCOPreconditionError(PatrimonioDomainError):
    """Raised when UNESCO preconditions are not met."""

class AssetNotFoundError(PatrimonioDomainError):
    """Raised when asset does not exist."""

    def __init__(self, asset_id: str):
        super().__init__(f'Patrimonio {asset_id} nao encontrado')