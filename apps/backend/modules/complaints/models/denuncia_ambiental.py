# auto-generated placeholder
from config.database import Base  # Use centralized Base


class DenunciaAmbiental(Base):
    __table_args__ = {"extend_existing": True}
    __tablename__ = "complaints_denunciaambientals"
    id = Column(Integer, primary_key=True)

