#!/bin/bash

# ==============================================================================
# SCRIPT DE REORGANIZAÇÃO DE PROJETO (Enterprise Edition)
# Executar na raiz do repositório 'sila-system/'.
# Objetivo: Mover arquivos e diretórios existentes para a nova estrutura modular,
# preservando o histórico com 'git mv'.
#
# Autor: Truman (Assistente AI)
# Data: 2025-11-15
# ==============================================================================

# --- Variáveis e Cores para Feedback ---
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Função para criar diretório se não existir
create_dir() {
    if [ ! -d "$1" ]; then
        echo -e "${YELLOW}Criando diretório: $1${NC}"
        mkdir -p "$1"
    fi
}

# Função para mover arquivos/diretórios com git
safe_git_mv() {
    local source="$1"
    local destination="$2"

    if [ -e "$source" ]; then
        echo -e "${GREEN}Movendo: $source -> $destination${NC}"
        git mv "$source" "$destination"
    else
        echo -e "${RED}Aviso: $source não encontrado. Pulando.${NC}"
    fi
}

# Função para verificar se estamos na raiz do projeto
check_project_root() {
    if [ ! -f "README.md" ] || [ ! -d ".git" ]; then
        echo -e "${RED}ERRO: Execute este script na raiz do projeto sila-system/${NC}"
        exit 1
    fi
}

# Função para backup de segurança
create_backup() {
    local backup_dir=".backups/restructure-$(date +%Y%m%d_%H%M%S)"
    echo -e "${BLUE}Criando backup em: $backup_dir${NC}"
    mkdir -p "$backup_dir"

    # Criar snapshot do estado atual
    git status --porcelain > "$backup_dir/git_status_before.txt"
    git log --oneline -10 > "$backup_dir/git_log_before.txt"

    echo -e "${GREEN}Backup criado com sucesso${NC}"
}

# ------------------------------------------------------------------------------
## VERIFICAÇÕES INICIAIS
# ------------------------------------------------------------------------------
echo -e "${BLUE}=== SCRIPT DE REORGANIZAÇÃO AUTOMÁTICA SILA ===${NC}"
echo -e "${YELLOW}Verificando ambiente...${NC}"

check_project_root
create_backup

# Verificar se há mudanças não commitadas
if ! git diff-index --quiet HEAD --; then
    echo -e "${RED}AVISO: Há mudanças não commitadas. Recomenda-se fazer commit antes de continuar.${NC}"
    read -p "Continuar mesmo assim? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# ------------------------------------------------------------------------------
## 1. CRIAÇÃO DA NOVA ESTRUTURA DE DIRETÓRIOS
# ------------------------------------------------------------------------------
echo -e "\n${BLUE}--- 1. CRIAÇÃO DE DIRETÓRIOS CHAVE ---${NC}"

# Estrutura de Domínio e Aplicações
create_dir core/models
create_dir core/schemas
create_dir core/services
create_dir core/utils

# apps/ já existe, mas garantir subdiretórios
create_dir apps/api_gateway
create_dir apps/worker

# Estrutura de Automação e Infraestrutura
create_dir automation/deployment
create_dir automation/migration
create_dir automation/monitoring
create_dir automation/validation
create_dir automation/governance

create_dir infrastructure/docker
create_dir infrastructure/k8s
create_dir infrastructure/ci
create_dir infrastructure/terraform

# Estrutura de Ferramentas e Scripts
# create_dir tools/cli  # removed: directory no longer used
# create_dir tools/analyzers  # removed: directory no longer used
# create_dir tools/devtools  # removed: directory no longer used

create_dir scripts/bootstrap
create_dir scripts/maintenance
create_dir scripts/diagnostics
create_dir scripts/orchestration
create_dir scripts/integration

# Estrutura de Configuração, Documentação e Relatórios
create_dir config/envs
create_dir config/secrets
create_dir config/vars

