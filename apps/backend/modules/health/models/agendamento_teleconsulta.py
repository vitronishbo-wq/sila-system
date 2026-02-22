# auto-generated placeholder
from config.database import Base  # Use centralized Base


class AgendamentoTeleconsulta(Base):
    __table_args__ = {"extend_existing": True}
    __tablename__ = "health_agendamentoteleconsultas"
    id = Column(Integer, primary_key=True)

