# auto-generated placeholder
from core.db.base_class import Base  # Use centralized Base


class MonitoramentoSistema(Base):
    __table_args__ = {"extend_existing": True}
    __tablename__ = "internal_monitoramentosistemas"
    id = Column(Integer, primary_key=True)
