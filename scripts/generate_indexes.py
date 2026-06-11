#!/usr/bin/env python3
"""Generate docs/tree.md and docs/modules/tree.modules.txt for focused modules.

Usage:
  - Edit `MODULO_ATUAL_DIR` in the script, or pass the module path as first arg,
    or set environment variable `MODULO_ATUAL_DIR`.

This is intentionally surgical: it scans only the specified module path and
writes small, machine-friendly indexes that the assistant and scripts can use.
"""
import os
import sys
from datetime import datetime, timezone
import json

# ---------------------------------------------------------------------------
# CONFIG: default module (change or pass as arg / env var)
# ---------------------------------------------------------------------------
DEFAULT_MODULO = "apps/modules/citizen"
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DOCS_DIR = os.path.join(BASE_DIR, "docs")
MODULES_DOC_DIR = os.path.join(DOCS_DIR, "modules")


def garantir_diretorios():
    os.makedirs(DOCS_DIR, exist_ok=True)
    os.makedirs(MODULES_DOC_DIR, exist_ok=True)


def gerar_macro_tree():
    """Gera o docs/tree.md mapeando a raíz do monorepo em blocos limpos."""
    tree_path = os.path.join(DOCS_DIR, "tree.md")
    data_iso = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    pastas_criticas = ["apps", "scripts", "tests", "docs"]

    conteudo = "# SILA SYSTEM - MACRO INDEX\n\n"
    conteudo += "```yaml\n"

    for pasta in pastas_criticas:
        caminho_completo = os.path.join(BASE_DIR, pasta)
        if os.path.exists(caminho_completo):
            conteudo += f"- area: {pasta}\n"
            conteudo += f"  path: {pasta}/\n"
            if pasta == "apps":
                conteudo += f"  purpose: Core da aplicação, micro-serviços e routers de governança.\n"
                conteudo += f"  tags: [apps, monorepo, backend]\n"
            elif pasta == "tests":
                conteudo += f"  purpose: Suítes de testes de integração e cenários E2E governamentais.\n"
                conteudo += f"  tags: [tests, e2e, integration]\n"
            else:
                conteudo += f"  purpose: Componentes auxiliares de infraestrutura do sistema.\n"
                conteudo += f"  tags: [{pasta}, devops]\n"
            conteudo += f"  last_updated: {data_iso}\n\n"

    conteudo += "```\n"

    with open(tree_path, "w", encoding="utf-8") as f:
        f.write(conteudo)
    print(f"[✓] Macro índice gerado com sucesso em: {tree_path}")

    # Também exporta uma versão machine-readable em JSON
    macro_items = []
    for pasta in pastas_criticas:
        caminho_completo = os.path.join(BASE_DIR, pasta)
        if os.path.exists(caminho_completo):
            item = {"area": pasta, "path": f"{pasta}/", "last_updated": data_iso}
            if pasta == "apps":
                item["purpose"] = "Core da aplicação, micro-serviços e routers de governança."
                item["tags"] = ["apps", "monorepo", "backend"]
            elif pasta == "tests":
                item["purpose"] = "Suítes de testes de integração e cenários E2E governamentais."
                item["tags"] = ["tests", "e2e", "integration"]
            elif pasta == "docs":
                item["purpose"] = "Documentação técnica, esquemas OpenAPI e índices de navegação modular."
                item["tags"] = ["docs", "documentation"]
            elif pasta == "scripts":
                item["purpose"] = "Componentes auxiliares de infraestrutura e automações de build/teste."
                item["tags"] = ["scripts", "devops"]
            else:
                item["purpose"] = "Componentes auxiliares de infraestrutura do sistema."
                item["tags"] = [pasta, "devops"]
            macro_items.append(item)

    tree_json_path = os.path.join(DOCS_DIR, "tree.json")
    with open(tree_json_path, "w", encoding="utf-8") as jf:
        json.dump({"generated_at": data_iso, "items": macro_items}, jf, ensure_ascii=False, indent=2)
    print(f"[✓] Macro JSON gerado em: {tree_json_path}")


