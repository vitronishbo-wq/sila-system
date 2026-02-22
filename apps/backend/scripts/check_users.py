import asyncio
import sys
from pathlib import Path

# Add backend dir to sys.path
sys.path.insert(0, "/app")

from sqlalchemy import select
from core.db.session import async_session_factory
from modules.identity.models.user import User

async def check_users():
    async with async_session_factory() as session:
        from sqlalchemy import func
        result = await session.execute(
            select(User.level, func.count(User.id))
            .where(User.email.like("truman%@sila.gov.ao"))
            .group_by(User.level)
        )
        counts = result.all()
        
        print("\n=== CONTAGEM DE USUÁRIOS TRUMAN ===")
        total = 0
        for level, count in counts:
            print(f"- Nível {level}: {count} usuários")
            total += count
        print(f"Total: {total} usuários")
        
        # Check specific trumanx pattern if requested
        res_specific = await session.execute(select(User).where(User.email == "truman@sila.gov.ao"))
        if res_specific.scalar_one_or_none():
            print("- Usuário 'truman@sila.gov.ao': Encontrado")
        else:
            print("- Usuário 'truman@sila.gov.ao': Não encontrado")

if __name__ == "__main__":
    asyncio.run(check_users())
