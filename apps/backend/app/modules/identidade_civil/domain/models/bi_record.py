"""
BI ORM Model - Persistência de Bilhetes de Identidade

Migração do dataclass para SQLAlchemy para garantir persistência robusta
em produção com auditoria e versionamento.
"""
import uuid
from datetime import date, datetime
from sqlalchemy import String, Date, DateTime, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base


class BIRecord(Base):
    """
    Registro persistente de Bilhetes de Identidade.
    
    Esta tabela armazena apenas metadados e status administrativo.
    Dados biográficos (nome, filiação, etc) são SEMPRE consultados no FUC.
    
    INVARIANTES:
    - citizen_fuc_id: Referência LÓGICA ao FUC (não FK, pois FUC é sistema externo)
    - bi_number: Formato validado XXXXXXXXXXXX
    - status: Uma de {DRAFT, ACTIVE, EXPIRED, SUSPENDED, CANCELLED, LOST}
    - issue_date/expiry_date: Não podem ser editados após ACTIVE
    """
    __tablename__ = "bi_records"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    
    # Referência ao cidadão no FUC (Soberania)
    citizen_fuc_id: Mapped[str] = mapped_column(String(50), index=True, nullable=False)
    
    # Número do BI (formato XXXXXXXXXXXX)
    bi_number: Mapped[str] = mapped_column(String(14), unique=True, nullable=False, index=True)
    
    # Datas
    issue_date: Mapped[date] = mapped_column(Date, nullable=False)
    expiry_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    
    # Status administrativo
    status: Mapped[str] = mapped_column(String(30), default="draft", nullable=False, index=True)
    
    # Versionamento para imutabilidade lógica
    version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    
    # Auditoria
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False, index=True
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )
    
    # Rastreamento de motivo (para cancelamento, suspenção, etc)
    reason_for_status: Mapped[str | None] = mapped_column(String(500), nullable=True)

    @property
    def is_valid(self) -> bool:
        """Verifica se o documento é válido para identificação oficial."""
        if self.status != "active":
            return False
        if self.expiry_date and self.expiry_date < date.today():
            return False
        return True

    @property
    def is_expired(self) -> bool:
        """Verifica se o documento já passou da data de validade."""
        return self.expiry_date is not None and self.expiry_date < date.today()

    def __repr__(self):
        return f"<BIRecord {self.bi_number} - {self.status}>"
