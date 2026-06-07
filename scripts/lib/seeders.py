"""
Shared seeders for SILA system - consolidates user and location seeding logic.
This module reduces duplication across seed_*.py scripts.
"""

import logging
from typing import Any
from uuid import uuid4

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


class BaseSeeder:
    """Base seeder class with common utilities."""
    
    def __init__(self, session: AsyncSession):
        """
        Initialize seeder with database session.
        
        Args:
            session: SQLAlchemy AsyncSession
        """
        self.session = session
    
    async def execute_raw(self, query: str) -> Any:
        """Execute raw SQL query."""
        result = await self.session.execute(text(query))
        return result
    
    async def fetch_one(self, query: str) -> Any | None:
        """Fetch single row."""
        result = await self.execute_raw(query)
        return result.scalar()


class LocationSeeder(BaseSeeder):
    """Seeder for locations (provinces, municipalities, communes)."""
    
    async def seed_province(self, 
                          name: str,
                          code: str | None = None,
                          parent_id: int | None = None,
                          type: str = "province") -> int:
        """
        Seed a province/location with upsert logic.
        
        Args:
            name: Location name  
            code: Optional location code
            parent_id: Parent location ID for hierarchy
            type: Location type (province, municipality, commune, etc.)
        
        Returns:
            Location ID
        """
        query = f"""
            INSERT INTO locations (name, code, type, parent_id, created_at)
            VALUES ('{name}', {"NULL" if not code else f"'{code}'"}, '{type}', 
                    {"NULL" if not parent_id else parent_id}, NOW())
            ON CONFLICT (name, type, parent_id) DO UPDATE SET updated_at = NOW()
            RETURNING id;
        """
        location_id = await self.fetch_one(query)
        logger.info(f"✅ Seeded {type}: {name} (id={location_id})")
        return location_id
    
    async def seed_provinces_law_14_24(self) -> dict[str, int]:
        """
        Seed all 21 provinces according to Lei 14/24 (Angola).
        
        Returns:
            Dictionary mapping province names to their IDs
        """
        provinces = [
            "Bengo", "Benguela", "Bié", "Cabinda", "Cunene",
            "Huambo", "Huíla", "Kwando Kubango", "Kwanza-Norte",
            "Kwanza-Sul", "Luanda", "Lunda-Norte", "Lunda-Sul",
            "Malange", "Moxico", "Namibe", "Uíge", "Zaire",
            "Província de Cabinda", "Municipio de Luanda", "Chitato"
        ]
        
        prov_ids = {}
        for prov in provinces:
            prov_id = await self.seed_province(prov)
            prov_ids[prov] = prov_id
        
        logger.info(f"✅ Seeded {len(prov_ids)} provinces from Lei 14/24")
        return prov_ids


class UserSeeder(BaseSeeder):
    """Seeder for users (admins, managers, officers, citizens)."""
    
    async def seed_user(self,
                       email: str,
                       full_name: str,
                       password_hash: str,
                       roles: list[str],
                       administrative_level: str | None = None,
                       region_id: int | None = None,
                       bi_number: str | None = None,
                       phone: str | None = None) -> str:
        """
        Seed a user with upsert logic.
        
        Args:
            email: User email (unique)
            full_name: Full name
            password_hash: Hashed password
            roles: List of roles (e.g., ["ADMIN", "MANAGER"])
            administrative_level: SUPER, NATIONAL, PROVINCIAL, MUNICIPAL, COMUNAL, CITIZEN
            region_id: Location/region ID
            bi_number: Identification/BI number
            phone: Phone number
        
        Returns:
            User ID (UUID)
        """
        user_id = str(uuid4())
        roles_json = str(roles).replace("'", '"')  # Convert to JSON format
        
        admin_level_val = 'NULL' if not administrative_level else f"'{administrative_level}'"
        region_val = 'NULL' if not region_id else region_id
        bi_val = 'NULL' if not bi_number else f"'{bi_number}'"
        phone_val = 'NULL' if not phone else f"'{phone}'"
        
        query = f"""
            INSERT INTO users 
            (id, email, full_name, password_hash, roles, administrative_level, 
             region_id, bi_number, phone, created_at)
            VALUES 
            ('{user_id}', '{email}', '{full_name}', '{password_hash}', 
             '{roles_json}'::jsonb, {admin_level_val}, 
             {region_val}, 
             {bi_val}, 
             {phone_val}, 
             NOW())
            ON CONFLICT (email) DO UPDATE 
            SET password_hash = EXCLUDED.password_hash,
                updated_at = NOW()
            RETURNING id;
        """
        
        result_id = await self.fetch_one(query)
        logger.info(f"✅ Seeded user: {email} (id={result_id}, roles={roles})")
        return result_id
    
    async def seed_admin_user(self,
                             email: str,
                             full_name: str,
                             password_hash: str) -> str:
        """Convenience method to seed ADMIN user."""
        return await self.seed_user(
            email=email,
            full_name=full_name,
            password_hash=password_hash,
            roles=["ADMIN"],
            administrative_level="SUPER"
        )
    
    async def seed_manager_user(self,
                               email: str,
                               full_name: str,
                               password_hash: str,
                               region_id: int,
                               administrative_level: str = "PROVINCIAL") -> str:
        """Convenience method to seed MANAGER user."""
        return await self.seed_user(
            email=email,
            full_name=full_name,
            password_hash=password_hash,
            roles=["MANAGER"],
            administrative_level=administrative_level,
            region_id=region_id
        )
    
    async def seed_citizen_user(self,
                               email: str,
                               full_name: str,
                               password_hash: str,
                               bi_number: str | None = None) -> str:
        """Convenience method to seed CITIZEN user."""
        return await self.seed_user(
            email=email,
            full_name=full_name,
            password_hash=password_hash,
            roles=["CITIZEN"],
            administrative_level="CITIZEN",
            bi_number=bi_number
        )


class TerritorySeeder(BaseSeeder):
    """Seeder for user-territory relationships."""
    
    async def bind_user_to_territory(self,
                                     user_id: str,
                                     location_id: int) -> bool:
        """
        Bind a user to a territory/location.
        
        Args:
            user_id: User UUID
            location_id: Location ID
        
        Returns:
            True if successful
        """
        query = f"""
            INSERT INTO user_territories (user_id, location_id, created_at)
            VALUES ('{user_id}', {location_id}, NOW())
            ON CONFLICT (user_id, location_id) DO NOTHING;
        """
        await self.execute_raw(query)
        logger.info(f"✅ Bound user {user_id} to territory {location_id}")
        return True
