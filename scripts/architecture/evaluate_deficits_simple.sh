#!/bin/bash
# Simple Module Deficit Evaluation - Batch Processing
# Avalia conformidade DDD + Hexagonal em lotes disciplinados

MODULES_DIR="/home/dev03wsl/sila-system/apps/backend/app/modules"

evaluate_module() {
  local module_name="$1"
  local module_path="$MODULES_DIR/$module_name"
  
  if [ ! -d "$module_path" ]; then
    return 1
  fi
  
  # Verificar componentes (lote 1: estrutura principal)
  local api="❌"
  local app="❌"
  local domain="❌"
  local infra="❌"
  local tests="❌"
  
  [ -d "$module_path/api" ] && api="✅"
  [ -d "$module_path/application" ] && app="✅"
  [ -d "$module_path/domain" ] && domain="✅"
  [ -d "$module_path/infrastructure" ] && infra="✅"
  [ -d "$module_path/tests" ] && tests="✅"
  
  # Verificar padrões (lote 2: especificidade)
  local repos=$(find "$module_path/infrastructure/repositories" -type f -name "*.py" 2>/dev/null | grep -v __init__ | wc -l)
  local ports=$(find "$module_path/domain/ports" -type f -name "*.py" 2>/dev/null | grep -v __init__ | wc -l)
  local commands=$(find "$module_path/application/commands" -type f -name "*.py" 2>/dev/null | grep -v __init__ | wc -l)
  local queries=$(find "$module_path/application/queries" -type f -name "*.py" 2>/dev/null | grep -v __init__ | wc -l)
  
  # Conformidade percentual
  local total=5
  local passed=0
  [ "$api" = "✅" ] && ((passed++))
  [ "$app" = "✅" ] && ((passed++))
  [ "$domain" = "✅" ] && ((passed++))
  [ "$infra" = "✅" ] && ((passed++))
  [ "$tests" = "✅" ] && ((passed++))
  
  local conformity=$((passed * 100 / total))
  
  # Output formatado
  printf "%-28s | API:%s APP:%s DOMAIN:%s INFRA:%s TESTS:%s | REPOS:%2d PORTS:%2d CQ:%2d/%2d | %3d%%\n" \
    "$module_name" "$api" "$app" "$domain" "$infra" "$tests" "$repos" "$ports" "$commands" "$queries" "$conformity"
}

echo "╔════════════════════════════════════════════════════════════════════════════════════════════╗"
echo "║          MODULE DEFICIT EVALUATION - DDD + HEXAGONAL ARCHITECTURE                        ║"
echo "║                                  $(date '+%Y-%m-%d %H:%M:%S')                                        ║"
echo "╚════════════════════════════════════════════════════════════════════════════════════════════╝"
echo ""

echo "📋 LOTE 1: INFRASTRUCTURE_SECTOR (FOCO PRINCIPAL)"
echo "─────────────────────────────────────────────────────────────────────────────────────────────"
evaluate_module "infrastructure_sector"
echo ""

echo "📋 LOTE 2: MÓDULOS CORE (audit, compliance, governance, identity)"
echo "─────────────────────────────────────────────────────────────────────────────────────────────"
for module in audit compliance governance identity; do
  evaluate_module "$module"
done
echo ""

echo "📋 LOTE 3: MÓDULOS DE INTEGRAÇÃO (payment, procurement, economy)"
echo "─────────────────────────────────────────────────────────────────────────────────────────────"
for module in payment procurement economy; do
  evaluate_module "$module"
done
echo ""

echo "📋 LOTE 4: MÓDULOS SETORIAIS (saude, educacao, energy, justice)"
echo "─────────────────────────────────────────────────────────────────────────────────────────────"
for module in saude educacao energy justice; do
  evaluate_module "$module"
done
echo ""

echo "═══════════════════════════════════════════════════════════════════════════════════════════════"
echo "LEGENDA:"
echo "  ✅ = Presente   |   ❌ = Ausente"
echo "  REPOS = Repositórios  |  PORTS = Portas de domínio  |  CQ = Commands/Queries"
echo "═══════════════════════════════════════════════════════════════════════════════════════════════"
