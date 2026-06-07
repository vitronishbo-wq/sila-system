from __future__ import annotations

import json
import os
from typing import Any


class NotificationService:
    """Unified notification service (email/sms/push placeholder).

    Channels are pluggable via simple mapping. For production replace
    with channel adapters (SMTP, Twilio, WhatsApp API, FCM, etc.).
    """

    def __init__(self, storage_path: str | None = None) -> None:
        self.channels = {"email": self._store, "sms": self._store}
        self.storage_path = storage_path or "data/foundation_notifications.jsonl"
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)

    def _store(self, to: str, subject: str, body: str, meta: dict[str, Any] | None = None) -> None:
        record = {"to": to, "subject": subject, "body": body, "meta": meta}
        with open(self.storage_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, default=str) + "\n")

    def send(self, channel: str, to: str, subject: str, body: str, meta: dict[str, Any] | None = None) -> None:
        sender = self.channels.get(channel)
        if not sender:
            raise ValueError(f"unknown channel: {channel}")
        sender(to, subject, body, meta)
