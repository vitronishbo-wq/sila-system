#!/usr/bin/env python3
"""🧪 SILA Env Files Consistency Check

Verifica a presença e alinhamento mínimo entre:
- .env.example (raiz)
- .env.development (raiz)
- .env.production (raiz)
- apps/backend/config/.env.*

Não valida segredos, apenas a estrutura e chaves principais.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

EXPECTED_ROOT_ENV = {
    ".env.example",
}

EXPECTED_BACKEND_ENV = {
    ".env.development",
    ".env.production",
}

BACKEND_CONFIG_DIR = ROOT / "apps" / "backend" / "config"


def load_env_keys(path: Path) -> set[str]:
    keys: set[str] = set()
    if not path.exists():
        return keys
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key = line.split("=", 1)[0].strip()
        if key:
            keys.add(key)
    return keys


def main() -> None:
    problems: dict[str, str] = {}

    # Root env.example
    root_example = ROOT / ".env.example"
    load_env_keys(root_example)
    if not root_example.exists():
        problems[str(root_example)] = "Arquivo ausente."

    # Backend config envs
    backend_envs = {}
    for name in EXPECTED_BACKEND_ENV:
        p = BACKEND_CONFIG_DIR / name
        backend_envs[name] = load_env_keys(p)
        if not p.exists():
            problems[str(p)] = "Arquivo ausente."

    # Checagem grossa de chaves mínimas
    critical_keys = {"DATABASE_URL", "ASYNC_DATABASE_URL", "SECRET_KEY"}
    missing_critical = {
        env_name: sorted(list(critical_keys - keys)) for env_name, keys in backend_envs.items()
    }

    for env_name, missing in missing_critical.items():
        if missing:
            problems[f"apps/backend/config/{env_name}"] = "Chaves críticas ausentes: " + ", ".join(
                missing
            )

    if not problems:
        print("✅ Arquivos .env principais presentes e minimamente consistentes.")
        raise SystemExit(0)

    print("❌ Inconsistências de arquivos .env detectadas:")
    for path, msg in problems.items():
        print(f" - {path}: {msg}")

    print("\n💡 Utilize o sistema de geração automática de .env para corrigir estas pendências.")
    raise SystemExit(1)


if __name__ == "__main__":  # pragma: no cover
    main()
