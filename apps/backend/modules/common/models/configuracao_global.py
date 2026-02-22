# auto-generated placeholder
from config.database import Base  # Use centralized Base


class ConfiguracaoGlobal(Base):
    __table_args__ = {"extend_existing": True}
    __tablename__ = "common_configuracaoglobals"
    id = Column(Integer, primary_key=True)

