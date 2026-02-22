# auto-generated placeholder
from config.database import Base  # Use centralized Base


class CertidaoNascimento(Base):
    __table_args__ = {"extend_existing": True}
    __tablename__ = "citizenship_certidaonascimentos"
    id = Column(Integer, primary_key=True)

