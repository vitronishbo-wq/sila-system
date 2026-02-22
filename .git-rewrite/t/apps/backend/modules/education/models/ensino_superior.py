# /opt/sila-system/backend/modules/education/models/ensino_superior.py

from sqlalchemy import Column, DateTime, Integer, String

from core.db.base_class import Base  # Centralized Base from your project


class EnsinoSuperior(Base):
    __tablename__ = "education_ensinosuperiors"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), nullable=False)
    sigla = Column(String(50), nullable=True)
    criado_em = Column(DateTime, nullable=True)
