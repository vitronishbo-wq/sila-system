from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import uuid4, UUID
from datetime import datetime
from typing import Optional, Dict, Any

from app.citizen.core.models import CitizenFUC
from app.core.events import publish_event
from app.core.audit import audit_log

class CitizenService:
    """Serviço REAL de cidadãos - sem stubs"""
    
    def __init__(self, db: AsyncSession, **kwargs):
        for k, v in kwargs.items(): setattr(self, k, v)
        self.db = db
    
    async def create_citizen(self, data: Dict[str, Any]) -> CitizenFUC:
        """Cria cidadão real na BD"""
        citizen_id = uuid4()
        
        citizen = CitizenFUC(
            citizen_id=citizen_id,
            full_name=data.get("full_name"),
            email=data.get("email"),
            birth_date=data.get("birth_date"),
            document_number=data.get("document_number"),
            province_id=data.get("province_id"),
            municipality_id=data.get("municipality_id"),
            commune_id=data.get("commune_id"),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        self.db.add(citizen)
        await self.db.commit()
        await self.db.refresh(citizen)
        
        # Evento real
        publish_event(
            "citizen.created",
            {
                "citizen_id": str(citizen_id),
                "email": data.get("email")
            }
        )
        
        return citizen
    
    async def get_citizen(self, citizen_id: UUID) -> Optional[CitizenFUC]:
        """Busca cidadão real"""
        result = await self.db.execute(
            select(CitizenFUC).filter(CitizenFUC.citizen_id == citizen_id)
        )
        return result.scalar_one_or_none()
    
    async def get_citizen_by_email(self, email: str) -> Optional[CitizenFUC]:
        """Busca por email"""
        result = await self.db.execute(
            select(CitizenFUC).filter(CitizenFUC.email == email)
        )
        return result.scalar_one_or_none()
    
    async def update_citizen(self, citizen_id: UUID, data: Dict[str, Any]) -> Optional[CitizenFUC]:
        """Atualiza dados reais"""
        citizen = await self.get_citizen(citizen_id)
        if not citizen:
            return None
        
        for key, value in data.items():
            if hasattr(citizen, key):
                setattr(citizen, key, value)
        
        citizen.updated_at = datetime.utcnow()
        await self.db.commit()
        await self.db.refresh(citizen)
        
        audit_log(
            action="CITIZEN_UPDATED",
            actor_id=str(citizen_id),
            actor_type="citizen",
            resource_id=str(citizen_id),
            resource_type="citizen",
            details={"updated_fields": list(data.keys())}
        )
        
        return citizen
