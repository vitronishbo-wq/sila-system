#!/usr/bin/env python3
import argparse
import datetime
import os
import re
import sys
from pathlib import Path
from urllib.parse import urlparse, urlunparse, quote_plus, unquote_plus

# Target unified password
TARGET_PASSWORD = "Truman1*Marcelo1*"
TARGET_PASSWORD_URLENC = quote_plus(TARGET_PASSWORD)

# Files and globs explicitly requested for normalization
FILE_SPECS = [
    # Compose files
    "docker-compose.yml",
    "docker-compose.test.yml",
    "docker-compose.dev.yml",
    "docker-compose.migration.yml",
    "devops/docker-compose.yml",
    # Backend envs
    "apps/backend/.env.test",
    "apps/backend/.env.development",
    # Scripts (moved to automation/)
    "automation/utils/preencher_env_critico.py",
    "automation/utils/preencher_env_critico_multi.py",
    "automation/utils/preencher_env_critico_multi_csv.py",
    "automation/setup/auto_create_admin.sh",
    "automation/utils/complete_env.sh",
    "automation/setup/start_live_stack.sh",
    "execute_auth_migration.sh",
]

# Known dev/test mismatched passwords we want to normalize FROM
LEGACY_PASSWORDS = [
    "Truman1*Marcelo1*",
    "Truman1*Marcelo1*",
    "postgres",
    "Truman1*Marcelo1*",
]
LEGACY_PASSWORDS_URLENC = list({quote_plus(p) for p in LEGACY_PASSWORDS})

# Regexes
# POSTGRES_PASSWORD=... (supports quoted or unquoted)
RE_POSTGRES_PASSWORD = re.compile(
    r"^(\s*POSTGRES_PASSWORD\s*[:=]\s*)([\"']?)([^\"'\n]+)\2(.*)$"
)
# docker-compose YAML environment key value like: KEY: value
RE_YAML_ENV = re.compile(r"^(\s*[A-Z0-9_]+\s*:\s*)(.+)$")

# DATABASE_URL detection and replacement in-line
RE_DBURL_LINE = re.compile(
    r"^(.*?(?:DATABASE_URL|ASYNC_DATABASE_URL)\s*[:=]\s*)([\"']?)([^\"'\n]+)\2(.*)$"
)

# Generic postgres URL pattern for substitution (postgres:// or postgresql://)
RE_PG_URL = re.compile(
    r"^(postgres(?:ql)?(?:\+asyncpg)?://)([^:@/]+)(?::([^@/]*))?@(.+)$", re.IGNORECASE
)


def _replace_postgres_password_line(line: str) -> tuple[str, bool]:
    m = RE_POSTGRES_PASSWORD.match(line)
    if not m:
        return line, False
    prefix, quote, _old, suffix = m.groups()
    new_val = f"{quote}{TARGET_PASSWORD}{quote}"
    return f"{prefix}{new_val}{suffix}\n", True


def _normalize_pg_url(url: str) -> str:
    m = RE_PG_URL.match(url)
    if not m:
        return url
    scheme, user, pwd, rest = m.groups()
    # Some usernames may be quoted or URL-encoded in the source; preserve as-is
    # Replace password with target (URL-encoded when embedded in URL)
    new_pwd = TARGET_PASSWORD_URLENC
    # If password component existed or not, ensure ":pwd@" appears once
    user_part = user
    return f"{scheme}{user_part}:{new_pwd}@{rest}"


def _replace_dburl_line(line: str) -> tuple[str, bool]:
    m = RE_DBURL_LINE.match(line)
    if not m:
        return line, False
    prefix, quote, url, suffix = m.groups()
    new_url = _normalize_pg_url(url)
    if new_url == url:
        # Also try replacing legacy URL-encoded passwords directly
        replaced = url
        for lp in LEGACY_PASSWORDS_URLENC:
            if lp in replaced:
                replaced = replaced.replace(lp, TARGET_PASSWORD_URLENC)
        if replaced != url:
            new_url = replaced
    if new_url == url:
        return line, False
    q = quote or ""
    return f"{prefix}{q}{new_url}{q}{suffix}\n", True


