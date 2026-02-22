# auto-generated placeholder model (minimal, valid SQLAlchemy)
from sqlalchemy import Column, Integer, String

from config.database import Base  # Use centralized Base

# Remove local Base creation


class AtualizacaoEndereco(Base):
    __table_args__ = {"extend_existing": True}
    __tablename__ = "citizenship_atualizacaoenderecos"

    id = Column(Integer, primary_key=True)
    rua = Column(String, nullable=True)
    numero = Column(String, nullable=True)
    municipio = Column(String, nullable=True)

