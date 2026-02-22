#!/usr/bin/env python3
import os
import re
import argparse

# ✅ Senha única universal
TARGET_PASSWORD = "Truman1*Marcelo1*"

# ✅ Todas as variações conhecidas e possíveis (regex abrangente)
PATTERNS = [
    r"Truman1[\*_]?Marcelo1[\*_0-9]*",
    r"Marcelo1[\*_]?Truman1[\*_0-9]*",
    r"Truman1*Marcelo1*",
    r"password\s*=\s*['\"]?[^'\"]+['\"]?",
]

# ❌ Pastas a ignorar
EXCLUDE_DIRS = {"venv", ".venv", ".git", "node_modules", "__pycache__", "dist", "build"}


def should_skip(path):
    return any(seg in EXCLUDE_DIRS for seg in path.split(os.sep))


def replace_in_file(path, apply, verbose):
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception:
        return

    updated = content
    for pattern in PATTERNS:
        updated = re.sub(pattern, TARGET_PASSWORD, updated)

    if updated != content:
        if verbose:
            print(f"→ updated: {path}")

        if apply:
            with open(path, "w", encoding="utf-8") as f:
                f.write(updated)


def walk_and_replace(apply, verbose):
    for root, dirs, files in os.walk("."):
        if should_skip(root):
            continue

        for file in files:
            # Inclui .env obrigatoriamente
            if (
                file.endswith(
                    (
                        ".py",
                        ".sh",
                        ".sql",
                        ".md",
                        ".txt",
                        ".yaml",
                        ".yml",
                        ".cfg",
                        ".ini",
                        ".json",
                        ".env",
                        ".env.local",
                        ".env.test",
                        ".env.dev",
                        ".env.example",
                    )
                )
                or "docker-compose" in file
            ):
                replace_in_file(os.path.join(root, file), apply, verbose)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Purga total e unificação de senhas.")
    parser.add_argument(
        "--apply", action="store_true", help="Aplica as mudanças nos arquivos"
    )
    parser.add_argument(
        "--verbose", action="store_true", help="Mostra cada modificação"
    )
    args = parser.parse_args()

    walk_and_replace(args.apply, args.verbose)

    print("\n✅ Purga concluída.")
    print(f"🔥 Senha universal aplicada: {TARGET_PASSWORD}\n")

    if not args.apply:
        print("⚠ Rodou apenas em modo de pré-visualização. Use --apply para gravar.")
