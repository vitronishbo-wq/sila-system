import uuid
import datetime
from sqlalchemy import String, ForeignKey, DateTime, JSON, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base

class DocumentFile(Base):
    """
    Representação de um ficheiro físico no sistema (Anexos, Biometria, Scans).
    """
    __tablename__ = "document_files"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Dono do ficheiro (Cidadão ou Pedido)
    owner_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), index=True, nullable=False)
    owner_type: Mapped[str] = mapped_column(String(50), index=True, nullable=False) # 'citizen', 'request'
    
    # Metadados do Ficheiro
    file_name: Mapped[str] = mapped_column(String(255), nullable=False)
    file_path: Mapped[str] = mapped_column(String(512), nullable=False) # Caminho relativo no storage
    content_type: Mapped[str | None] = mapped_column(String(100), nullable=True)
    file_size: Mapped[int | None] = mapped_column(nullable=True) # em bytes
    
    # Tipo de conteúdo (PHOTO, FINGERPRINT_LEFT_INDEX, etc)
    category: Mapped[str] = mapped_column(String(50), index=True) 
    
    meta_data: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)
    
    def __repr__(self):
        return f"<DocumentFile {self.file_name} ({self.category})>"
