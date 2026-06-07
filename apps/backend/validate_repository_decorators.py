#!/usr/bin/env python3
"""
Validador pós-LEGACY_ERADICATION - Identity Repositories

Confirma que:
1. core/iam foi removido
2. UserRepository do módulo identity está acessível
3. Métodos críticos existem
"""

import inspect
import sys
from pathlib import Path

# Adiciona o caminho do backend aos imports
sys.path.insert(0, "/home/dev03wsl/sila-system/apps/backend")

from apps.backend.app.modules.identity.infrastructure.repositories.user_repository import (
    UserRepository,
)


def check_method_exists(repo_class, method_name):
    """Verifica se um método existe na classe."""
    method = getattr(repo_class, method_name, None)
    if method is None:
        return False, "Method not found"
    return True, "Method found"


def validate_repositories():
    """Valida estado pós-remoção do core/iam."""

    print("=" * 80)
    print("VALIDAÇÃO PÓS-LEGACY_ERADICATION - Identity Repositories")
    print("=" * 80)
    print()

    core_iam_path = Path(__file__).resolve().parent / "app" / "core" / "iam"
    print("📌 Verificação de remoção do core/iam:")
    print("-" * 80)
    if core_iam_path.exists():
        print(f"❌ core/iam ainda existe: {core_iam_path}")
        iam_removed = False
    else:
        print("✅ core/iam removido")
        iam_removed = True
    print()

    print("📌 UserRepository Validations:")
    print("-" * 80)

    user_methods = {
        "create": "CREATE",
        "find_by_email": "FIND_BY_EMAIL",
        "find_by_citizen_id": "FIND_BY_CITIZEN_ID",
    }

    user_passed = 0
    user_total = len(user_methods)

    for method_name, _expected_action in user_methods.items():
        is_present, msg = check_method_exists(UserRepository, method_name)
        status = "✅ PASS" if is_present else "❌ FAIL"
        print(f"{status} | UserRepository.{method_name}()")
        print(f"       └─ {msg}")
        if is_present:
            user_passed += 1
        print()

    print("=" * 80)
    print("📊 RESUMO DE VALIDAÇÃO")
    print("=" * 80)
    print(f"core/iam removido:   {'✅' if iam_removed else '❌'}")
    print(f"UserRepository:      {user_passed}/{user_total} ✅")
    print(f"Total checks:        {user_passed + (1 if iam_removed else 0)}/{user_total + 1} ✅")
    print()

    print("=" * 80)
    print("🔍 ASSINATURAS DE MÉTODOS")
    print("=" * 80)
    print()

    print("UserRepository.create():")
    print(f"  Signature: {inspect.signature(UserRepository.create)}")
    print(f"  Source file: {inspect.getfile(UserRepository.create)}")
    print()

    print("=" * 80)
    print("✨ VALIDAÇÃO COMPLETA")
    print("=" * 80)

    total_checks = user_total + 1
    total_passed = user_passed + (1 if iam_removed else 0)

    if total_passed == total_checks:
        print(f"✅ SUCESSO: {total_passed}/{total_checks} validações passaram!")
        print()
        print("Repos de identity estão acessíveis e core/iam foi removido.")
        return 0

    print(f"⚠️  PARCIAL: {total_passed}/{total_checks} validações passaram.")
    print()
    print("Verifique a estrutura de identity e a remoção de core/iam.")
    return 1


if __name__ == "__main__":
    exit_code = validate_repositories()
    sys.exit(exit_code)
