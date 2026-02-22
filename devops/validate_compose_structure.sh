#!/bin/bash
# devops/validate_compose_structure.sh
# ==============================================
# Script de validação completa do docker-compose.yml
# - Verifica estrutura YAML
# - Valida seção services:
# - Lista serviços encontrados
# - Valida com docker compose config
# - Sugere correções se necessário
# ==============================================

set -euo pipefail

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# Funções de log
log_info() { echo -e "${BLUE}ℹ️  $1${NC}"; }
log_success() { echo -e "${GREEN}✅ $1${NC}"; }
log_warning() { echo -e "${YELLOW}⚠️  $1${NC}"; }
log_error() { echo -e "${RED}❌ $1${NC}"; }
log_step() {
    echo ""
    echo -e "${CYAN}========================================${NC}"
    echo -e "${CYAN}$1${NC}"
    echo -e "${CYAN}========================================${NC}"
}

# Garantir que estamos no diretório correto
cd "$(dirname "$0")"

# FORÇAR uso do arquivo correto (devops/docker-compose.yml)
COMPOSE_FILE="../docker-compose.yml"
COMPOSE_PROFILES="infra backend"

# Verificar se arquivo existe
if [ ! -f "$COMPOSE_FILE" ]; then
    log_error "Arquivo $COMPOSE_FILE não encontrado!"
    log_info "Execute este script a partir do diretório devops/"
    exit 1
fi

log_info "Arquivo: $COMPOSE_FILE"
log_info "Profiles: $COMPOSE_PROFILES"

log_step "Validação do docker-compose.yml"

# ============================================
# 0. VERIFICAR CONFLITOS COM ARQUIVO DA RAIZ
# ============================================
ROOT_COMPOSE="$HOME/dev/sila-system/docker-compose.yml"
if [ -f "$ROOT_COMPOSE" ]; then
    log_warning "Arquivo docker-compose.yml encontrado na raiz do projeto!"
    log_info "Raiz: $ROOT_COMPOSE"
    log_info "Devops: $(pwd)/$COMPOSE_FILE"
    echo ""
    log_info "⚠️  IMPORTANTE: Sempre use '-f docker-compose.yml' para garantir que está usando o arquivo correto!"
    echo ""
fi

# ============================================
# 1. VALIDAR SINTAXE YAML
# ============================================
log_step "1. Validando sintaxe YAML"

if command -v python3 >/dev/null 2>&1; then
    log_info "Verificando sintaxe YAML com Python..."
    if python3 -c "
import yaml
import sys
try:
    with open('$COMPOSE_FILE', 'r') as f:
        yaml.safe_load(f)
    print('OK')
except yaml.YAMLError as e:
    print(f'ERROR: {e}')
    sys.exit(1)
except Exception as e:
    print(f'ERROR: {e}')
    sys.exit(1)
" 2>&1 | grep -q "OK"; then
        log_success "Sintaxe YAML válida"
    else
        log_error "Erro na sintaxe YAML"
        python3 -c "
import yaml
import sys
try:
    with open('$COMPOSE_FILE', 'r') as f:
        yaml.safe_load(f)
except yaml.YAMLError as e:
    print(f'Erro: {e}')
    sys.exit(1)
" 2>&1
        exit 1
    fi
else
    log_warning "Python3 não encontrado, pulando validação YAML"
fi

# ============================================
# 2. VERIFICAR SEÇÃO services:
# ============================================
log_step "2. Verificando seção 'services:'"

if ! grep -q "^services:" "$COMPOSE_FILE" && ! grep -q "^  services:" "$COMPOSE_FILE"; then
    log_error "Seção 'services:' não encontrada!"
    log_info "Adicione 'services:' no início do arquivo"
    exit 1
fi

log_success "Seção 'services:' encontrada"

# Verificar se há serviços dentro de services:
log_info "Procurando serviços definidos..."
SERVICES=$(grep -E "^\s{0,2}[a-zA-Z_-]+:" "$COMPOSE_FILE" | grep -v "^#" | grep -v "services:" | grep -v "networks:" | grep -v "volumes:" | grep -v "version:" | sed 's/://g' | sed 's/^[[:space:]]*//' | sort -u)

if [ -z "$SERVICES" ]; then
    log_error "Nenhum serviço encontrado dentro de 'services:'!"
    log_info "Verifique a indentação dos serviços"
    exit 1
fi

log_success "Serviços encontrados:"
for service in $SERVICES; do
    echo "  • $service"
done

# ============================================
# 3. VALIDAR INDENTAÇÃO
# ============================================
log_step "3. Validando indentação"

# Verificar se serviços estão com indentação correta (2 espaços)
log_info "Verificando indentação dos serviços..."
BAD_INDENT=$(grep -E "^\s{0,1}[a-zA-Z_-]+:" "$COMPOSE_FILE" | grep -v "^  " | grep -v "^#" | grep -v "services:" | grep -v "networks:" | grep -v "volumes:" | grep -v "version:" | head -5 || true)

