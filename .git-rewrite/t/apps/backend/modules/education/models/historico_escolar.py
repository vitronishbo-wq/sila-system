# auto-generated placeholder
from core.db.base_class import Base  # Use centralized Base


class HistoricoEscolar(Base):
    __table_args__ = {"extend_existing": True}
    __tablename__ = "education_historicoescolars"
    id = Column(Integer, primary_key=True)
