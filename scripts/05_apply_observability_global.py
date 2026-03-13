#!/usr/bin/env python3
"""Aplicar observabilidade global em todos os routers"""

import re
from pathlib import Path

BASE = Path("/home/dev03wsl/sila-system/apps/backend")
MODULES = BASE / "app" / "modules"

print("🔥 APLICANDO OBSERVABILIDADE GLOBAL")
print("====================================\n")

router_files = list(MODULES.rglob("api/router.py"))
print(f"📊 Total de routers encontrados: {len(router_files)}\n")

processed = 0
for router_file in sorted(router_files):
    content = router_file.read_text()
    original_content = content
    
    # Adicionar import se necessário
    if "from app.core.observability" not in content:
        # Encontrar última linha de import
        lines = content.split('\n')
        import_end = 0
        
        for i, line in enumerate(lines):
            if line.startswith(('from ', 'import ')) or line.strip() == '':
                import_end = i + 1
            elif line.strip() and not line.startswith(('from ', 'import ', '#')):
                break
        
        # Inserir novo import
        lines.insert(import_end, 'from app.core.observability import observability_middleware')
        content = '\n'.join(lines)
    
    # Adicionar middleware ao router se não existir
    if "router.middleware" not in content and "@router.middleware" not in content:
        # Procurar onde adicionar (depois da criação do router)
        if "router = APIRouter(" in content:
            # Adicionar após a linha de criação
            content = re.sub(
                r'(router = APIRouter\([^)]*\))',
                r'\1\n\nrouter.middleware("http")(observability_middleware)',
                content
            )
        else:
            # Fallback: adicionar no final
            content = content.rstrip() + '\n\nrouter.middleware("http")(observability_middleware)\n'
    
    if content != original_content:
        router_file.write_text(content)
        rel_path = router_file.relative_to(BASE)
        print(f"   ✅ {rel_path}")
        processed += 1
    else:
        rel_path = router_file.relative_to(BASE)
        print(f"   ⏭️  {rel_path} (already has observability)")

print(f"\n📊 Routers atualizados: {processed}/{len(router_files)}")

# Agora aplicar @trace() em service methods
print("\n\n🔥 APLICANDO @trace() EM SERVICE METHODS")
print("==========================================\n")

service_files = list(MODULES.rglob("application/services/*.py"))
# Filtrar __init__.py
service_files = [f for f in service_files if f.name != "__init__.py"]

print(f"📊 Total de services encontrados: {len(service_files)}\n")

trace_count = 0
for service_file in sorted(service_files):
    content = service_file.read_text()
    original_content = content
    
    # Adicionar import se necessário
    if "@trace" in content and "from app.core.observability" not in content:
        lines = content.split('\n')
        import_end = 0
        
        for i, line in enumerate(lines):
            if line.startswith(('from ', 'import ')) or line.strip() == '':
                import_end = i + 1
            elif line.strip() and not line.startswith(('from ', 'import ', '#')):
                break
        
        # Inserir novo import
        lines.insert(import_end, 'from app.core.observability import trace')
        content = '\n'.join(lines)
    
    # Adicionar @trace() a métodos async que não o têm
    lines = content.split('\n')
    modified = False
    
    for i, line in enumerate(lines):
        # Procurar por "async def" ou "def" que não tenha decorator
        if (line.strip().startswith(('async def', 'def')) and 
            not line.strip().startswith(('async def __', 'def __')) and  # Skip dunder methods
            (i == 0 or not lines[i-1].strip().startswith('@')) and
            'async def' in line):  # Apenas métodos async
            
            indent = len(line) - len(line.lstrip())
            lines.insert(i, ' ' * indent + '@trace()')
            modified = True
            trace_count += 1
    
    if modified:
        content = '\n'.join(lines)
        service_file.write_text(content)
        rel_path = service_file.relative_to(BASE)
        print(f"   ✅ {rel_path}")

print(f"\n📊 Métodos com @trace(): {trace_count}")

print("\n✅ OBSERVABILIDADE GLOBAL APLICADA")
