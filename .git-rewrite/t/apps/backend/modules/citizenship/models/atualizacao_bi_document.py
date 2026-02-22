"""Models for BI update document handling."""

from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from core.db.base_class import Base


class AtualizacaoBIDocument(Base):
    """Model for storing BI update document references."""

    __tablename__ = "citizenship_bi_update_documents"

    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    bi_update_id = Column(
        Integer,
        ForeignKey("citizenship_atualizacao_b_i.id"),
        nullable=False,
    )
    path = Column(String, nullable=False)
    original_name = Column(String, nullable=False)
    content_type = Column(String, nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    bi_update = relationship(
        "AtualizacaoBI", foreign_keys=[bi_update_id], back_populates="documents"
    )
