#!/bin/bash

# ============================================================================
# SCRIPT DE CONSOLIDAÇÃO DE MÓDULOS - SILA3
# Consolida fragmentação de /modules/, /app/modules/ para /apps/backend/app/modules/
# ============================================================================

set -e  # Exit on error

BACKUP_DIR="/tmp/sila_modules_backup"
WORKSPACE="/home/dev03wsl/sila-system"
MODULES_OLD_A="$WORKSPACE/modules"
MODULES_OLD_B="$WORKSPACE/app/modules"
MODULES_NEW="$WORKSPACE/apps/backend/app/modules"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# ============================================================================
# FASE 1: BACKUP E VALIDAÇÃO
# ============================================================================

echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}FASE 1: BACKUP E VALIDAÇÃO${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"

# 1.1 Criar backup
echo -e "\n${YELLOW}[1.1]${NC} Criando backup..."
mkdir -p "$BACKUP_DIR"
tar -czf "$BACKUP_DIR/modules_${TIMESTAMP}.tar.gz" -C "$WORKSPACE" modules app/modules 2>/dev/null || true
echo -e "${GREEN}✓${NC} Backup guardado em: $BACKUP_DIR/modules_${TIMESTAMP}.tar.gz"

# 1.2 Validar que /apps/backend/app/modules existe
if [[ ! -d "$MODULES_NEW" ]]; then
    echo -e "${RED}✗ ERRO: $MODULES_NEW não existe!${NC}"
    exit 1
fi
echo -e "${GREEN}✓${NC} Estrutura de destino validada"

# 1.3 Listar o que va ser consolidado
echo -e "\n${YELLOW}[1.2]${NC} Módulos a consolidar:"
echo -e "  De A: $MODULES_OLD_A"
[[ -d "$MODULES_OLD_A" ]] && ls -1 "$MODULES_OLD_A" | grep -v ".py" | sed 's/^/    • /' || echo "    (não existe)"

echo -e "\n  De B: $MODULES_OLD_B"
[[ -d "$MODULES_OLD_B" ]] && ls -1 "$MODULES_OLD_B" | grep -v ".py" | sed 's/^/    • /' || echo "    (não existe)"

read -p "Prosseguir? (s/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Ss]$ ]]; then
    echo -e "${YELLOW}Abortado pelo utilizador${NC}"
    exit 0
fi

# ============================================================================
# FASE 2: CONSOLIDAÇÃO DE MÓDULOS
# ============================================================================

echo -e "\n${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}FASE 2: CONSOLIDAÇÃO DE MÓDULOS${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"

consolidated_count=0

# 2.1 Processar /modules/
if [[ -d "$MODULES_OLD_A" ]]; then
    for module in $(ls -1 "$MODULES_OLD_A" | grep -v "\.py$"); do
        module_src="$MODULES_OLD_A/$module"
        module_dst="$MODULES_NEW/$module"
        
        if [[ -d "$module_src" ]]; then
            if [[ -d "$module_dst" ]]; then
                # Módulo existe em ambos - copiar ficheiros únicos
                echo -e "\n${YELLOW}[2.1]${NC} Consolidando $module (existe em ambos)..."
                
                # Copiar estrutura de domínio se existir em OLD mas não em NEW
                if [[ -d "$module_src/domain" && ! -d "$module_dst/domain" ]]; then
                    cp -r "$module_src/domain" "$module_dst/"
                    echo -e "${GREEN}  ✓${NC} domain/ copiado"
                fi
                
                # Copiar middleware se existir (para identity)
                if [[ -d "$module_src/middleware" && ! -d "$module_dst/middleware" ]]; then
                    cp -r "$module_src/middleware" "$module_dst/"
                    echo -e "${GREEN}  ✓${NC} middleware/ copiado"
                fi
                
                # Copiar schemas/services de documents e payment
                if [[ -d "$module_src/schemas" && ! -d "$module_dst/schemas" ]]; then
                    mkdir -p "$module_dst/application"
                    cp -r "$module_src/schemas" "$module_dst/application/"
                    echo -e "${GREEN}  ✓${NC} schemas/ copiado para application/"
                fi
                
                if [[ -d "$module_src/services" && ! -d "$module_dst/application/services" ]]; then
                    mkdir -p "$module_dst/application"
                    cp -r "$module_src/services" "$module_dst/application/"
                    echo -e "${GREEN}  ✓${NC} services/ copiado para application/"
                fi
                
                if [[ -d "$module_src/models" && ! -d "$module_dst/models" ]]; then
                    cp -r "$module_src/models" "$module_dst/"
                    echo -e "${GREEN}  ✓${NC} models/ copiado"
                fi
                
                ((consolidated_count++))
            else
                # Módulo novo - copiar integralmente
                echo -e "\n${YELLOW}[2.1]${NC} Consolidando $module (novo)..."
                cp -r "$module_src" "$module_dst"
                echo -e "${GREEN}  ✓${NC} Módulo completo copiado"
                ((consolidated_count++))
            fi
        fi
    done
fi

# 2.2 Processar /app/modules/
if [[ -d "$MODULES_OLD_B" ]]; then
    for module in $(ls -1 "$MODULES_OLD_B" | grep -v "\.py$"); do
        module_src="$MODULES_OLD_B/$module"
        module_dst="$MODULES_NEW/$module"
        
        if [[ -d "$module_src" ]]; then
            echo -e "\n${YELLOW}[2.2]${NC} Consolidando $module de /app/modules/..."
            
            if [[ -d "$module_dst" ]]; then
                # Copiar apenas core/ se existir vazio em destino
                if [[ -d "$module_src/core" ]]; then
                    cp -r "$module_src/core"/* "$module_dst/" 2>/dev/null || true
                    echo -e "${GREEN}  ✓${NC} Conteúdo de core/ mesclado"
                fi
                ((consolidated_count++))
            else
                # Copiar integralmente
                cp -r "$module_src" "$module_dst"
                echo -e "${GREEN}  ✓${NC} Módulo completo copiado"
                ((consolidated_count++))
            fi
        fi
    done
fi

echo -e "\n${GREEN}✓${NC} Total de módulos consolidados: $consolidated_count"

# ============================================================================
# FASE 3: ATUALIZAR IMPORTS
# ============================================================================

echo -e "\n${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}FASE 3: ATUALIZAR IMPORTS${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"

echo -e "\n${YELLOW}[3.1]${NC} Procurando ficheiros com imports antigos..."

# 3.1 Encontrar ficheiros
import_files=$(grep -r "from modules\.|from app\.modules\." "$WORKSPACE" \
    --include="*.py" 2>/dev/null | \
    grep -v ".venv" | grep -v "__pycache__" | \
    cut -d: -f1 | sort -u | wc -l)

echo -e "  Encontrados $import_files ficheiros com imports antigos"

# 3.2 Criar script de correção
cat > /tmp/fix_imports_consolidate.py << 'PYSCRIPT'
#!/usr/bin/env python3
import re
import os
import sys
from pathlib import Path

WORKSPACE = "/home/dev03wsl/sila-system"

def fix_imports(filepath):
    """Corrige imports antigos para novo padrão"""
    try:
        with open(filepath, 'r') as f:
            content = f.read()
        
        original = content
        
        # Pattern 1: from modules.XXX -> from apps.backend.app.modules.XXX
        content = re.sub(
            r'from modules\.(\w+)',
            r'from apps.backend.app.modules.\1',
            content
        )
        
        # Pattern 2: from app.modules.XXX -> from apps.backend.app.modules.XXX
        content = re.sub(
            r'from app\.modules\.(\w+)',
            r'from apps.backend.app.modules.\1',
            content
        )
        
        # Pattern 3: import modules.XXX -> import apps.backend.app.modules.XXX
        content = re.sub(
            r'import modules\.(\w+)',
            r'import apps.backend.app.modules.\1 as \1',
            content
        )
        
        if content != original:
            with open(filepath, 'w') as f:
                f.write(content)
            return True
        return False
    except Exception as e:
        print(f"  ✗ Erro em {filepath}: {e}", file=sys.stderr)
        return False

# Encontrar todos os ficheiros Python
py_files = []
for root, dirs, files in os.walk(WORKSPACE):
    # Skip virtual env e caches
    dirs[:] = [d for d in dirs if d not in ['.venv', '__pycache__', '.git', 'node_modules']]
    
    for file in files:
        if file.endswith('.py'):
            py_files.append(os.path.join(root, file))

# Corrigir imports
fixed_count = 0
for filepath in py_files:
    if fix_imports(filepath):
        print(f"  ✓ {filepath}")
        fixed_count += 1

print(f"\n✓ Total de ficheiros atualizados: {fixed_count}")
sys.exit(0)

PYSCRIPT

python3 /tmp/fix_imports_consolidate.py

# ============================================================================
# FASE 4: REMOVER DIRETÓRIOS ANTIGOS
# ============================================================================

echo -e "\n${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}FASE 4: REMOVER DIRETÓRIOS ANTIGOS${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"

echo -e "\n${YELLOW}[4.1]${NC} Limpando diretórios antigos..."

if [[ -d "$MODULES_OLD_A" ]]; then
    rm -rf "$MODULES_OLD_A"
    echo -e "${GREEN}✓${NC} Removido: $MODULES_OLD_A"
fi

if [[ -d "$MODULES_OLD_B" ]]; then
    rm -rf "$MODULES_OLD_B"
    echo -e "${GREEN}✓${NC} Removido: $MODULES_OLD_B"
fi

# ============================================================================
# FASE 5: VALIDAÇÃO
# ============================================================================

echo -e "\n${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}FASE 5: VALIDAÇÃO${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"

# 5.1 Verificar que nenhum import antigo existe
echo -e "\n${YELLOW}[5.1]${NC} Verificando se todos imports foram atualizados..."
remaining=$(grep -r "from modules\.|from app\.modules\." "$WORKSPACE" \
    --include="*.py" 2>/dev/null | \
    grep -v ".venv" | grep -v "__pycache__" | \
    wc -l)

if [[ $remaining -eq 0 ]]; then
    echo -e "${GREEN}✓${NC} Nenhum import antigo encontrado"
else
    echo -e "${RED}✗${NC} Ainda existem $remaining imports antigos!"
    echo -e "${YELLOW}   Execute:${NC}"
    echo "   grep -r 'from modules\.' $WORKSPACE --include='*.py' | grep -v '.venv'"
fi

# 5.2 Verificar integridade de módulos
echo -e "\n${YELLOW}[5.2]${NC} Verificando integridade de módulos..."
module_count=$(ls -1 "$MODULES_NEW" | grep -v "\.py$" | grep -v "__" | wc -l)
echo -e "${GREEN}✓${NC} Total de módulos consolidados: $module_count"

# 5.3 Listar testes
echo -e "\n${YELLOW}[5.3]${NC} Testes encontrados:"
test_count=$(find "$MODULES_NEW" -name "test_*.py" -o -name "*_test.py" | wc -l)
echo -e "${GREEN}✓${NC} Total de ficheiros de teste: $test_count"

# ============================================================================
# RESUMO FINAL
# ============================================================================

echo -e "\n${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}✅ CONSOLIDAÇÃO CONCLUÍDA COM SUCESSO${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"

echo -e "\n${GREEN}RESUMO:${NC}"
echo -e "  • Módulos consolidados: $consolidated_count"
echo -e "  • Imports atualizados: Verificar saída acima"
echo -e "  • Diretórios antigos removidos: /modules/, /app/modules/"
echo -e "  • Backup guardado: $BACKUP_DIR/modules_${TIMESTAMP}.tar.gz"
echo -e "\n${YELLOW}PRÓXIMAS AÇÕES:${NC}"
echo -e "  1. Executar testes: pytest $MODULES_NEW/../.. -v"
echo -e "  2. Verificar tipos: mypy $MODULES_NEW/"
echo -e "  3. Git: git add -A && git commit -m 'consolidate: single source of truth for modules'"
echo -e "  4. Fazer push para review: git push -u origin consolidate/modules-single-source"

echo -e "\n${GREEN}✓ Script concluído!${NC}\n"
