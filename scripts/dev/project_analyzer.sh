#!/bin/bash
# =============================================================================
# SILA Project Analyzer - Versão 3.0
# =============================================================================
# Script robusto para análise da estrutura atual do projeto
# =============================================================================

set -euo pipefail

# Cores para output
readonly GREEN='\033[0;32m'
readonly BLUE='\033[0;34m'
readonly YELLOW='\033[1;33m'
readonly RED='\033[0;31m'
readonly CYAN='\033[0;36m'
readonly NC='\033[0m'

# Configurações
readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly PROJECT_ROOT="$SCRIPT_DIR"
readonly OUTPUT_DIR="$PROJECT_ROOT/.project_analysis"
readonly TIMESTAMP=$(date +%Y%m%d_%H%M%S)
readonly DEFAULT_OUTPUT_FILE="$OUTPUT_DIR/project_analysis_$TIMESTAMP.md"

# Criar diretório de saída
mkdir -p "$OUTPUT_DIR"

# Funções de log
log() {
    local level=$1
    shift
    local message="$*"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')

    case $level in
        "INFO") color=$BLUE; prefix="ℹ️" ;;
        "SUCCESS") color=$GREEN; prefix="✅" ;;
        "WARNING") color=$YELLOW; prefix="⚠️" ;;
        "ERROR") color=$RED; prefix="❌" ;;
        "STEP") color=$CYAN; prefix="🔄" ;;
    esac

    echo -e "${color}${prefix} [${timestamp}] ${message}${NC}"
}

# Analisar estrutura do projeto
analyze_project_structure() {
    local output_file=$1

    log "STEP" "Analisando estrutura do projeto..."

    echo "# SILA Project Analysis - $(date)" > "$output_file"
    echo "## 📁 Estrutura de Diretórios" >> "$output_file"
    echo '```' >> "$output_file"
    tree -L 3 -I "node_modules|venv|.cache|.git" >> "$output_file" 2>/dev/null || echo "[tree command not available]" >> "$output_file"
    echo '```' >> "$output_file"

    log "SUCCESS" "Estrutura de diretórios analisada"
}

