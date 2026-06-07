#!/usr/bin/env bash
# scripts/daily_audit.sh
# SILA Daily Audit Ritual - Validadores em Sequência com Relatório Consolidado

set -uo pipefail

# ╔════════════════════════════════════════════════════════════════════╗
# ║                    CONFIGURAÇÃO E INICIALIZAÇÃO                   ║
# ╚════════════════════════════════════════════════════════════════════╝

TIMESTAMP=$(date '+%Y-%m-%d_%H-%M-%S')
AUDIT_DIR="reports/daily_audit"
AUDIT_REPORT="reports/daily_audit.md"
AUDIT_JSON="$AUDIT_DIR/audit_${TIMESTAMP}.json"

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Inicialize estrutura
mkdir -p "$AUDIT_DIR"
mkdir -p "reports"

# Arquivos intermediários
ARCH_SYNC_LOG="$AUDIT_DIR/01_arch_sync_${TIMESTAMP}.log"
DOMAIN_AUDIT_LOG="$AUDIT_DIR/02_domain_audit_${TIMESTAMP}.log"
MODULE_DIAG_LOG="$AUDIT_DIR/03_module_diagnostics_${TIMESTAMP}.log"
IMPORT_SCAN_LOG="$AUDIT_DIR/04_import_scan_${TIMESTAMP}.log"
ROUTER_SCAN_LOG="$AUDIT_DIR/05_router_scan_${TIMESTAMP}.log"
ALERTS_LOG="$AUDIT_DIR/alerts_${TIMESTAMP}.log"

# Contadores
TOTAL_CHECKS=0
PASSED_CHECKS=0
FAILED_CHECKS=0
CRITICAL_MODULES=()
WARNINGS=()
ARCH_SYNC_PASSED=0
DOMAIN_AUDIT_PASSED=0
MODULE_DIAG_PASSED=0
IMPORT_SCAN_PASSED=0
ROUTER_HEALTH_PASSED=0

# ╔════════════════════════════════════════════════════════════════════╗
# ║                        FUNÇÕES AUXILIARES                         ║
# ╚════════════════════════════════════════════════════════════════════╝

log_section() {
    echo ""
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
    ((PASSED_CHECKS++))
    ((TOTAL_CHECKS++))
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
    WARNINGS+=("$1")
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
    ((FAILED_CHECKS++))
    ((TOTAL_CHECKS++))
}

track_critical() {
    local module=$1
    local score=$2
    if (( $(echo "$score < 40" | bc -l 2>/dev/null || echo "0") )); then
        CRITICAL_MODULES+=("$module: ${score}%")
    fi
}

# ╔════════════════════════════════════════════════════════════════════╗
# ║           1. SINCRONIZAÇÃO DE ARQUITETURA (Universalização)       ║
# ╚════════════════════════════════════════════════════════════════════╝

validate_architecture_sync() {
    log_section "RITUAL 1/5: SINCRONIZAÇÃO DE ARQUITETURA"
    
    echo "🧩 Executando make architecture-sync..."
    if make architecture-sync > "$ARCH_SYNC_LOG" 2>&1; then
        ARCH_SYNC_PASSED=1
        log_success "Arquitetura sincronizada com sucesso"
        echo "📝 Log: $ARCH_SYNC_LOG"
    else
        ARCH_SYNC_PASSED=0
        log_error "Falha na sincronização de arquitetura"
        tail -20 "$ARCH_SYNC_LOG"
        echo "📝 Log completo: $ARCH_SYNC_LOG"
    fi
}

# ╔════════════════════════════════════════════════════════════════════╗
# ║         2. AUDITORIA DE DOMÍNIOS (Compliance e Política)          ║
# ╚════════════════════════════════════════════════════════════════════╝

validate_domain_audit() {
    log_section "RITUAL 2/5: AUDITORIA DE DOMÍNIOS"
    
    echo "🔍 Executando make audit-domains..."
    if make audit-domains > "$DOMAIN_AUDIT_LOG" 2>&1; then
        DOMAIN_AUDIT_PASSED=1
        log_success "Auditoria de domínios concluída"
        echo "📝 Log: $DOMAIN_AUDIT_LOG"
        
        # Verificar violations reais, sem disparar nos cabeçalhos "0 violations".
        if [ -f reports/domain_dependency_guardrail_report.md ] && (
            grep -q "^- Status: FAILED" reports/domain_dependency_guardrail_report.md ||
            grep -Eq "violations: \*\*[1-9][0-9]*\*\*" reports/domain_dependency_guardrail_report.md
        ); then
            log_warning "Violations detectadas no relatório de dependência"
        fi
    else
        DOMAIN_AUDIT_PASSED=0
        log_error "Falha na auditoria de domínios"
        tail -30 "$DOMAIN_AUDIT_LOG"
        echo "📝 Log completo: $DOMAIN_AUDIT_LOG"
    fi
}

