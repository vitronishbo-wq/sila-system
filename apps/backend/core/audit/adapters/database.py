"""PostgreSQL database adapter for audit system"""
import os
from typing import List, Optional
from datetime import datetime
from sqlalchemy import create_engine, Column, String, Integer, DateTime, Text, Enum as SQLEnum, select
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import select
import asyncio

from ..audit_engine import AuditRecord, AuditAction, AuditStatus, AuditAdapter

Base = declarative_base()


class AuditLogModel(Base):
    """SQLAlchemy model for audit_logs table"""
    __tablename__ = 'audit_logs'
    
    audit_id = Column(UUID(as_uuid=True), primary_key=True)
    timestamp = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    user_id = Column(String(255), nullable=True)
    module = Column(String(100), nullable=True)
    action = Column(SQLEnum(AuditAction), nullable=False)
    status = Column(SQLEnum(AuditStatus), nullable=False)
    request_path = Column(String(500), nullable=True)
    result_code = Column(Integer, nullable=True)
    result_message = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)


class DatabaseAuditAdapter(AuditAdapter):
    """PostgreSQL-based audit storage adapter"""
    
    def __init__(self, db_url: Optional[str] = None):
        """Initialize database adapter with async engine"""
        if db_url is None:
            # Build from environment variables
            user = os.getenv('POSTGRES_USER', 'sila_user')
            password = os.getenv('POSTGRES_PASSWORD', 'Trumanmarcelo_1983')
            host = os.getenv('POSTGRES_HOST', 'db')
            port = os.getenv('POSTGRES_PORT', '5432')
            database = os.getenv('POSTGRES_DB', 'sila_db')
            db_url = f'postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}'
        
        self.engine = create_async_engine(
            db_url,
            echo=False,
            pool_pre_ping=True,
            pool_size=5,
            max_overflow=10
        )
        self.SessionLocal = sessionmaker(self.engine, class_=AsyncSession, expire_on_commit=False)
    
    async def store(self, record: AuditRecord) -> bool:
        """Store audit record in PostgreSQL"""
        try:
            async with self.SessionLocal() as session:
                model = AuditLogModel(
                    audit_id=record.audit_id,
                    timestamp=record.timestamp,
                    user_id=record.user_id or None,
                    module=record.module or None,
                    action=record.action,
                    status=record.status,
                    request_path=record.request_path or None,
                    result_code=record.result_code,
                    result_message=record.result_message or None
                )
                session.add(model)
                await session.commit()
                return True
        except Exception as e:
            print(f"Error storing audit record: {e}")
            return False
    
    async def retrieve(self, audit_id: str) -> Optional[AuditRecord]:
        """Retrieve single audit record by ID"""
        try:
            async with self.SessionLocal() as session:
                stmt = select(AuditLogModel).where(AuditLogModel.audit_id == audit_id)
                result = await session.execute(stmt)
                model = result.scalars().first()
                
                if not model:
                    return None
                
                return AuditRecord(
                    audit_id=str(model.audit_id),
                    timestamp=model.timestamp,
                    user_id=model.user_id,
                    module=model.module,
                    action=model.action,
                    status=model.status,
                    request_path=model.request_path,
                    result_code=model.result_code,
                    result_message=model.result_message
                )
        except Exception as e:
            print(f"Error retrieving audit record: {e}")
            return None
    
    async def query(self, **filters) -> List[AuditRecord]:
        """Query audit records with filters"""
        try:
            async with self.SessionLocal() as session:
                stmt = select(AuditLogModel)
                
                # Apply filters
                if 'user_id' in filters:
                    stmt = stmt.where(AuditLogModel.user_id == filters['user_id'])
                if 'module' in filters:
                    stmt = stmt.where(AuditLogModel.module == filters['module'])
                if 'action' in filters:
                    stmt = stmt.where(AuditLogModel.action == filters['action'])
                if 'status' in filters:
                    stmt = stmt.where(AuditLogModel.status == filters['status'])
                if 'limit' in filters:
                    stmt = stmt.limit(filters['limit']).order_by(AuditLogModel.timestamp.desc())
                
                result = await session.execute(stmt)
                models = result.scalars().all()
                
                records = []
                for model in models:
                    records.append(AuditRecord(
                        audit_id=str(model.audit_id),
                        timestamp=model.timestamp,
                        user_id=model.user_id,
                        module=model.module,
                        action=model.action,
                        status=model.status,
                        request_path=model.request_path,
                        result_code=model.result_code,
                        result_message=model.result_message
                    ))
                return records
        except Exception as e:
            print(f"Error querying audit records: {e}")
            return []
    
    async def close(self):
        """Close database connection"""
        await self.engine.dispose()
