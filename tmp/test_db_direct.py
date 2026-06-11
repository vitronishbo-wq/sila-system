"""Reproduce the 500 error by importing the service dependencies directly."""

import sys, os
sys.path.insert(0, '/home/dev03wsl/sila-system')
sys.path.insert(0, '/home/dev03wsl/sila-system/apps/backend')

os.environ['ENV_MODE'] = 'host'

from apps.backend.app.api.deps import get_db
from apps.backend.app.modules.society.assistencia_social.api.deps import get_beneficiario_service
from apps.backend.app.modules.society.assistencia_social.infrastructure.repositories import SQLAlchemyBeneficiarioRepository
from apps.backend.app.modules.society.assistencia_social.application.services.beneficiario_service import BeneficiarioService

import asyncio

async def test():
    try:
        async for session in get_db():
            try:
                repo = SQLAlchemyBeneficiarioRepository(session)
                result = await repo.list_all()
                print(f"list_all() OK: {len(result)} items")
            except Exception as e:
                print(f"ERROR in repo: {type(e).__name__}: {e}")
                import traceback
                traceback.print_exc()
    except Exception as e:
        print(f"ERROR in get_db: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()

asyncio.run(test())
