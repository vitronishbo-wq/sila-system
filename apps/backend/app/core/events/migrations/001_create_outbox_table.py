"""Migration for Outbox Event Table - Phase 19"""
from sqlalchemy import Column, String, JSON, DateTime, Boolean, TIMESTAMP, create_engine
from datetime import datetime
from uuid import uuid4

def create_outbox_table(engine):
    """Create outbox table if it doesn't exist"""
    from app.core.db.base_class import Base
    from app.core.events.outbox.outbox_model import OutboxEvent
    Base.metadata.create_all(bind=engine)