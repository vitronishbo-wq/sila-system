"""
Script para testar permissões diretamente, sem depender do pytest.
Execute com: python3 run_permission_tests_directly.py
"""

import sys
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


# Simulação do FastAPI HTTPException
class HTTPException(Exception):
    def __init__(self, status_code: int, detail: dict):
        self.status_code = status_code
        self.detail = detail
        super().__init__(f"HTTP {status_code}: {detail}")


# Simulação do Pydantic BaseModel
class BaseModel:
    def dict(self):
        return {k: v for k, v in self.__dict__.items() if not k.startswith("_")}


# Modelo de usuário para testes
@dataclass
class UserStub(BaseModel):
    id: str
    email: str
    full_name: str
    is_active: bool = True
    is_superuser: bool = False
    permissions: List[str] | None = None
    level: Optional[str] = None
    region_id: Optional[str] = None
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()

    def __post_init__(self):
        if self.permissions is None:
            self.permissions = []


# Implementação das permissões
class CitizenshipPermissions:
    CITIZEN_CREATE = "citizenship:citizen:create"
    CITIZEN_READ = "citizenship:citizen:read"
    CITIZEN_UPDATE = "citizenship:citizen:update"
    CITIZEN_DELETE = "citizenship:citizen:delete"
    DOCUMENT_UPLOAD = "citizenship:document:upload"
    DOCUMENT_DOWNLOAD = "citizenship:document:download"

    @classmethod
    def all_permissions(cls):
        return [
            v
            for k, v in cls.__dict__.items()
            if not k.startswith("_") and isinstance(v, str)
        ]


# Função para testar permissões
async def has_permission(required_permission: str, current_user: UserStub) -> UserStub:
    if current_user.is_superuser:
        return current_user

    if not hasattr(current_user, "permissions") or not current_user.permissions:
        raise HTTPException(
            status_code=403, detail={"status": "error", "code": "permission_denied"}
        )

    if required_permission not in current_user.permissions:
        raise HTTPException(
            status_code=403, detail={"status": "error", "code": "permission_denied"}
        )

    return current_user


# Funções de teste
async def test_all_permissions():
    print("\nTestando listagem de todas as permissões...")
    perms = CitizenshipPermissions.all_permissions()
    assert isinstance(perms, list), "A lista de permissões deve ser uma lista"
    assert len(perms) > 0, "A lista de permissões não deve estar vazia"
    assert all(
        isinstance(p, str) for p in perms
    ), "Todas as permissões devem ser strings"
    assert all(
        p.startswith("citizenship:") for p in perms
    ), "Todas as permissões devem começar com 'citizenship:'"
    print("✅ Teste de listagem de permissões passou com sucesso!")
    return True


async def test_has_permission_success():
    print("\nTestando permissão concedida...")
    postgres = UserStub(
        id="1",
        email="test@example.com",
        full_name="Test User",
        permissions=["citizenship:citizen:read", "citizenship:document:download"],
    )

    result = await has_permission("citizenship:citizen:read", postgres)
    assert result == postgres, "O usuário com permissão deve ser retornado"
    print("✅ Teste de permissão concedida passou com sucesso!")
    return True


async def test_has_permission_denied():
    print("\nTestando permissão negada...")
    postgres = UserStub(
        id="1",
        email="test@example.com",
        full_name="Test User",
        permissions=["citizenship:citizen:read"],
    )

    try:
        await has_permission("citizenship:citizen:create", postgres)
        assert False, "Deveria ter lançado HTTPException"
    except HTTPException as e:
        assert e.status_code == 403, "Deveria retornar status 403"
        assert "permission_denied" in str(e.detail), "Deveria indicar permissão negada"
        print("✅ Teste de permissão negada passou com sucesso!")
        return True


async def test_superuser_has_all_permissions():
    print("\nTestando superusuário com todas as permissões...")
    postgres = UserStub(
        id="1",
        email="admin@example.com",
        full_name="Admin User",
        is_superuser=True,
        permissions=[],
    )

    result = await has_permission("any:permission", postgres)
    assert result == postgres, "Superusuário deve ter todas as permissões"
    print("✅ Teste de superusuário passou com sucesso!")
    return True


# Execução dos testes
async def run_tests():
    print("🚀 Iniciando testes de permissões...")
    tests = [
        test_all_permissions,
        test_has_permission_success,
        test_has_permission_denied,
        test_superuser_has_all_permissions,
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            success = await test()
            if success:
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ Erro ao executar teste: {e}")
            failed += 1

    print(f"\n📊 Resultado dos testes: {passed} aprovados, {failed} falhas")
    return failed == 0


if __name__ == "__main__":
    import asyncio

    success = asyncio.run(run_tests())
    sys.exit(0 if success else 1)
