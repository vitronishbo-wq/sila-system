"""Application ports (interfaces for external services)"""


class RepositoryPort:
    """Port for repository implementations"""

    pass


class ServicePort:
    """Port for external service calls"""

    pass


__all__ = ["RepositoryPort", "ServicePort"]
