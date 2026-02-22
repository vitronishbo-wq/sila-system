# auto-generated placeholder
from config.database import Base  # Use centralized Base


class RelatorioKPI(Base):
    __table_args__ = {"extend_existing": True}
    __tablename__ = "statistics_relatoriokpis"
    id = Column(Integer, primary_key=True)

