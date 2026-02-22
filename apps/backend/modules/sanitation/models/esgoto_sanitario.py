# auto-generated placeholder
from config.database import Base  # Use centralized Base


class EsgotoSanitario(Base):
    __table_args__ = {"extend_existing": True}
    __tablename__ = "sanitation_esgotosanitarios"
    id = Column(Integer, primary_key=True)

