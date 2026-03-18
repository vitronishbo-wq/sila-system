class OutboxWorker:
    """Worker de outbox (stub) para compatibilidade com deps da API."""

    def __init__(self, *, outbox_repo, event_bus) -> None:
        self.outbox_repo = outbox_repo
        self.event_bus = event_bus

    async def run_once(self) -> int:
        """Executa um ciclo simples de processamento."""
        return 0