# auto-generated placeholder
from core.db.base_class import Base  # Use centralized Base


class EmergenciaMedica(Base):
    __table_args__ = {"extend_existing": True}
    __tablename__ = "health_emergenciamedicas"
    id = Column(Integer, primary_key=True)
