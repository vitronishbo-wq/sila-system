# auto-generated placeholder
from config.database import Base  # Use centralized Base


class VistoPermanencia(Base):
    __table_args__ = {"extend_existing": True}
    __tablename__ = "citizenship_vistopermanencias"
    id = Column(Integer, primary_key=True)

