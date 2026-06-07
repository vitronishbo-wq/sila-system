"""
🛠️ Utilidades de Território

Funções compartilhadas para criar/recuperar territórios.
"""

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.core.territory.models.territory import Territory


async def get_or_create_territory(
    session: AsyncSession, name: str, type: str, parent_id: uuid.UUID = None
) -> Territory:
    """
    Recupera um território existente ou o cria se não existir.

    Args:
        session: Sessão async do SQLAlchemy
        name: Nome do território (ex: "Angola", "Huambo")
        type: Tipo (ex: "country", "province", "municipality", "commune")
        parent_id: ID do território pai (para hierarquia)

    Returns:
        Territory: Objeto do território criado ou recuperado

    Exemplo:
        >>> angola = await get_or_create_territory(session, "Angola", "country")
        >>> huambo = await get_or_create_territory(session, "Huambo", "province", angola.id)
    """
    res = await session.execute(
        select(Territory).where(Territory.name == name, Territory.type == type).limit(1)
    )
    territory = res.scalar_one_or_none()
    if not territory:
        territory = Territory(id=uuid.uuid4(), name=name, type=type, parent_id=parent_id)
        session.add(territory)
        await session.flush()
        print(f"📍 Criado: {name} ({type})")
    else:
        print(f"ℹ️  Existe: {name} ({type})")
    return territory


__all__ = ["get_or_create_territory"]