def gerar_micro_module_tree(modulo_rel_path: str):
    """Gera o docs/modules/tree.modules.txt focado estritamente no módulo de trabalho."""
    modules_txt_path = os.path.join(MODULES_DOC_DIR, "tree.modules.txt")
    caminho_modulo = os.path.join(BASE_DIR, modulo_rel_path)

    if not os.path.exists(caminho_modulo):
        print(f"[X] Erro: O diretório do módulo configurado não existe: {modulo_rel_path}")
        sys.exit(1)

    nome_modulo = os.path.basename(modulo_rel_path.rstrip("/"))

    # Busca cirúrgica de ficheiros chave do módulo
    routers = []
    tests = []
    workflows = []

    for root, _, files in os.walk(caminho_modulo):
        for file in files:
            rel_file_path = os.path.relpath(os.path.join(root, file), BASE_DIR)
            if "router" in file and file.endswith(".py"):
                routers.append(rel_file_path)
            elif "test" in file and file.endswith(".py"):
                tests.append(rel_file_path)
            elif ("workflow" in file or "process" in file) and file.endswith(".py"):
                workflows.append(rel_file_path)

    conteudo = "=" * 80 + "\n"
    conteudo += f"MODULE: {nome_modulo.upper()}\n"
    conteudo += f"ROOT: {modulo_rel_path}/\n"
    conteudo += f"PURPOSE: Módulo de execução e regras de negócio isoladas para {nome_modulo}.\n\n"

    conteudo += "ENTRYPOINTS (ROUTERS):\n"
    for r in routers[:5]:  # Limita para manter o índice microscópico e rápido
        conteudo += f"  - {r}\n"
    if not routers:
        conteudo += "  - Nenhum router localizado neste escopo.\n"

    conteudo += "\nCORE WORKFLOWS & PROCESSES:\n"
    for w in workflows[:5]:
        conteudo += f"  - {w}\n"
    if not workflows:
        conteudo += "  - Operando via repositórios CRUD base padrão.\n"

    conteudo += "\nTARGET TESTS:\n"
    for t in tests[:3]:
        conteudo += f"  - {t}\n"
    if not tests:
        conteudo += "  - Verifique a suíte global em tests/e2e/.\n"

    quick_run = f"PYTHONPATH=. python -m pytest {tests[0]}" if tests else "PYTHONPATH=. python -m pytest tests/"
    conteudo += f"\nQUICK_RUN: {quick_run}\n"
    conteudo += "=" * 80 + "\n"

    with open(modules_txt_path, "w", encoding="utf-8") as f:
        f.write(conteudo)
    print(f"[✓] Micro índice do módulo [{nome_modulo}] gerado em: {modules_txt_path}")

    # Também exporta uma versão JSON canónica do índice do módulo
    module_index = {
        "module": nome_modulo,
        "root": f"{modulo_rel_path}/",
        "purpose": f"Módulo de execução e regras de negócio isoladas para {nome_modulo}.",
        "entrypoints": routers[:50],
        "workflows": workflows[:50],
        "tests": tests[:20],
        "quick_run": quick_run,
        "last_updated": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
    }

    modules_json_path = os.path.join(MODULES_DOC_DIR, "tree.modules.json")
    with open(modules_json_path, "w", encoding="utf-8") as mj:
        json.dump(module_index, mj, ensure_ascii=False, indent=2)
    print(f"[✓] Micro JSON do módulo gerado em: {modules_json_path}")


def main():
    garantir_diretorios()

    # resolve module path: arg > env > default
    modulo = None
    if len(sys.argv) > 1:
        modulo = sys.argv[1]
    else:
        modulo = os.environ.get("MODULO_ATUAL_DIR", DEFAULT_MODULO)

    gerar_macro_tree()
    gerar_micro_module_tree(modulo)


if __name__ == "__main__":
    main()
