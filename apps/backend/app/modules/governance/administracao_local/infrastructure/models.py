from sqlalchemy import Column, String
from app.db.base import Base

class AdministradorModel(Base):
    __tablename__ = 'administradores_locais'
    id = Column(String, primary_key=True)
    nome = Column(String, nullable=False)
    cargo = Column(String, nullable=False)