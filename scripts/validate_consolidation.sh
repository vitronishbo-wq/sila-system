#!/bin/bash

# ============================================================================
# SCRIPT DE VALIDAÇÃO - Verificar saúde da consolidação
# ============================================================================

WORKSPACE="/home/dev03wsl/sila-system"
MODULES="$WORKSPACE/apps/backend/app/modules"

echo "════════════════════════════════════════════════════════════════"
echo "VALIDAÇÃO DE CONSOLIDAÇÃO DE MÓDULOS"
echo "════════════════════════════════════════════════════════════════"

# 1. Verificar que diretórios antigos foram removidos
echo -e "\n[1] Verificar remoção de diretórios antigos..."
if [[ -d "$WORKSPACE/modules" ]]; then
    echo "  ✗ ERRO: /modules/ ainda existe!"
else
    echo "  ✓ /modules/ foi removido"
fi

if [[ -d "$WORKSPACE/app/modules" ]]; then
    echo "  ✗ ERRO: /app/modules/ ainda existe!"
else
    echo "  ✓ /app/modules/ foi removido"
fi

# 2. Verificar que MODULES_NEW existe
echo -e "\n[2] Verificar localização única..."
if [[ ! -d "$MODULES" ]]; then
    echo "  ✗ ERRO: $MODULES não existe!"
    exit 1
fi
echo "  ✓ Localização unificada confirmada: $MODULES"

# 3. Contar módulos
echo -e "\n[3] Verificar módulos consolidados..."
module_count=$(ls -1 "$MODULES" | grep -v "\.py\|__" | wc -l)
echo "  ✓ Total de módulos: $module_count"
ls -1 "$MODULES" | grep -v "\.py\|__" | sed 's/^/    • /'

# 4. Verificar imports antigos
echo -e "\n[4] Verificar imports antigos (CRÍTICO)..."
old_imports=$(grep -r "from modules\.|from app\.modules\." "$WORKSPACE" \
    --include="*.py" 2>/dev/null | \
    grep -v ".venv" | grep -v "__pycache__" | wc -l)

if [[ $old_imports -gt 0 ]]; then
    echo "  ✗ ERRO: Ainda existem $old_imports imports antigos!"
    echo -e "\n  Ficheiros afetados:"
    grep -r "from modules\.|from app\.modules\." "$WORKSPACE" \
        --include="*.py" 2>/dev/null | \
        grep -v ".venv" | cut -d: -f1 | sort -u | sed 's/^/    • /'
    exit 1
else
    echo "  ✓ Nenhum import antigo encontrado"
fi

# 5. Verificar estrutura hexagonal
echo -e "\n[5] Verificar estrutura hexagonal em módulos..."
hexagonal_modules=0
for module in $(ls -1 "$MODULES" | grep -v "\.py\|__"); do
    module_path="$MODULES/$module"
    if [[ -d "$module_path" ]]; then
        # Verificar se tem estrutura hexagonal
        if [[ -d "$module_path/api" || -d "$module_path/application" || -d "$module_path/domain" || -d "$module_path/infrastructure" ]]; then
            ((hexagonal_modules++))
        fi
    fi
done
echo "  ✓ Módulos com arquitetura hexagonal: $hexagonal_modules/$module_count"

# 6. Verificar ficheiros de teste
echo -e "\n[6] Verificar testes consolidados..."
test_files=$(find "$MODULES" -name "test_*.py" -o -name "*_test.py" | wc -l)
echo "  ✓ Ficheiros de teste encontrados: $test_files"

# 7. Verificar duplicação de módulos
echo -e "\n[7] Verificar duplicação de módulos..."
all_modules=$(ls -1 "$MODULES" | grep -v "\.py\|__")
duplicates=$(echo "$all_modules" | sort | uniq -d | wc -l)
if [[ $duplicates -gt 0 ]]; then
    echo "  ✗ ERRO: Encontrados $duplicates módulos duplicados!"
else
    echo "  ✓ Nenhum módulo duplicado"
fi

# 8. Verificar module.yaml
echo -e "\n[8] Verificar ficheiros de configuração (module.yaml)..."
yaml_count=$(find "$MODULES" -name "module.yaml" | wc -l)
echo "  ✓ Ficheiros module.yaml: $yaml_count"

# 9. Verificar ARCHITECTURE.md
echo -e "\n[9] Verificar documentação de arquitetura..."
arch_count=$(find "$MODULES" -name "ARCHITECTURE.md" | wc -l)
echo "  ✓ Ficheiros ARCHITECTURE.md: $arch_count"

# 10. Validação Python
echo -e "\n[10] Validação Python (syntax check)..."
syntax_errors=$(python3 -m py_compile "$MODULES"/*.py 2>&1 | wc -l)
if [[ $syntax_errors -gt 0 ]]; then
    echo "  ✗ Erros de syntax encontrados"
else
    echo "  ✓ Nenhum erro de syntax"
fi

# ============================================================================
# RESUMO
# ============================================================================

echo -e "\n════════════════════════════════════════════════════════════════"
echo "RESUMO DE VALIDAÇÃO"
echo "════════════════════════════════════════════════════════════════"

if [[ $old_imports -eq 0 && $syntax_errors -eq 0 ]]; then
    echo -e "\n✅ CONSOLIDAÇÃO VALIDADA COM SUCESSO!\n"
    exit 0
else
    echo -e "\n❌ PROBLEMAS ENCONTRADOS - REVISE A CONSOLIDAÇÃO\n"
    exit 1
fi
