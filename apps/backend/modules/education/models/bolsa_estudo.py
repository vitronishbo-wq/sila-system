# auto-generated placeholder
from config.database import Base  # Use centralized Base


class BolsaEstudo(Base):
    __table_args__ = {"extend_existing": True}
    __tablename__ = "education_bolsaestudos"
    id = Column(Integer, primary_key=True)

