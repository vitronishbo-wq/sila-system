# auto-generated placeholder
from config.database import Base  # Use centralized Base


class RegitroEleitoral(Base):
    __table_args__ = {"extend_existing": True}
    __tablename__ = "citizenship_regitroeleitorals"
    id = Column(Integer, primary_key=True)

