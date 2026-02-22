# auto-generated placeholder
from config.database import Base  # Use centralized Base


class TutelaMenor(Base):
    __table_args__ = {"extend_existing": True}
    __tablename__ = "registry_tutelamenors"
    id = Column(Integer, primary_key=True)

