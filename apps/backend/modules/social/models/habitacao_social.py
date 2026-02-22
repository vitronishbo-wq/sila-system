# auto-generated placeholder
from config.database import Base  # Use centralized Base


class HabitacaoSocial(Base):
    __table_args__ = {"extend_existing": True}
    __tablename__ = "social_habitacaosocials"
    id = Column(Integer, primary_key=True)

