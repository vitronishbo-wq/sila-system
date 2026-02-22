# auto-generated placeholder
from config.database import Base  # Use centralized Base


class ValidacaoCEP(Base):
    __table_args__ = {"extend_existing": True}
    __tablename__ = "address_validacaoceps"
    id = Column(Integer, primary_key=True)

