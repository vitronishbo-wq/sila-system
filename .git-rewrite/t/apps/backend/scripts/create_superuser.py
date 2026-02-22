#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from config.settings import settings
from modules.auth.models.user import User, AdministrativeLevel
from passlib.context import CryptContext
from uuid import uuid4

# 🔹 Configurar engine e sessão
DATABASE_URL = settings.ASYNC_DATABASE_URL
engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# 🔹 Configurar hash de senha
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 🔹 Dados do superusuário
SUPERUSER_EMAIL = "admin@sila.gov.ao"
SUPERUSER_PASSWORD = "Truman1*"
FULL_NAME = "Administrador SILA"
LEVEL = AdministrativeLevel.CENTRAL

async def create_superuser():
    async with AsyncSessionLocal() as session:
        # Verificar se o usuário já existe
        result = await session.execute(
            User.__table__.select().where(User.email == SUPERUSER_EMAIL)
        )
        existing_user = result.scalar_one_or_none()
        if existing_user:
            print(f"Usuário {SUPERUSER_EMAIL} já existe. Nada a fazer.")
            return

        # Criar novo usuário
        new_user = User(
            id=uuid4(),
            email=SUPERUSER_EMAIL,
            hashed_password=pwd_context.hash(SUPERUSER_PASSWORD),
            full_name=FULL_NAME,
            is_active=True,
            is_superuser=True,
            is_verified=True,
            level=LEVEL,
        )
        session.add(new_user)
        await session.commit()
        print(f"✅ Superusuário {SUPERUSER_EMAIL} criado com sucesso.")

if __name__ == "__main__":
    asyncio.run(create_superuser())
