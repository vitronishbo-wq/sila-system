"""Business rules for BI update requests (minimal stub for tests).

The real implementation lives elsewhere; tests only need the symbol to be
importable during collection and may patch behaviours as needed.
"""


class BIBusinessRules:
    """Minimal placeholder for business rules used by routes/tests."""

    @staticmethod
    def validate_bi_update(data):
        # In triage we accept any data
        return True


# auto-generated placeholder
