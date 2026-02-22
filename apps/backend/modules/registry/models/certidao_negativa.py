# auto-generated placeholder
from config.database import Base  # Use centralized Base


class CertidaoNegativa(Base):
    __table_args__ = {"extend_existing": True}
    __tablename__ = "registry_certidaonegativas"
    id = Column(Integer, primary_key=True)