if [ -n "$BAD_INDENT" ]; then
    log_warning "Possíveis problemas de indentação encontrados:"
    echo "$BAD_INDENT" | head -5
    log_info "Serviços devem ter 2 espaços de indentação"
else
    log_success "Indentação parece correta"
fi

# ============================================
# 4. VALIDAR COM docker compose config
# ============================================
log_step "4. Validando com 'docker compose config' (com profiles)"

log_info "Executando: docker compose -f $COMPOSE_FILE --profile infra --profile backend config"
if docker compose -f "$COMPOSE_FILE" --profile infra --profile backend config > /tmp/compose_validated.yml 2>&1; then
    log_success "docker compose config passou!"

    # Extrair serviços do arquivo validado (com profiles)
    log_info "Serviços reconhecidos pelo Docker Compose (com profiles):"
    docker compose -f "$COMPOSE_FILE" --profile infra --profile backend config --services | while read service; do
        echo "  • $service"
    done
else
    log_error "docker compose config falhou!"
    log_info "Erros encontrados:"
    docker compose -f "$COMPOSE_FILE" --profile infra --profile backend config 2>&1 | tail -20
    exit 1
fi

# ============================================
# 5. VERIFICAR ESTRUTURA ESPERADA
# ============================================
log_step "5. Verificando estrutura esperada"

EXPECTED_SERVICES=("db" "backend")
MISSING_SERVICES=()

for expected in "${EXPECTED_SERVICES[@]}"; do
    if docker compose -f "$COMPOSE_FILE" --profile infra --profile backend config --services | grep -q "^${expected}$"; then
        log_success "Serviço '$expected' encontrado"
    else
        log_warning "Serviço '$expected' não encontrado"
        MISSING_SERVICES+=("$expected")
    fi
done

# ============================================
# 6. VERIFICAR DEPENDÊNCIAS
# ============================================
log_step "6. Verificando dependências"

if docker compose -f "$COMPOSE_FILE" --profile infra --profile backend config --services | grep -q "^backend$"; then
    log_info "Verificando se backend depende de db..."
    if grep -A 5 "backend:" "$COMPOSE_FILE" | grep -q "depends_on:"; then
        if grep -A 10 "backend:" "$COMPOSE_FILE" | grep -A 5 "depends_on:" | grep -q "db:"; then
            log_success "Backend depende de 'db'"
        else
            log_warning "Backend não depende de 'db' explicitamente"
        fi
    else
        log_warning "Backend não tem 'depends_on' definido"
    fi
fi

# ============================================
# 7. VERIFICAR QUAL ARQUIVO ESTÁ SENDO USADO
# ============================================
log_step "7. Verificando arquivo em uso"

DB_PORT=$(docker compose -f "$COMPOSE_FILE" --profile infra --profile backend config 2>/dev/null | grep -A 5 "db:" | grep "ports:" -A 1 | grep -oE "[0-9]+:5432" | cut -d: -f1 | head -1 || echo "N/A")

if [ "$DB_PORT" = "5434" ]; then
    log_success "✅ Usando arquivo DEVOPS (porta DB: 5434)"
elif [ "$DB_PORT" = "5433" ]; then
    log_warning "⚠️  Usando arquivo RAIZ (porta DB: 5433) - Verifique se é isso que você quer!"
else
    log_info "Porta DB: $DB_PORT"
fi

# ============================================
# 8. RESUMO FINAL
# ============================================
log_step "8. Resumo Final"

echo ""
log_info "Estrutura do docker-compose.yml:"
echo ""
echo "📁 Arquivo: $COMPOSE_FILE"
echo "📊 Serviços encontrados: $(docker compose -f "$COMPOSE_FILE" --profile infra --profile backend config --services | wc -l)"
echo "🔌 Porta DB: $DB_PORT"
echo "🎯 Profiles: $COMPOSE_PROFILES"
echo ""

if [ ${#MISSING_SERVICES[@]} -eq 0 ]; then
    log_success "✅ Validação completa! Arquivo está correto."
    echo ""
    log_info "Você pode executar:"
    echo "  docker compose -f $COMPOSE_FILE --profile infra --profile backend up -d"
    echo "  # OU usar o script automatizado:"
    echo "  ./setup_backend_complete.sh"
    echo ""
else
    log_warning "⚠️  Alguns serviços esperados não foram encontrados"
    echo ""
    log_info "Serviços faltando: ${MISSING_SERVICES[*]}"
    echo ""
fi

# ============================================
# 9. SUGESTÕES DE CORREÇÃO (se necessário)
# ============================================
if [ ${#MISSING_SERVICES[@]} -gt 0 ] || [ -n "$BAD_INDENT" ]; then
    log_step "9. Sugestões de Correção"

    echo ""
    log_info "Estrutura correta esperada:"
    echo ""
    cat << 'EOF'
services:
  db:
    image: postgres:15
    container_name: sila-db
    # ... outras configurações

  backend:
    build: ./backend
    depends_on:
      - db
    # ... outras configurações
EOF
    echo ""
fi

echo ""
