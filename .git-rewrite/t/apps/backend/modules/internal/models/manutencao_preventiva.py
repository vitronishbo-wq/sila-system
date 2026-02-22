# auto-generated placeholder
from core.db.base_class import Base  # Use centralized Base


class ManutencaoPreventiva(Base):
    __table_args__ = {"extend_existing": True}
    __tablename__ = "internal_manutencaopreventivas"
    id = Column(Integer, primary_key=True)
