# auto-generated placeholder
from core.db.base_class import Base  # Use centralized Base


class CursoTecnico(Base):
    __table_args__ = {"extend_existing": True}
    __tablename__ = "education_cursotecnicos"
    id = Column(Integer, primary_key=True)
