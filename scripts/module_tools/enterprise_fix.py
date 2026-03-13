#!/usr/bin/env python3
import os
import sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

MODULES_ROOT = Path("apps/backend/app/modules")
LAYERS = ["api", "application", "domain", "infrastructure", "tests"]
SKIP = {"api", "audit", "__init__.py", "conftest.py"}

def fix_module(module_path):
    """Normaliza um módulo para simetria DDD."""
    results = []
    
    try:
        # 1. Criar camadas faltantes
        for layer in LAYERS:
            layer_path = module_path / layer
            layer_path.mkdir(parents=True, exist_ok=True)
            init_file = layer_path / "__init__.py"
            if not init_file.exists():
                init_file.touch()
        
        # 2. Injetar exceptions.py se não existir
        exc_path = module_path / "domain" / "exceptions.py"
        if not exc_path.exists():
            module_name = module_path.name.title().replace("_", "")
            exc_path.write_text(
                f"class {module_name}Exception(Exception):\n    pass\n"
            )
            results.append(f"  ✓ {module_path.name}: exceptions.py criado")
        
        # 3. Injetar health.py se não existir
        health_path = module_path / "api" / "health.py"
        if not health_path.exists():
            health_path.write_text(
                "from fastapi import APIRouter\nrouter = APIRouter()\n\n"
                "@router.get('/health')\ndef health():\n    return {'status': 'ok'}\n"
            )
            results.append(f"  ✓ {module_path.name}: health.py criado")
        
        # 4. Mover core -> domain (se existir)
        core_path = module_path / "core"
        domain_path = module_path / "domain"
        if core_path.exists():
            os.system(f"cp -rn {core_path}/* {domain_path}/ 2>/dev/null")
            os.system(f"rm -rf {core_path}")
            results.append(f"  ✓ {module_path.name}: core/ consolidado em domain/")
        
        return module_path.name, results
    
    except Exception as e:
        return module_path.name, [f"  ✗ {module_path.name}: {str(e)}"]

def main():
    if not MODULES_ROOT.exists():
        print("❌ Erro: pasta não encontrada")
        sys.exit(1)
    
    # Listar módulos
    modules = [m for m in MODULES_ROOT.iterdir() 
               if m.is_dir() and m.name not in SKIP]
    
    print(f"🔧 Padronizando {len(modules)} módulos...\n")
    
    # Executar em paralelo
    all_results = {}
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = {executor.submit(fix_module, m): m.name for m in modules}
        for future in as_completed(futures):
            name, results = future.result()
            all_results[name] = results
    
    # Saída
    for name in sorted(all_results.keys()):
        for result in all_results[name]:
            print(result)
    
    print(f"\n✅ Padronização concluída: {len(modules)} módulos")

if __name__ == "__main__":
    main()
