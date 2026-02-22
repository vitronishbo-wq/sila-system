import uuid
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


class ServicePermission(Base):
    """
    Tabela de junção entre Services e Permissions.
    Permite associar múltiplas permissões a um serviço.
    """
    __tablename__ = "service_permissions"

    service_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("services.id", ondelete="CASCADE"),
        primary_key=True,
        index=True
    )
    permission_id: Mapped[int] = mapped_column(
        ForeignKey("permissions.id", ondelete="CASCADE"),
        primary_key=True,
        index=True
    )

    # Relacionamentos (opcional, para navegação)
    # service: Mapped["Service"] = relationship(back_populates="permissions")
    # permission: Mapped["Permission"] = relationship(back_populates="services")
