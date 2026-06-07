"""Migration for Outbox Event Table - Phase 19"""


def create_outbox_table(engine):
    """Create outbox table if it doesn't exist"""
    from apps.backend.app.core.db.base_class import Base

    Base.metadata.create_all(bind=engine)
