"""
🔥 Teste Global de Importação de Módulos
----------------------------------------------------------
Varre todo o diretório backend/app e tenta importar cada módulo Python.

Objetivos:
✅ Detectar todos os erros de importação de forma global.
✅ Mostrar resultados coloridos e resumidos no terminal.
✅ Funcionar mesmo com submódulos profundos.
----------------------------------------------------------
"""

import importlib
import os
import pkgutil
import sys
import time
import traceback

# ✅ Configuração de caminho para permitir importações de backend/app
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../backend"))
APP_DIR = os.path.join(BASE_DIR, "app")
sys.path.insert(0, BASE_DIR)


# 🎨 Cores para saída visual no terminal
class Color:
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    CYAN = "\033[96m"
    RESET = "\033[0m"
    BOLD = "\033[1m"
    GRAY = "\033[90m"


def test_import_all_modules():
    base_package = "app"
    base_path = [APP_DIR]

    print(f"\n{Color.CYAN}{Color.BOLD}🔍 Iniciando varredura global de módulos...{Color.RESET}")
    print(f"{Color.GRAY}Diretório alvo: {APP_DIR}{Color.RESET}\n")

    start_time = time.time()
    total = imported = 0
    errors = []

    for module_info in pkgutil.walk_packages(path=base_path, prefix=f"{base_package}."):
        name = module_info.name
        total += 1
        try:
            importlib.import_module(name)
            imported += 1
        except Exception as e:
            tb = traceback.format_exc(limit=6)
            errors.append((name, str(e), tb))

    duration = time.time() - start_time
    print(f"\n{Color.BOLD}📦 Total de módulos encontrados:{Color.RESET} {total}")
    print(f"{Color.GREEN}✅ Importados com sucesso:{Color.RESET} {imported}")
    print(f"{Color.YELLOW}⏱️ Tempo total:{Color.RESET} {duration:.2f}s\n")

    if errors:
        print(f"{Color.RED}{Color.BOLD}❌ {len(errors)} módulos falharam ao importar:{Color.RESET}")
        for i, (name, err, tb) in enumerate(errors, start=1):
            print(f"\n{Color.YELLOW}#{i} Falha ao importar: {Color.BOLD}{name}{Color.RESET}")
            print(f"{Color.RED}{err}{Color.RESET}")
            traceback_lines = tb.strip().split("\n")[-5:]
            print(f"{Color.GRAY}{''.join(traceback_lines)}{Color.RESET}")
            print("-" * 100)
        raise AssertionError(f"{len(errors)} módulos falharam ao importar.")
    else:
        print(
            f"{Color.GREEN}{Color.BOLD}✅ Todos os {total} módulos foram importados com sucesso! 🎉{Color.RESET}"
        )
