from __future__ import annotations
import uuid
from datetime import datetime, timezone

class PaymentService:
    """Minimal sync adapter for treasury orchestration flows."""

    def create_payment(self, db, data: dict):
        return {'id': str(uuid.uuid4()), 'citizen_id': data.get('citizen_id'), 'amount': data.get('amount'), 'type': data.get('type'), 'status': 'created', 'created_at': datetime.now(timezone.utc).isoformat()}