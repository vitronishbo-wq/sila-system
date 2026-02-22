from datetime import datetime

from sqlalchemy import JSON, Boolean, Column, DateTime, Integer, String

from config.database import Base


class AlvaraFuncionamento(Base):
    __table_args__ = {"extend_existing": True}
    __tablename__ = "urbanism_alvara_funcionamento"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(200), nullable=False)
    nome_en = Column(String(200), nullable=False)  # English name
    descricao = Column(String(500))
    descricao_en = Column(String(500))  # English description
    ativo = Column(Boolean, default=True)
    data_criacao = Column(DateTime, default=datetime.utcnow)
    dados_adicionais = Column(JSON)  # For flexible additional data
    # Conditional relationship based on service type
    municipe_id = Column(Integer, nullable=False)  # Only for citizen services
    status = Column(String(50), default="pendente")

