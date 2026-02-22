# auto-generated placeholder
from config.database import Base  # Use centralized Base


class AuxilioSocial(Base):
    __table_args__ = {"extend_existing": True}
    __tablename__ = "social_auxiliosocials"
    id = Column(Integer, primary_key=True)

