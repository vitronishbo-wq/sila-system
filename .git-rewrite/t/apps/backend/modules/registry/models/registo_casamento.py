# auto-generated placeholder
from core.db.base_class import Base  # Use centralized Base


class RegistoCasamento(Base):
    __table_args__ = {"extend_existing": True}
    __tablename__ = "registry_registocasamentos"
    id = Column(Integer, primary_key=True)
