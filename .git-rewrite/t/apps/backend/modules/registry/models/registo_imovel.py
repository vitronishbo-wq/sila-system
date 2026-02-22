# auto-generated placeholder
from core.db.base_class import Base  # Use centralized Base


class RegistoImovel(Base):
    __table_args__ = {"extend_existing": True}
    __tablename__ = "registry_registoimovels"
    id = Column(Integer, primary_key=True)
