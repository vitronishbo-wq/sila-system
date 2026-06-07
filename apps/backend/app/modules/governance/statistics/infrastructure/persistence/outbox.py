class Outbox:
    def enqueue(self, event: dict) -> None:
        _ = event
