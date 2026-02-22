# auto-generated placeholder
from config.database import Base  # Use centralized Base


class AgenteSanitario(Base):
    __table_args__ = {"extend_existing": True}
    __tablename__ = "sanitation_agentesanitarios"
    id = Column(Integer, primary_key=True)

