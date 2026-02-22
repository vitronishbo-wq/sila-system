# auto-generated placeholder
from config.database import Base  # Use centralized Base


class FiscalizacaoMercado(Base):
    __table_args__ = {"extend_existing": True}
    __tablename__ = "commercial_fiscalizacaomercados"
    id = Column(Integer, primary_key=True)

