# auto-generated placeholder
from config.database import Base  # Use centralized Base


class SugestaoMelhoria(Base):
    __table_args__ = {"extend_existing": True}
    __tablename__ = "complaints_sugestaomelhorias"
    id = Column(Integer, primary_key=True)

