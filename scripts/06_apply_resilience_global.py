#!/usr/bin/env python3
"""Aplicar resiliência global em todos os clients de integração"""

import re
from pathlib import Path

BASE = Path("/home/dev03wsl/sila-system/apps/backend")
MODULES = BASE / "app" / "modules"

print("🔥 APLICANDO RESILIÊNCIA GLOBAL")
print("================================\n")

# Encontrar todos os clients de integração
integration_files = list(MODULES.rglob("integrations/*.py"))
integration_files = [f for f in integration_files if f.name != "__init__.py"]

print(f"📊 Total de clients de integração encontrados: {len(integration_files)}\n")

processed = 0
for client_file in sorted(integration_files):
    content = client_file.read_text()
    original_content = content
    
    # Verificar se usa httpx diretamente
    if "httpx" in content and "ResilientClient" not in content:
        
        # Adicionar import
        if "from app.core.resilience import ResilientClient" not in content:
            lines = content.split('\n')
            import_end = 0
            
            for i, line in enumerate(lines):
                if line.startswith(('from ', 'import ')) or line.strip() == '':
                    import_end = i + 1
                elif line.strip() and not line.startswith(('from ', 'import ', '#')):
                    break
            
            lines.insert(import_end, 'from app.core.resilience import ResilientClient')
            content = '\n'.join(lines)
        
        # Substituir httpx.AsyncClient por ResilientClient
        content = re.sub(
            r'httpx\.AsyncClient\(([^)]*)\)',
            r'ResilientClient(\1)',
            content
        )
        
        client_file.write_text(content)
        rel_path = client_file.relative_to(BASE)
        print(f"   ✅ {rel_path}")
        processed += 1

print(f"\n📊 Clients de integração atualizados: {processed}/{len(integration_files)}")

# Agora aplicar resiliência em repositories que fazem chamadas HTTP
print("\n\n🔥 APLICANDO RESILIÊNCIA EM REPOSITORIES")
print("=========================================\n")

repo_files = list(MODULES.rglob("infrastructure/repositories/*.py"))
repo_files = [f for f in repo_files if f.name != "__init__.py"]

print(f"📊 Total de repositories encontrados: {len(repo_files)}\n")

repo_processed = 0
for repo_file in sorted(repo_files):
    content = repo_file.read_text()
    original_content = content
    
    # Verificar se usa httpx diretamente
    if "httpx" in content and "ResilientClient" not in content:
        
        # Adicionar import
        if "from app.core.resilience import ResilientClient" not in content:
            lines = content.split('\n')
            import_end = 0
            
            for i, line in enumerate(lines):
                if line.startswith(('from ', 'import ')) or line.strip() == '':
                    import_end = i + 1
                elif line.strip() and not line.startswith(('from ', 'import ', '#')):
                    break
            
            lines.insert(import_end, 'from app.core.resilience import ResilientClient')
            content = '\n'.join(lines)
        
        # Substituir httpx.AsyncClient por ResilientClient
        content = re.sub(
            r'httpx\.AsyncClient\(([^)]*)\)',
            r'ResilientClient(\1)',
            content
        )
        
        repo_file.write_text(content)
        rel_path = repo_file.relative_to(BASE)
        print(f"   ✅ {rel_path}")
        repo_processed += 1

print(f"\n📊 Repositories atualizados: {repo_processed}/{len(repo_files)}")

print("\n✅ RESILIÊNCIA GLOBAL APLICADA")
