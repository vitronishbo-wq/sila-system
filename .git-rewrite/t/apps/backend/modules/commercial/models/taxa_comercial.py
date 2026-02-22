# auto-generated placeholder
from core.db.base_class import Base  # Use centralized Base


class TaxaComercial(Base):
    __table_args__ = {"extend_existing": True}
    __tablename__ = "commercial_taxacomercials"
    id = Column(Integer, primary_key=True)
