# auto-generated placeholder
from core.db.base_class import Base  # Use centralized Base


class RegistoMarca(Base):
    __table_args__ = {"extend_existing": True}
    __tablename__ = "commercial_registomarcas"
    id = Column(Integer, primary_key=True)
