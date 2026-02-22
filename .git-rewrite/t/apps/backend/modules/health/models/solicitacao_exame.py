# auto-generated placeholder
from core.db.base_class import Base  # Use centralized Base


class SolicitacaoExame(Base):
    __table_args__ = {"extend_existing": True}
    __tablename__ = "health_solicitacaoexames"
    id = Column(Integer, primary_key=True)