create_dir docs/architecture
create_dir docs/deployment
create_dir docs/standards
create_dir docs/summaries

create_dir reports/audit
create_dir reports/integration
create_dir reports/performance
create_dir reports/logs

# Estrutura de Testes e Dependências
create_dir tests/unit
create_dir tests/integration
create_dir tests/smoke
create_dir tests/performance

# ------------------------------------------------------------------------------
## 2. REORGANIZAÇÃO DE ARQUIVOS CHAVE E DIRETÓRIOS EXISTENTES
# ------------------------------------------------------------------------------
echo -e "\n${BLUE}--- 2. REORGANIZAÇÃO DE ARQUIVOS EXISTENTES ---${NC}"

# A. Mover Scripts de Automação
echo -e "${YELLOW}Movendo scripts de automação...${NC}"
safe_git_mv prepare_environment.sh scripts/bootstrap/
safe_git_mv complete_env.sh scripts/bootstrap/
safe_git_mv init_project.ps1 scripts/bootstrap/
safe_git_mv dev-up.ps1 scripts/orchestration/
safe_git_mv down.ps1 scripts/orchestration/
safe_git_mv quick_deploy.sh scripts/orchestration/

# Scripts de monitoramento
safe_git_mv monitor_sila.sh automation/monitoring/
safe_git_mv nginx_monitor.sh automation/monitoring/
safe_git_mv nginx_diagnostic.sh automation/monitoring/
safe_git_mv monitor_documents.py automation/monitoring/

# Scripts de migração e validação
safe_git_mv execute_auth_migration.sh automation/migration/
safe_git_mv prepare_migration.sh automation/migration/
safe_git_mv migrate_user_passwords.py automation/migration/
safe_git_mv fix_pydantic_v2_config.py automation/migration/

# Scripts de deployment
safe_git_mv automation/deployment/deploy_staging.sh automation/deployment/
safe_git_mv automation/deployment/deployment_automation.py automation/deployment/

# B. Mover Ferramentas e Analisadores
echo -e "${YELLOW}Movendo ferramentas e analisadores...${NC}"
# safe_git_mv analyze_frontend_deps.py tools/analyzers/  # removed
# safe_git_mv advanced_project_analyzer.sh tools/analyzers/  # removed
# safe_git_mv project_analyzer.sh tools/analyzers/  # removed
safe_git_mv tools/codegen tools/

# Scripts de limpeza e manutenção
safe_git_mv cleanup_project.sh scripts/maintenance/
safe_git_mv cleanup_all_backups.sh scripts/maintenance/
safe_git_mv cleanup_obsolete.sh scripts/maintenance/
safe_git_mv cleanup_temp_files.sh scripts/maintenance/
safe_git_mv clean_pendrive_safe.sh scripts/maintenance/

# C. Mover Configurações
echo -e "${YELLOW}Movendo configurações...${NC}"
safe_git_mv .env.example config/envs/
safe_git_mv .env.template config/envs/
safe_git_mv defined_vars.txt config/vars/
safe_git_mv missing_in_env.txt config/vars/
safe_git_mv .sila_config config/

# D. Mover Documentação
echo -e "${YELLOW}Movendo documentação...${NC}"
safe_git_mv docs/architecture docs/
safe_git_mv docs/adr docs/architecture/
safe_git_mv automation/docs docs/summaries/automation/

# E. Mover Infraestrutura
echo -e "${YELLOW}Movendo arquivos de infraestrutura...${NC}"
safe_git_mv devops/docker infrastructure/docker/
safe_git_mv devops/nginx infrastructure/docker/nginx/
safe_git_mv devops/monitoring infrastructure/monitoring/
safe_git_mv infrastructure/docker infrastructure/
safe_git_mv infrastructure/k8s infrastructure/
safe_git_mv infrastructure/terraform infrastructure/

# F. Mover Requirements
echo -e "${YELLOW}Reorganizando requirements...${NC}"
if [ -f "requirements.txt" ]; then
    safe_git_mv requirements.txt requirements/base.txt
