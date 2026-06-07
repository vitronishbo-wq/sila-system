class StubAsyncService:
    """Stub async service for router import compatibility."""

    def __getattr__(self, name):

        async def _missing(*_args, **_kwargs):
            raise NotImplementedError(f"Servico nao implementado: {self.__class__.__name__}.{name}")

        return _missing
