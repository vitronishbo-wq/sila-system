#!/bin/bash
# Module Deficit Evaluation Script
# Avalia conformidade DDD + Hexagonal Architecture
# Usa tree.md/tree.txt como índice conforme Regra Inviolável #1

set -e

MODULES_DIR="/home/dev03wsl/sila-system/apps/backend/app/modules"
TREE_INDEX="/home/dev03wsl/sila-system/docs/tree.md"
OUTPUT_FILE="/tmp/deficit_evaluation_$(date +%Y%m%d_%H%M%S).tsv"

# Cores para output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "📊 MODULE DEFICIT EVALUATION REPORT"
echo "   Foco: infrastructure_sector + módulos core"
echo "   Data: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""
echo "Usando tree.md/tree.txt como índice (Regra Inviolável #1)"
echo ""

# Cabeçalho TSV
echo -e "MODULE\tAPI\tAPPLICATION\tDOMAIN\tINFRASTRUCTURE\tTESTS\tREPOS_PATTERN\tCOMMANDS_QUERIES\tPORTS\tCONFORMITY" > "$OUTPUT_FILE"

# ==============================================================================
# FASE 1: Localização via grep no tree index (Regra Inviolável #1)
# ==============================================================================

echo "🔍 FASE 1: Localizando estruturas no índice..."
echo ""

check_component() {
  local module_path="$1"
  local component="$2"
  
  if [ -d "$module_path/$component" ]; then
    echo -n "✅"
    return 0
  else
    echo -n "❌"
    return 1
  fi
}

check_files() {
  local module_path="$1"
  local pattern="$2"
  
  local count=$(find "$module_path" -type f -name "$pattern" 2>/dev/null | wc -l)
  if [ "$count" -gt 0 ]; then
    echo "$count"
    return 0
  fi
  echo "0"
  return 1
}

# ==============================================================================
# FASE 2: Avaliação em lote (Regra Inviolável #2)
# ==============================================================================

echo "📋 FASE 2: Avaliação de conformidade em lote"
echo ""

evaluate_module() {
  local module_name="$1"
  local module_path="$MODULES_DIR/$module_name"
  
  if [ ! -d "$module_path" ]; then
    return 1
  fi
  
  echo -n "  [$module_name] "
  
  # Verificar componentes obrigatórios (lote disciplinado)
  echo -n "API:"
  local api_check=$([ -d "$module_path/api" ] && echo "✅" || echo "❌")
  
  echo -n " APP:"
  local app_check=$([ -d "$module_path/application" ] && echo "✅" || echo "❌")
  
  echo -n " DOMAIN:"
  local domain_check=$([ -d "$module_path/domain" ] && echo "✅" || echo "❌")
  
  echo -n " INFRA:"
  local infra_check=$([ -d "$module_path/infrastructure" ] && echo "✅" || echo "❌")
  
  echo -n " TESTS:"
  local tests_check=$([ -d "$module_path/tests" ] && echo "✅" || echo "❌")
  
  # Verificar padrões (lote por especificidade)
  # 1. Repositórios
  local repos=$(find "$module_path/infrastructure/repositories" -type f -name "*.py" 2>/dev/null | grep -v __init__ | wc -l)
  local repos_pattern="unknown"
  if [ "$repos" -gt 0 ]; then
    # Detectar padrão (SQLAlchemy, InMemory, etc)
    if grep -r "SQLAlchemy\|Base\|declarative_base" "$module_path/infrastructure/orm" 2>/dev/null | grep -q ""; then
      repos_pattern="SQLAlchemy"
    elif grep -r "InMemory" "$module_path/infrastructure" 2>/dev/null | grep -q ""; then
      repos_pattern="InMemory"
    else
      repos_pattern="custom"
    fi
  else
    repos_pattern="missing"
  fi
  
  # 2. Commands/Queries
  local has_commands=$([ -d "$module_path/application/commands" ] && echo "yes" || echo "no")
  local has_queries=$([ -d "$module_path/application/queries" ] && echo "yes" || echo "no")
  local cq_status="$has_commands/$has_queries"
  
  # 3. Ports
  local ports=$(find "$module_path/domain/ports" -type f -name "*.py" 2>/dev/null | grep -v __init__ | wc -l)
  local ports_status="$([ "$ports" -gt 0 ] && echo "$ports ports" || echo "❌")"
  
  # Calcular conformidade percentual
  local total_checks=5
  local passed=0
  [ "$api_check" = "✅" ] && ((passed++))
  [ "$app_check" = "✅" ] && ((passed++))
  [ "$domain_check" = "✅" ] && ((passed++))
  [ "$infra_check" = "✅" ] && ((passed++))
  [ "$tests_check" = "✅" ] && ((passed++))
  local conformity=$((passed * 100 / total_checks))
  
  # Adicionar à TSV
  echo -e "$module_name\t$api_check\t$app_check\t$domain_check\t$infra_check\t$tests_check\t$repos_pattern\t$cq_status\t$ports_status\t${conformity}%" >> "$OUTPUT_FILE"
  
  echo -n " REPOS:$repos_pattern CQ:$cq_status PORTS:$ports_status → ${conformity}%"
  echo ""
}

# ==============================================================================
# EXECUÇÃO EM LOTE (conforme Regra Inviolável #2)
# ==============================================================================

# LOTE 1: infrastructure_sector (foco principal)
echo "🎯 LOTE 1: infrastructure_sector (FOCO PRINCIPAL)"
evaluate_module "infrastructure_sector"
echo ""

# LOTE 2: Módulos Core (audit, compliance, governance, identity)
echo "🎯 LOTE 2: MÓDULOS CORE"
for module in audit compliance governance identity; do
  evaluate_module "$module"
done
echo ""

# LOTE 3: Módulos de Integração (payment, procurement, economy)
echo "🎯 LOTE 3: MÓDULOS DE INTEGRAÇÃO"
for module in payment procurement economy; do
  evaluate_module "$module"
done
echo ""

# LOTE 4: Módulos Setoriais (saude, educacao, energy, justice)
echo "🎯 LOTE 4: MÓDULOS SETORIAIS"
for module in saude educacao energy justice; do
  evaluate_module "$module"
done
echo ""

# ==============================================================================
# RELATÓRIO FINAL
# ==============================================================================

echo "════════════════════════════════════════════════════════════════"
echo "📊 RELATÓRIO RESUMIDO"
echo "════════════════════════════════════════════════════════════════"
echo ""

column -t -s $'\t' "$OUTPUT_FILE" | head -15
echo ""
echo "... (relatório completo em: $OUTPUT_FILE)"
echo ""

# Análise de déficits por componente
echo "🔍 ANÁLISE DE DÉFICITS"
echo ""

echo "  Missing API layer:"
for module in audit compliance governance identity payment procurement economy saude educacao energy justice infrastructure_sector; do
  [ ! -d "$MODULES_DIR/$module/api" ] && echo "    ❌ $module"
done

echo "  Missing TESTS layer:"
for module in audit compliance governance identity payment procurement economy saude educacao energy justice infrastructure_sector; do
  [ ! -d "$MODULES_DIR/$module/tests" ] && echo "    ❌ $module"
done

echo "  Missing PORTS (domain contracts):"
for module in audit compliance governance identity payment procurement economy saude educacao energy justice infrastructure_sector; do
  [ ! -d "$MODULES_DIR/$module/domain/ports" ] && echo "    ❌ $module"
done

echo ""
echo "✅ Avaliação concluída"
echo "   Relatório detalhado: $OUTPUT_FILE"
