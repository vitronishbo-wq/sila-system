# auto-generated placeholder
from core.db.base_class import Base  # Use centralized Base


class MonitoramentoAmbiental(Base):
    __table_args__ = {"extend_existing": True}
    __tablename__ = "sanitation_monitoramentoambientals"
    id = Column(Integer, primary_key=True)
