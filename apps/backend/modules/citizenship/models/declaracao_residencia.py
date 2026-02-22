# auto-generated placeholder
from config.database import Base  # Use centralized Base


class DeclaracaoResidencia(Base):
    __table_args__ = {"extend_existing": True}
    __tablename__ = "citizenship_declaracaoresidencias"
    id = Column(Integer, primary_key=True)

