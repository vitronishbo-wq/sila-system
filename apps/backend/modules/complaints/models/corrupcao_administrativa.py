# auto-generated placeholder
from config.database import Base  # Use centralized Base


class CorrupcaoAdministrativa(Base):
    __table_args__ = {"extend_existing": True}
    __tablename__ = "complaints_corrupcaoadministrativas"
    id = Column(Integer, primary_key=True)