# Estatísticas do projeto
calculate_project_stats() {
    local output_file=$1

    log "STEP" "Calculando estatísticas do projeto..."

    echo "" >> "$output_file"
    echo "## 📊 Estatísticas do Projeto" >> "$output_file"

    declare -A stats=(
        ["Python"]="$(find . -name "*.py" -not -path "*/node_modules/*" -not -path "*/venv/*" | wc -l)"
        ["TypeScript/JavaScript"]="$(find . -name "*.ts" -o -name "*.tsx" -o -name "*.js" -o -name "*.jsx" -not -path "*/node_modules/*" -not -path "*/venv/*" | wc -l)"
        ["Config Files"]="$(find . -name "*.yml" -o -name "*.yaml" -o -name "*.json" -o -name "*.toml" -not -path "*/node_modules/*" -not -path "*/venv/*" | wc -l)"
        ["Markdown"]="$(find . -name "*.md" -not -path "*/node_modules/*" -not -path "*/venv/*" | wc -l)"
        ["Shell Scripts"]="$(find . -name "*.sh" -not -path "*/node_modules/*" -not -path "*/venv/*" | wc -l)"
        ["Docker Files"]="$(find . -name "Dockerfile*" -o -name "docker-compose*.yml" -not -path "*/node_modules/*" -not -path "*/venv/*" | wc -l)"
    )

    for key in "${!stats[@]}"; do
        echo "- **${key}:** ${stats[$key]}" >> "$output_file"
    done

    log "SUCCESS" "Estatísticas calculadas"
}

# Verificar serviços principais
check_core_services() {
    local output_file=$1

    log "STEP" "Verificando serviços principais..."

    echo "" >> "$output_file"
    echo "## 🚀 Serviços Principais" >> "$output_file"

    # Backend
    if [ -f "backend/Dockerfile" ]; then
        echo "- ✅ **Backend:** Dockerfile encontrado" >> "$output_file"

        # Verificar entrypoint
        if [ -f "backend/entrypoint.sh" ]; then
            echo "  - ✅ entrypoint.sh encontrado" >> "$output_file"

            # Verificar funcionalidades do entrypoint
            grep -q "wait_for_db" "backend/entrypoint.sh" && \
                echo "    - ✅ Contém wait_for_db" >> "$output_file" || \
                echo "    - ⚠️ Falta wait_for_db" >> "$output_file"

            grep -q "alembic" "backend/entrypoint.sh" && \
                echo "    - ✅ Contém migrações Alembic" >> "$output_file" || \
                echo "    - ⚠️ Falta migrações Alembic" >> "$output_file"
        else
            echo "  - ⚠️ entrypoint.sh não encontrado" >> "$output_file"
        fi
    else
        echo "- ⚠️ **Backend:** Dockerfile não encontrado" >> "$output_file"
    fi

    # Frontend
    if [ -f "frontend/Dockerfile" ]; then
        echo "- ✅ **Frontend:** Dockerfile encontrado" >> "$output_file"
    else
        echo "- ⚠️ **Frontend:** Dockerfile não encontrado" >> "$output_file"
    fi

    # Docker Compose
    if [ -f "docker-compose.yml" ]; then
        echo "- ✅ **Docker Compose:** arquivo principal encontrado" >> "$output_file"

        # Verificar arquivos adicionais
        compose_files=(
            "docker-compose.prod.yml"
            "docker-compose.staging.yml"
            "docker-compose.dev.yml"
        )

        for file in "${compose_files[@]}"; do
            if [ -f "$file" ]; then
                echo "  - ✅ $file encontrado" >> "$output_file"
            else
                echo "  - ⚠️ $file não encontrado" >> "$output_file"
            fi
        done
    else
        echo "- ❌ **Docker Compose:** arquivo principal não encontrado" >> "$output_file"
    fi

    log "SUCCESS" "Serviços principais verificados"
}

# Verificar arquivos de configuração
check_config_files() {
    local output_file=$1

    log "STEP" "Verificando arquivos de configuração..."

    echo "" >> "$output_file"
    echo "## ⚙️ Arquivos de Configuração" >> "$output_file"

    # Verificar .env files
    env_files=(
        ".env"
        ".env.development"
        ".env.production"
        ".env.staging"
    )

    for file in "${env_files[@]}"; do
        if [ -f "$file" ]; then
            echo "- ✅ $file encontrado" >> "$output_file"
            # Verificar se não está vazio
            if [ -s "$file" ]; then
                echo "  - ✅ Contém configurações" >> "$output_file"
            else
                echo "  - ⚠️ Arquivo vazio" >> "$output_file"
            fi
        else
            echo "- ⚠️ $file não encontrado" >> "$output_file"
        fi
    done

    log "SUCCESS" "Arquivos de configuração verificados"
}

# Analisar volumes Docker
analyze_docker_volumes() {
    local output_file=$1

    log "STEP" "Analisando configurações de volume..."

    echo "" >> "$output_file"
    echo "## 💾 Volumes Docker" >> "$output_file"

    if [ -f "docker-compose.yml" ]; then
        volumes=$(grep -E "^\s+volumes:" -A 10 "docker-compose.yml" || true)

        if [ -n "$volumes" ]; then
            echo "- Volumes definidos no docker-compose.yml:" >> "$output_file"
            echo '```yaml' >> "$output_file"
            echo "$volumes" >> "$output_file"
            echo '```' >> "$output_file"

            # Verificar boas práticas
            if echo "$volumes" | grep -q ".env"; then
                echo "  - ✅ .env montado corretamente" >> "$output_file"
            else
                echo "  - ⚠️ .env não está sendo montado" >> "$output_file"
            fi

            if echo "$volumes" | grep -q "prometheus_data"; then
                echo "  - ✅ Volume prometheus_data definido" >> "$output_file"
            else
                echo "  - ⚠️ Volume prometheus_data não encontrado" >> "$output_file"
            fi
        else
            echo "- ⚠️ Nenhum volume definido no docker-compose.yml" >> "$output_file"
        fi
    fi

    log "SUCCESS" "Configurações de volume analisadas"
}

# Main
main() {
    local output_file="$DEFAULT_OUTPUT_FILE"

    echo ""
    log "INFO" "Iniciando análise do projeto SILA"
    log "INFO" "Saída será salva em: $output_file"

    # Executar todas as análises
    analyze_project_structure "$output_file"
    calculate_project_stats "$output_file"
    check_core_services "$output_file"
    check_config_files "$output_file"
    analyze_docker_volumes "$output_file"

    # Resumo final
    echo "" >> "$output_file"
    echo "## 📝 Resumo da Análise" >> "$output_file"
    echo "- Data: $(date)" >> "$output_file"
    echo "- Diretório analisado: $PROJECT_ROOT" >> "$output_file"

    log "SUCCESS" "Análise concluída com sucesso!"
    log "INFO" "Arquivo de saída: $output_file"

    # Mostrar caminho completo para o usuário
    echo ""
    echo "═══════════════════════════════════════════════════"
    echo -e "${GREEN}✅ Análise do projeto concluída!${NC}"
    echo "Arquivo gerado: $(realpath "$output_file")"
    echo "═══════════════════════════════════════════════════"
    echo ""
}

main "$@"