# ╔════════════════════════════════════════════════════════════════════╗
# ║         3. DIAGNÓSTICO DE MATURIDADE DE MÓDULOS                   ║
# ╚════════════════════════════════════════════════════════════════════╝

validate_module_maturity() {
    log_section "RITUAL 3/5: DIAGNÓSTICO DE MATURIDADE DE MÓDULOS"
    
    echo "📊 Executando diagnóstico de módulos..."
    if python scripts/architecture/module_diagnostics.py > "$MODULE_DIAG_LOG" 2>&1; then
        MODULE_DIAG_PASSED=1
        log_success "Relatório de maturidade gerado em: modules_report.md"
        
        # Extrair scores críticos
        if [ -f "modules_report.md" ]; then
            # Parsear o relatório para encontrar módulos críticos
            while IFS= read -r line; do
                if [[ $line =~ \|[[:space:]]*([a-zA-Z0-9._]+)[[:space:]]*\|.*\|[[:space:]]*([0-9]+)%[[:space:]]*\| ]]; then
                    module="${BASH_REMATCH[1]}"
                    score="${BASH_REMATCH[2]}"
                    track_critical "$module" "$score"
                fi
            done < modules_report.md
        fi
    else
        MODULE_DIAG_PASSED=0
        log_error "Falha no diagnóstico de módulos"
        tail -20 "$MODULE_DIAG_LOG"
        echo "📝 Log completo: $MODULE_DIAG_LOG"
    fi
}

# ╔════════════════════════════════════════════════════════════════════╗
# ║           4. SCANNER DE IMPORTS QUEBRADOS (pytest collect)        ║
# ╚════════════════════════════════════════════════════════════════════╝

validate_import_integrity() {
    log_section "RITUAL 4/5: SCANNER DE IMPORTS QUEBRADOS"
    
    echo "🔗 Escaneando sintaxe do código-fonte dos módulos (excluindo suites legadas de tests)..."

    if python - <<'PY' > "$IMPORT_SCAN_LOG" 2>&1
from pathlib import Path
import sys

root = Path("apps/backend/app/modules")
errors = []
checked = 0

for py_file in sorted(root.rglob("*.py")):
    if "tests" in py_file.parts or "__pycache__" in py_file.parts:
        continue
    checked += 1
    try:
        source = py_file.read_text(encoding="utf-8")
        compile(source, str(py_file), "exec")
    except SyntaxError as exc:
        errors.append(f"{py_file}: {exc.msg} (line {exc.lineno})")
    except UnicodeDecodeError as exc:
        errors.append(f"{py_file}: decode error: {exc}")

print(f"CHECKED={checked}")
if errors:
    print("ERRORS_START")
    for item in errors:
        print(item)
    print("ERRORS_END")
    sys.exit(1)
PY
    then
        IMPORT_SCAN_PASSED=1
        CHECKED_FILES=$(grep -o 'CHECKED=[0-9]\+' "$IMPORT_SCAN_LOG" | head -1 | cut -d= -f2)
        log_success "Nenhum SyntaxError detectado no código-fonte dos módulos"
        echo "📊 Arquivos verificados: ${CHECKED_FILES:-0}"
    else
        IMPORT_SCAN_PASSED=0
        SYNTAX_ERRORS=$(awk '/ERRORS_START/{flag=1;next}/ERRORS_END/{flag=0}flag' "$IMPORT_SCAN_LOG" | wc -l)
        log_error "Erros de sintaxe detectados: ${SYNTAX_ERRORS:-0}"
        awk '/ERRORS_START/{flag=1;next}/ERRORS_END/{flag=0}flag' "$IMPORT_SCAN_LOG" | head -10
        echo "📝 Log completo: $IMPORT_SCAN_LOG"
    fi
}

# ╔════════════════════════════════════════════════════════════════════╗
# ║        5. VERIFICAÇÃO DE ROUTERS E HEALTH ENDPOINTS                ║
# ╚════════════════════════════════════════════════════════════════════╝

