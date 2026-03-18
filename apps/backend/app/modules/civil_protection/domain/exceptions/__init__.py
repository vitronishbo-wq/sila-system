"""Domain exceptions"""

class DomainException(Exception):
    """Base domain exception"""

    def __init__(self, message: str, code: str='DOMAIN_ERROR'):
        self.message = message
        self.code = code
        super().__init__(f'[{code}] {message}')

class EntityNotFoundError(DomainException):
    """Entity not found in repository"""

    def __init__(self, entity_type: str, entity_id: str):
        super().__init__(f'{entity_type} with ID {entity_id} not found', 'ENTITY_NOT_FOUND')

class InvalidEntityError(DomainException):
    """Entity validation failed"""

    def __init__(self, message: str):
        super().__init__(message, 'INVALID_ENTITY')

class RepositoryError(DomainException):
    """Repository operation failed"""

    def __init__(self, message: str):
        super().__init__(message, 'REPOSITORY_ERROR')
__all__ = ['DomainException', 'EntityNotFoundError', 'InvalidEntityError', 'RepositoryError']