# auto-generated placeholder
from core.db.base_class import Base  # Use centralized Base


class InspecaoSanitaria(Base):
    __table_args__ = {"extend_existing": True}
    __tablename__ = "commercial_inspecaosanitarias"
    id = Column(Integer, primary_key=True)
