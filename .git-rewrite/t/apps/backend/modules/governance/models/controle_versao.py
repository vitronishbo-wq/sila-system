from sqlalchemy import Column, Integer

from core.db.base_class import Base  # Use centralized Base

# Remove local Base creation


class ControleVersao(Base):
    __tablename__ = "governance_controleversaos"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True)
