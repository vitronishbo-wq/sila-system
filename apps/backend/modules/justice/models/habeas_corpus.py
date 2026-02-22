# auto-generated placeholder
from config.database import Base  # Use centralized Base


class HabeasCorpus(Base):
    __table_args__ = {"extend_existing": True}
    __tablename__ = "justice_habeascorpuss"
    id = Column(Integer, primary_key=True)

