# auto-generated placeholder
from core.db.base_class import Base  # Use centralized Base


class CertificacaoOrigem(Base):
    __table_args__ = {"extend_existing": True}
    __tablename__ = "commercial_certificacaoorigems"
    id = Column(Integer, primary_key=True)
