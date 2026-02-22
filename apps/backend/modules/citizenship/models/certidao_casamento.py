# auto-generated placeholder
from config.database import Base  # Use centralized Base


class CertidaoCasamento(Base):
    __table_args__ = {"extend_existing": True}
    __tablename__ = "citizenship_certidaocasamentos"
    id = Column(Integer, primary_key=True)