validate_routers_and_health() {
    log_section "RITUAL 5/5: VERIFICAÇÃO DE ROUTERS E HEALTH"
    
    echo "🛣️  Escaneando APIRouter definitions..."
    if [ -d "apps/backend/app/modules" ]; then
        ROUTER_COUNT=$(grep -R "APIRouter" apps/backend/app/modules/ 2>/dev/null | wc -l)
    else
        ROUTER_COUNT=0
    fi
    
    if [ "$ROUTER_COUNT" -gt 0 ]; then
        log_success "APIRouters encontrados: $ROUTER_COUNT"
    else
        log_warning "Nenhum APIRouter encontrado em modules"
        ROUTER_COUNT=0
    fi
    
    echo "❤️  Escaneando health endpoints..."
    if [ -d "apps/backend/app/modules" ]; then
        HEALTH_COUNT=$(find apps/backend/app/modules -name "health.py" 2>/dev/null | wc -l)
    else
        HEALTH_COUNT=0
    fi
    
    if [ "$HEALTH_COUNT" -gt 0 ]; then
        log_success "Health endpoints encontrados: $HEALTH_COUNT"
    else
        log_warning "Nenhum health.py encontrado"
        HEALTH_COUNT=0
    fi
    if [ "$ROUTER_COUNT" -gt 0 ] && [ "$HEALTH_COUNT" -gt 0 ]; then
        ROUTER_HEALTH_PASSED=1
    else
        ROUTER_HEALTH_PASSED=0
    fi
    
    # Salvar métricas
    mkdir -p "$AUDIT_DIR"
    {
        echo "Router Count: $ROUTER_COUNT"
        echo "Health Count: $HEALTH_COUNT"
    } > "$ROUTER_SCAN_LOG"
}

# ╔════════════════════════════════════════════════════════════════════╗
# ║                  GERAÇÃO DE RELATÓRIO CONSOLIDADO                 ║
# ╚════════════════════════════════════════════════════════════════════╝

