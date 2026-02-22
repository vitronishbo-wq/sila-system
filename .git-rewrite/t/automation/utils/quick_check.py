import sys

print("✅ Python version:", sys.version)

modules = [
    "os",
    "sys",
    "json",
    "logging",
    "requests",
    "fastapi",
    "sqlalchemy",
    "psycopg2",
    "pytest",
]

print("\n🔍 Testando importação de módulos:")
for mod in modules:
    try:
        __import__(mod)
        print(f"✅ {mod} importado com sucesso")
    except ImportError:
        print(f"❌ Falha ao importar: {mod}")
