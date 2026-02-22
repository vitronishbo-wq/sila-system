# auto-generated placeholder
from config.database import Base  # Use centralized Base


class LeilaoJudicial(Base):
    __table_args__ = {"extend_existing": True}
    __tablename__ = "justice_leilaojudicials"
    id = Column(Integer, primary_key=True)

