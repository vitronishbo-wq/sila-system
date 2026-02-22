import logging
from typing import Optional, List, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from modules.identity.models.user import User, AdministrativeLevel
from modules.identity.schemas.user import UserCreate
from core.security import verify_password, get_password_hash
from core.scope import DataScope

logger = logging.getLogger(__name__)


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_user_scoped(self, payload: UserCreate, scope: DataScope) -> User:
        """
        Cria um usuário respeitando a hierarquia administrativa e o escopo territorial.
        """
        # Se não for superuser, aplicamos as travas de governança (DPA)
        if not scope.is_admin:
            # 1. Validação Territorial: O novo usuário deve estar dentro da jurisdição do criador
            if payload.region_id not in scope.allowed_ids:
                logger.warning(f"Tentativa de violação de escopo territorial por {scope.user_id}")
                raise ValueError("Região fora do escopo permitido para sua jurisdição.")

            # 2. Validação de Hierarquia: Um usuário só cria subordinados (níveis inferiores)
            hierarchy = {
                AdministrativeLevel.CENTRAL: 1,
                AdministrativeLevel.PROVINCIAL: 2,
                AdministrativeLevel.MUNICIPAL: 3,
                AdministrativeLevel.COMMUNAL: 4,
                AdministrativeLevel.LOCAL: 5
            }

            creator_rank = hierarchy.get(scope.level, 5)
            target_rank = hierarchy.get(payload.level, 5)

            if target_rank <= creator_rank:
                raise ValueError("Permissão negada: Nível administrativo deve ser inferior ao seu.")

        hashed_pwd = get_password_hash(payload.password)

        new_user = User(
            email=payload.email.lower().strip(),
            full_name=payload.full_name,
            hashed_password=hashed_pwd,
            is_active=True,
            is_superuser=False,
            level=payload.level,
            region_id=payload.region_id,
        )

        try:
            self.db.add(new_user)
            await self.db.commit()
            await self.db.refresh(new_user)
            return new_user
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Erro na persistência do usuário: {str(e)}")
            raise

    async def get_user_by_email(self, email: str) -> Optional[User]:
        normalized = email.lower().strip()
        result = await self.db.execute(
            select(User).where(func.lower(User.email) == normalized)
        )
        return result.scalar_one_or_none()

    async def authenticate(self, email: str, password: str) -> Optional[User]:
        user = await self.get_user_by_email(email)
        if not user or not user.is_active:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    async def get_all_scoped(self, scope: DataScope) -> List[User]:
        """
        Retorna usuários filtrados automaticamente pelo DataScope (cerca sanitária).
        """
        query = select(User).order_by(User.created_at.desc())

        # Aplica a query recursiva de territórios do DataScope
        query = scope.apply_filter(query, User.region_id)

        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_by_id(self, user_id: int) -> Optional[User]:
        result = await self.db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def update(self, user: User, update_data: dict) -> User:
        for field, value in update_data.items():
            setattr(user, field, value)
        
        try:
            self.db.add(user)
            await self.db.commit()
            await self.db.refresh(user)
            return user
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Erro ao atualizar usuário: {str(e)}")
            raise

    async def delete(self, user: User) -> None:
        try:
            await self.db.delete(user)
            await self.db.commit()
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Erro ao excluir usuário: {str(e)}")
            raise
