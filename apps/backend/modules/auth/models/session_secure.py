# auto-generated placeholder
from config.database import Base  # Use centralized Base


class SessaoSegura(Base):
    __table_args__ = {"extend_existing": True}
    __tablename__ = "auth_sessaoseguras"
    id = Column(Integer, primary_key=True)

