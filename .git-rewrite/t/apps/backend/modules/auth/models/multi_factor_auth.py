# auto-generated placeholder
from core.db.base_class import Base  # Use centralized Base


class AutenticacaoMultifator(Base):
    __table_args__ = {"extend_existing": True}
    __tablename__ = "auth_autenticacaomultifators"
    id = Column(Integer, primary_key=True)
