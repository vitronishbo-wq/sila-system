import asyncio
import importlib
import os
import sys

# Garante que o app está no path
sys.path.append(os.getcwd())

SEEDS = [
    "seeds.scripts.seed_base_users",
    "seeds.scripts.seed_reference_data",
    # Adicione novos paths aqui na ordem de dependência
]


async def run_seeds():
    print("🚀 Iniciando semeadura do banco de dados...")
    for seed_path in SEEDS:
        try:
            module = importlib.import_module(seed_path)
            if hasattr(module, "run"):
                print(f"  → Executando: {seed_path}")
                await module.run()
            else:
                print(f"  ⚠️ Ignorado: {seed_path} não possui função run()")
        except Exception as e:
            print(f"  ❌ Erro em {seed_path}: {e}")


if __name__ == "__main__":
    asyncio.run(run_seeds())
