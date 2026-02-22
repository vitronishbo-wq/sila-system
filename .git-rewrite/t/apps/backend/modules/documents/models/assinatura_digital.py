# auto-generated placeholder
from core.db.base_class import Base  # Use centralized Base


class AssinaturaDigital(Base):
    __table_args__ = {"extend_existing": True}
    __tablename__ = "documents_assinaturadigitals"
    id = Column(Integer, primary_key=True)
