import os
import sys
import subprocess
import pkg_resources

BASE_PATH = os.path.join("backend", "requirements", "base.txt")
TEST_PATH = os.path.join("backend", "requirements_test.txt")

def check_file_exists(path):
    if not os.path.isfile(path):
        print(f"[❌] Arquivo ausente: {path}")
        return False
    print(f"[✅] Arquivo encontrado: {path}")
    return True

def parse_requirements(path):
    with open(path, "r") as f:
        lines = f.readlines()
    return [
        line.strip().split("==")[0].split(">=")[0]
        for line in lines
        if line.strip() and not line.startswith("#") and not line.startswith("-r")
    ]

def check_installed(packages):
    missing = []
    for pkg in packages:
        try:
            pkg_resources.get_distribution(pkg)
            print(f"[✅] {pkg} instalado")
        except pkg_resources.DistributionNotFound:
            print(f"[❌] {pkg} não encontrado")
            missing.append(pkg)
    return missing

def check_virtual_env():
    if sys.prefix == sys.base_prefix:
        print("[⚠️] Ambiente virtual NÃO está ativo")
        return False
    print("[✅] Ambiente virtual ativo")
    return True

def main()
    print("🔍 Validação do ambiente de dependências\n")

    files_ok = check_file_exists(BASE_PATH) and check_file_exists(TEST_PATH)
    venv_ok = check_virtual_env()

    if not files_ok or not venv_ok:
        print("\n[🛑] Ambiente inválido. Corrija os erros acima.")
        return

    base_packages = parse_requirements(BASE_PATH)
    test_packages = parse_requirements(TEST_PATH)

    print("\n📦 Verificando pacotes base...")
    missing_base = check_installed(base_packages)

    print("\n🧪 Verificando pacotes de teste...")
    missing_test = check_installed(test_packages)

    if not missing_base and not missing_test:
        print("\n✅ Ambiente está coerente e completo.")
    else:
        print("\n⚠️ Pacotes ausentes detectados:")
        for pkg in missing_base + missing_test:
            print(f"  - {pkg}")
        print("\nSugestão: execute `pip install -r backend/requirements_test.txt`")

if __name__ == "__main__":
    main()