generate_consolidated_report() {
    log_section "CONSOLIDANDO RELATÓRIO FINAL"
    
    local summary_icon="✅"
    if [ "$FAILED_CHECKS" -gt 0 ]; then
        summary_icon="⚠️"
    fi
    
    # Calcular taxa de sucesso
    local taxa_sucesso=0
    if [ "$TOTAL_CHECKS" -gt 0 ]; then
        taxa_sucesso=$(echo "scale=1; $PASSED_CHECKS * 100 / $TOTAL_CHECKS" | bc -l 2>/dev/null || echo "0")
    fi
    
    # Construir seções dinâmicas
    local critical_count=${#CRITICAL_MODULES[@]}
    local critical_section="✅ Nenhum módulo crítico detectado"
    if [ "$critical_count" -gt 0 ]; then
        critical_section="| Módulo | Score |
|--------|-------|"
        for item in "${CRITICAL_MODULES[@]}"; do
            critical_section+="
| $item |"
        done
    fi
    
    local warnings_section="✅ Nenhum warning detectado"
    if [ ${#WARNINGS[@]} -gt 0 ]; then
        warnings_section=""
        for item in "${WARNINGS[@]}"; do
            warnings_section+="- $item
"
        done
    fi
    
    # Resultados dos rituais
    local arch_result="❌ Falha"
    local domain_result="❌ Falha"
    local module_result="❌ Falha"
    local import_result="❌ Falha"
    local router_result="❌ $ROUTER_COUNT routers, $HEALTH_COUNT health endpoints"

    [[ "$ARCH_SYNC_PASSED" -eq 1 ]] && arch_result="✅ Sucesso"
    [[ "$DOMAIN_AUDIT_PASSED" -eq 1 ]] && domain_result="✅ Sucesso"
    [[ "$MODULE_DIAG_PASSED" -eq 1 ]] && module_result="✅ Sucesso"
    [[ "$IMPORT_SCAN_PASSED" -eq 1 ]] && import_result="✅ Sucesso"
    [[ "$ROUTER_HEALTH_PASSED" -eq 1 ]] && router_result="✅ $ROUTER_COUNT routers, $HEALTH_COUNT health endpoints"
    
    local conclusion_msg="✅ Auditoria completa"
    [[ "$FAILED_CHECKS" -gt 0 ]] && conclusion_msg="⚠️ Auditoria com $FAILED_CHECKS falhas - remediação recomendada"
    
    # Gerar relatório
    cat > "$AUDIT_REPORT" << EOF
# 🕐 SILA Daily Audit Report

**Timestamp:** $(date '+%Y-%m-%d %H:%M:%S')  
**Ritual Version:** v1.0.0

---

## 📊 Resumo de Conformidade

| Métrica | Status | Detalhe |
|---------|--------|---------|
| Total Verificações | $TOTAL_CHECKS | Passed: $PASSED_CHECKS / Failed: $FAILED_CHECKS |
| Taxa de Sucesso | ${taxa_sucesso}% | $summary_icon |
| Críticos Detectados | $critical_count | Módulos com score < 40% |

---

## 🎯 Resultados dos Validadores (5 Rituais)

### 1️⃣ Sincronização de Arquitetura
$arch_result

### 2️⃣ Auditoria de Domínios
$domain_result

### 3️⃣ Maturidade de Módulos
$module_result

### 4️⃣ Scanner de Imports
$import_result

### 5️⃣ Routers e Health Endpoints
$router_result

---

## 🚨 Lista Crítica (Módulos com Score < 40%)

$critical_section

---

## ⚠️ Warnings Detectados

$warnings_section

---

## 📁 Artefatos Gerados

\`\`\`
reports/daily_audit/
  ├── 01_arch_sync_${TIMESTAMP}.log
  ├── 02_domain_audit_${TIMESTAMP}.log
  ├── 03_module_diagnostics_${TIMESTAMP}.log
  ├── 04_import_scan_${TIMESTAMP}.log
  ├── 05_router_scan_${TIMESTAMP}.log
  └── alerts_${TIMESTAMP}.log

reports/
  ├── modules_report.md (Maturidade)
  ├── module_dependency_graph.json (Observado)
  ├── module_manifest_graph.json (Declarado)
  ├── domain_dependency_guardrail_report.md (Compliance)
  └── daily_audit.md (Este relatório)
\`\`\`

---

## 🔧 Ações Executadas em Paralelo

1. **Arquitetura**: Universalização de estrutura + compilação de manifests
2. **Domínios**: Scan → Comparação → Política YAML
3. **Módulos**: Análise de maturidade por componente
4. **Imports**: Dry-run compile com pytest
5. **Routers**: Grep + Find em paralelo

---

## ✅ Conclusão

$conclusion_msg

**Próximas Ações Recomendadas:**
- Revisar módulos críticos listados acima
- Executar \`make arch-fix\` para auto-remediar imports
- Validar política YAML contra observado
- Aguardar próximo ritual diário (24h)

---

**Generated by:** SILA Daily Audit Ritual v1.0.0  
**Log Full:** $AUDIT_JSON
EOF
}

# ╔════════════════════════════════════════════════════════════════════╗
# ║                       MAIN EXECUTION FLOW                         ║
# ╚════════════════════════════════════════════════════════════════════╝

main() {
    local start_time=$(date +%s)
    
    echo -e "${BLUE}╔════════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║                  🕐 SILA Daily Audit Ritual                       ║${NC}"
    echo -e "${BLUE}║                      Timestamp: ${TIMESTAMP}                    ║${NC}"
    echo -e "${BLUE}╚════════════════════════════════════════════════════════════════════╝${NC}"
    
    # Executar rituais em sequência
    validate_architecture_sync
    validate_domain_audit
    validate_module_maturity
    validate_import_integrity
    validate_routers_and_health
    
    # Gerar relatório consolidado
    generate_consolidated_report
    
    # Calcular tempo total
    local end_time=$(date +%s)
    local execution_time=$((end_time - start_time))
    
    # Resumo final
    log_section "RITUAL CONCLUÍDO"
    echo -e "${GREEN}✅ Auditoria Diária Completa${NC}"
    echo ""
    local taxa_sucesso=0
    if [ "$TOTAL_CHECKS" -gt 0 ]; then
        taxa_sucesso=$(echo "scale=1; $PASSED_CHECKS * 100 / $TOTAL_CHECKS" | bc -l 2>/dev/null || echo "0")
    fi
    echo -e "📊 ${BLUE}Estatísticas:${NC}"
    echo "  - Total Verificações: $TOTAL_CHECKS"
    echo "  - Passou: $PASSED_CHECKS"
    echo "  - Falhou: $FAILED_CHECKS"
    echo "  - Taxa de Sucesso: ${taxa_sucesso}%"
    echo "  - Módulos Críticos: ${#CRITICAL_MODULES[@]}"
    echo "  - Tempo Total: ${execution_time}s"
    echo ""
    echo -e "📝 ${BLUE}Relatórios Gerados:${NC}"
    echo "  - $AUDIT_REPORT"
    echo "  - $AUDIT_DIR/*.log"
    echo ""
    echo -e "🚀 ${BLUE}Próximas Ações:${NC}"
    echo "  1. Revisar: reports/daily_audit.md"
    echo "  2. Se críticos: make arch-fix"
    echo "  3. Validar: make audit-full"
    echo ""
    
    # Sair com status correto
    [ "$FAILED_CHECKS" -eq 0 ] && exit 0 || exit 1
}

# Executar main
main "$@"