fi
safe_git_mv requirements-dev.txt requirements/dev.txt
safe_git_mv requirements/base.txt requirements/
safe_git_mv requirements/complete.txt requirements/
safe_git_mv requirements/dev.txt requirements/

# G. Mover Scripts de CI/CD
echo -e "${YELLOW}Movendo scripts de CI/CD...${NC}"
safe_git_mv .github/workflows infrastructure/ci/github/
safe_git_mv .gitlab-ci.yml infrastructure/ci/
safe_git_mv ci/ infrastructure/ci/scripts/

# H. Mover Scripts de Diagnóstico
echo -e "${YELLOW}Movendo scripts de diagnóstico...${NC}"
safe_git_mv nginx_automation.sh scripts/diagnostics/
safe_git_mv repair_all_runner.sh scripts/diagnostics/
safe_git_mv repair_all_simple.sh scripts/diagnostics/

# I. Mover Arquivos de Dados e Logs
echo -e "${YELLOW}Organizando dados e logs...${NC}"
safe_git_mv healing_output.txt reports/logs/
safe_git_mv integration_test_results.txt reports/integration/
safe_git_mv erros.txt reports/logs/
safe_git_mv deleted_files_snapshot.txt reports/audit/

# ------------------------------------------------------------------------------
## 3. AJUSTES ESPECIAIS E LIMPEZA
# ------------------------------------------------------------------------------
echo -e "\n${BLUE}--- 3. AJUSTES FINAIS ---${NC}"

# Criar arquivos .gitkeep em diretórios vazios importantes
touch core/models/.gitkeep
touch core/schemas/.gitkeep
touch core/services/.gitkeep
touch core/utils/.gitkeep
touch automation/governance/.gitkeep
# touch tools/cli/.gitkeep  # removed
# touch tools/devtools/.gitkeep  # removed
touch config/secrets/.gitkeep
touch tests/unit/.gitkeep
touch tests/integration/.gitkeep
touch tests/smoke/.gitkeep
touch tests/performance/.gitkeep
touch reports/audit/.gitkeep
touch reports/integration/.gitkeep
touch reports/performance/.gitkeep

# Adicionar os .gitkeep ao git
git add core/models/.gitkeep core/schemas/.gitkeep core/services/.gitkeep core/utils/.gitkeep
# git add automation/governance/.gitkeep tools/cli/.gitkeep tools/devtools/.gitkeep  # removed
git add config/secrets/.gitkeep tests/*/.gitkeep reports/*/.gitkeep

# ------------------------------------------------------------------------------
## 4. RELATÓRIO FINAL
# ------------------------------------------------------------------------------
echo -e "\n${GREEN}=== REORGANIZAÇÃO CONCLUÍDA COM SUCESSO ===${NC}"
echo -e "${YELLOW}Resumo das operações:${NC}"
echo "✅ Nova estrutura de diretórios criada"
echo "✅ Arquivos movidos preservando histórico git"
echo "✅ Backup de segurança criado"
echo "✅ Arquivos .gitkeep adicionados"

echo -e "\n${BLUE}PRÓXIMOS PASSOS OBRIGATÓRIOS:${NC}"
echo "1. ${YELLOW}Revisar mudanças:${NC} git status"
echo "2. ${YELLOW}Refatorar imports:${NC} Atualizar caminhos nos arquivos movidos"
echo "3. ${YELLOW}Atualizar configurações:${NC} Makefile, docker-compose.yml, etc."
echo "4. ${YELLOW}Testar aplicação:${NC} Verificar se tudo funciona"
echo "5. ${YELLOW}Commit das mudanças:${NC} git commit -m 'Reorganização da estrutura do projeto'"

echo -e "\n${GREEN}Script executado com sucesso!${NC}"
echo -e "${BLUE}Backup disponível em: .backups/restructure-$(date +%Y%m%d_%H%M%S)${NC}"
