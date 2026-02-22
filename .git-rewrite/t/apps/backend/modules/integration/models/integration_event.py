# auto-generated placeholder
from core.db.base_class import Base  # Use centralized Base


class IntegrationEvent(Base):
    __table_args__ = {"extend_existing": True}
    __tablename__ = "integration_integrationevents"
    id = Column(Integer, primary_key=True)
