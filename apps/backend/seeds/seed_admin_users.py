import uuid
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.settings import settings
from app.core.security import get_password_hash
from app.core.constants import UserRole, AdminLevel
from apps.backend.app.modules.identity.models.user import User
from datetime import datetime

ADMIN_USERS = [
    {
        "email": "central@sila.gov.ao",
        "role": UserRole.ADMIN.value,
        "level": AdminLevel.SUPERUSER.value,
        "username": "central.admin"
    },
    {
        "email": "prov.huambo@sila.gov.ao",
        "role": UserRole.MANAGER.value,
        "level": AdminLevel.PROVINCIAL.value,
        "username": "prov.huambo"
    },
    {
        "email": "mun.huambo@sila.gov.ao",
        "role": UserRole.MANAGER.value,
        "level": AdminLevel.MUNICIPAL.value,
        "username": "mun.huambo"
    },
    {
        "email": "comun.huambo@sila.gov.ao",
        "role": UserRole.OFFICER.value,
        "level": AdminLevel.COMUNAL.value,
        "username": "comun.huambo"
    },
]

PASSWORD = "Sila_1983"


def seed_admin_users():
    sync_database_url = settings.DATABASE_URL.replace("+asyncpg", "")
    engine = create_engine(sync_database_url, echo=False)
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    try:
        for user_data in ADMIN_USERS:
            user = db.query(User).filter_by(email=user_data["email"]).first()
            if not user:
                user = User(
                    id=uuid.uuid4(),
                    email=user_data["email"],
                    username=user_data["username"],
                    password_hash=get_password_hash(PASSWORD),
                    role=user_data["role"],
                    level=user_data["level"],
                    is_active=True,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow(),
                )
                db.add(user)
        db.commit()
        print("✅ Usuários administrativos criados com sucesso!")
    except Exception as e:
        db.rollback()
        print(f"❌ Erro ao criar usuários administrativos: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_admin_users()
