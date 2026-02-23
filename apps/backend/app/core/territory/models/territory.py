import uuid
from sqlalchemy import String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

class Territory(Base):
    __tablename__ = "territories"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String, index=True)
    code: Mapped[str | None] = mapped_column(String, unique=True, nullable=True, index=True)
    
    # 'province', 'municipality', 'commune'
    type: Mapped[str] = mapped_column(String) 
    
    # Permite que um município não tenha comuna, ou uma província seja o topo
    parent_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), 
        ForeignKey("locations.id", ondelete="CASCADE"), 
        nullable=True
    )
    
    # Relacionamento para navegar na árvore (Ex: província.children retorna municípios)
    parent = relationship("Territory", remote_side=[id], back_populates="children")
    children = relationship("Territory", back_populates="parent", cascade="all, delete")

