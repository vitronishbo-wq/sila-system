# auto-generated placeholder
from config.database import Base  # Use centralized Base


class NormalizacaoEndereco(Base):
    __table_args__ = {"extend_existing": True}
    __tablename__ = "address_normalizacaoenderecos"
    id = Column(Integer, primary_key=True)

