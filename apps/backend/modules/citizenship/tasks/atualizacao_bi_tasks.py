"""Task handler stubs for BI update background processing used in tests.

These are minimal placeholders so routes can import the expected symbols
during test collection. Tests typically patch task functions rather than
calling these directly.
"""


class BITaskHandler:
    """Placeholder task handler with minimal API."""

    @staticmethod
    def send_bi_update_notification(bi_id: int, event_type: str, recipient: str):
        # no-op for triage
        return None
