# auto-generated placeholder
from config.database import Base  # Use centralized Base


class FiscalizacaoObra(Base):
    __table_args__ = {"extend_existing": True}
    __tablename__ = "complaints_fiscalizacaoobras"
    id = Column(Integer, primary_key=True)

