# auto-generated placeholder
from config.database import Base  # Use centralized Base


class MerendaEscolar(Base):
    __table_args__ = {"extend_existing": True}
    __tablename__ = "education_merendaescolars"
    id = Column(Integer, primary_key=True)

