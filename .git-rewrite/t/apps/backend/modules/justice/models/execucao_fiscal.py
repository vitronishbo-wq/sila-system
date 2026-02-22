# auto-generated placeholder
from core.db.base_class import Base  # Use centralized Base


class ExecucaoFiscal(Base):
    __table_args__ = {"extend_existing": True}
    __tablename__ = "justice_execucaofiscals"
    id = Column(Integer, primary_key=True)
