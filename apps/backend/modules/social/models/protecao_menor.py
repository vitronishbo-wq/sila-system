# auto-generated placeholder
from config.database import Base  # Use centralized Base


class ProtecaoMenor(Base):
    __table_args__ = {"extend_existing": True}
    __tablename__ = "social_protecaomenors"
    id = Column(Integer, primary_key=True)

