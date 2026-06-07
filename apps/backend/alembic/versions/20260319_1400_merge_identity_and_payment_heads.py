"""merge identity and payment heads

Revision ID: 20260319_1400_merge_identity_and_payment_heads
Revises: 20260318_1800_create_identity_biometrics, 20260319_1300_add_payment_taxpayer_tables
Create Date: 2026-03-19 14:00:00.000000
"""

from __future__ import annotations

revision: str = "20260319_1400_merge_identity_and_payment_heads"
down_revision = (
    "20260318_1800_create_identity_biometrics",
    "20260319_1300_add_payment_taxpayer_tables",
)
branch_labels = None
depends_on = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
