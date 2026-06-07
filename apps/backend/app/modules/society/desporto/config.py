from dataclasses import dataclass


@dataclass(frozen=True)
class DesportoConfig:
    outbox_batch_size: int = 100
    outbox_poll_interval_seconds: int = 10
    outbox_lock_ttl_seconds: int = 60
    outbox_retry_delay_seconds: int = 5
    ranking_refresh_seconds: int = 300
    resilience_retries: int = 3
    resilience_backoff_seconds: float = 0.5
