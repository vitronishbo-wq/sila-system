"""Service Hub Models - ORM definitions"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime

from core.db.base_class import Base


class ServiceCategory(Base):
    __tablename__ = "service_hub_servicecategorys"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(String(1024), nullable=True)


class ServiceScope(Base):
    __tablename__ = "service_hub_servicescopes"
    id = Column(Integer, primary_key=True)


class Service(Base):
    __tablename__ = "services"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Relationship with Service Locations
    locations: Mapped[list["ServiceLocation"]] = relationship(
        "ServiceLocation",
        back_populates="service",
        cascade="all, delete-orphan",
        lazy="selectin",
    )


class ServiceLocation(Base):
    __tablename__ = "service_locations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    service_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("services.id", ondelete="CASCADE"), nullable=False
    )
    province: Mapped[str] = mapped_column(String(255), nullable=False)
    address: Mapped[str | None] = mapped_column(String(500), nullable=True)

    # Relationship back to Service
    service: Mapped["Service"] = relationship(
        "Service", back_populates="locations", lazy="selectin"
    )
