# auto-generated placeholder
from config.database import Base  # Use centralized Base


class ControleAcesso(Base):
    __table_args__ = {"extend_existing": True}
    __tablename__ = "auth_controleacessos"
    id = Column(Integer, primary_key=True)

