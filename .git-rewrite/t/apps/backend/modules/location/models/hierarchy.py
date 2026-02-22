"""Hierarchical location models - Country > Province > Municipality > Commune > City > Address."""

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from core.db.base_class import Base


class CountryModel(Base):
    """Country level - Top of hierarchy."""

    __tablename__ = "location_countries"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    code = Column(String, unique=True, index=True)

    provinces = relationship("ProvinceModel", back_populates="country")


class ProvinceModel(Base):
    """Province level - Within a country."""

    __tablename__ = "location_provinces"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    country_id = Column(Integer, ForeignKey("location_countries.id"))

    country = relationship(
        "CountryModel", foreign_keys=[country_id], back_populates="provinces"
    )
    municipalities = relationship("MunicipalityModel", back_populates="province")


class MunicipalityModel(Base):
    """Municipality level - Within a province."""

    __tablename__ = "location_municipalities"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    province_id = Column(Integer, ForeignKey("location_provinces.id"))

    province = relationship(
        "ProvinceModel", foreign_keys=[province_id], back_populates="municipalities"
    )
    communes = relationship("CommuneModel", back_populates="municipality")


class CommuneModel(Base):
    """Commune level - Within a municipality."""

    __tablename__ = "location_communes"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    municipality_id = Column(Integer, ForeignKey("location_municipalities.id"))

    municipality = relationship(
        "MunicipalityModel", foreign_keys=[municipality_id], back_populates="communes"
    )
    cities = relationship("CityModel", back_populates="commune")
    addresses = relationship("FullAddress", back_populates="commune")


class CityModel(Base):
    """City level - Within a commune."""

    __tablename__ = "location_cities"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    commune_id = Column(Integer, ForeignKey("location_communes.id"))

    commune = relationship(
        "CommuneModel", foreign_keys=[commune_id], back_populates="cities"
    )


class FullAddress(Base):
    """Full address - Within a commune."""

    __tablename__ = "location_full_addresses"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    street = Column(String)
    number = Column(String)
    zip_code = Column(String)

    commune_id = Column(Integer, ForeignKey("location_communes.id"))
    commune = relationship(
        "CommuneModel", foreign_keys=[commune_id], back_populates="addresses"
    )