def _replace_yaml_env_value(line: str) -> tuple[str, bool]:
    # Specifically handle YAML environment entries with POSTGRES_PASSWORD or DB URLs
    if "POSTGRES_PASSWORD" in line:
        return _replace_postgres_password_line(line)
    if "DATABASE_URL" in line or "ASYNC_DATABASE_URL" in line:
        return _replace_dburl_line(line)
    return line, False


def process_file(
    path: Path, dry_run: bool = True, verbose: bool = False
) -> tuple[int, int]:
    if not path.exists() or not path.is_file():
        if verbose:
            print(f"- skip missing: {path}")
        return 0, 0

    changed_lines = 0
    total_lines = 0
    new_lines: list[str] = []

    try:
        content = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        content = path.read_text(encoding="latin-1")

    lines = content.splitlines(keepends=False)

    for raw in lines:
        line = raw
        modified = False

        # Try specific handlers first
        if (
            "POSTGRES_PASSWORD" in line
            or "DATABASE_URL" in line
            or "ASYNC_DATABASE_URL" in line
        ):
            if path.suffix in {".yml", ".yaml"} or "/docker-compose" in str(
                path
            ).replace("\\", "/"):
                line2, did = _replace_yaml_env_value(line)
            else:
                # For .env-like or script lines, attempt replacements generically
                line2, did = _replace_postgres_password_line(line)
                if not did:
                    line2, did = _replace_dburl_line(line)
            if did:
                modified = True
                line = line2.rstrip("\n")

        # Fallback: if line still contains legacy passwords plainly, replace them
        if not modified:
            plain_before = line
            for legacy in LEGACY_PASSWORDS:
                if legacy in line:
                    line = line.replace(legacy, TARGET_PASSWORD)
            # URL-encoded legacy passwords as well
            for legacy_enc in LEGACY_PASSWORDS_URLENC:
                if legacy_enc in line:
                    line = line.replace(legacy_enc, TARGET_PASSWORD_URLENC)
            if line != plain_before:
                modified = True

        new_lines.append(line)
        total_lines += 1
        if modified:
            changed_lines += 1

    if changed_lines and not dry_run:
        # Backup
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = path.with_suffix(path.suffix + f".bak.{ts}")
        path.write_text(
            "\n".join(lines) + "\n", encoding="utf-8"
        )  # write original to backup file? keep as copy
        backup_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        # Write new content
        path.write_text("\n".join(new_lines) + "\n", encoding="utf-8")

    if verbose:
        status = "changed" if changed_lines else "ok"
        print(f"{status:7} {changed_lines:4} lines  {path}")

    return changed_lines, total_lines


def expand_targets(root: Path) -> list[Path]:
    targets: list[Path] = []
    for spec in FILE_SPECS:
        if "*" in spec or "?" in spec:
            # glob
            targets.extend(root.glob(spec))
        else:
            p = root / spec
            if p.exists():
                targets.append(p)
    # Add any scripts matching the wildcard explicitly
    targets.extend((root / "scripts").glob("preencher_env_critico*.py"))
    # Deduplicate while preserving order
    seen = set()
    unique: list[Path] = []
    for p in targets:
        rp = p.resolve()
        if rp not in seen:
            seen.add(rp)
            unique.append(p)
    return unique


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Uniformize dev/test passwords to a single target value."
    )
    ap.add_argument(
        "--apply", action="store_true", help="Apply changes in-place (default: dry-run)"
    )
    ap.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    ap.add_argument(
        "--root", default=".", help="Project root (default: current directory)"
    )
    args = ap.parse_args()

    root = Path(args.root).resolve()
    targets = expand_targets(root)

    if not targets:
        print("No target files found.")
        return 1

    total_changed = 0
    total_files = 0
    mode = "APPLY" if args.apply else "DRY-RUN"
    print(f"Mode: {mode}  Target password: {TARGET_PASSWORD}")

    for path in targets:
        changed, _ = process_file(path, dry_run=not args.apply, verbose=args.verbose)
        total_files += 1
        total_changed += 1 if changed else 0

    print(f"Summary: processed={total_files} files, modified={total_changed} files")
    if not args.apply:
        print(
            "Nothing written. Re-run with --apply to write changes (backups created)."
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
