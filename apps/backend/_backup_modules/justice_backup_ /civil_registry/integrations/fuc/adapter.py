from .client import CitizenFUCClient

class FUCAdapter(CitizenFUCClient):
    """Alias adapter that preserves the legacy integration semantics."""
    pass
__all__ = ['FUCAdapter']