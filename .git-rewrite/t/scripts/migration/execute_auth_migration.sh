#!/bin/bash

# ============================================================================
# IMPORTAR BIBLIOTECAS COMUNS
# ============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/../lib/colors.sh"
source "$SCRIPT_DIR/../lib/logging.sh"

# Função para verificar status do último comando
check_status() {
    if [ $? -eq 0 ]; then
        success "$1"
        return 0
    else
        error "$1 falhou!"
        return 1
    fi
}

# Aliases para compatibilidade
warning() {
    warn "$1"
}

# Função para detectar o arquivo docker-compose correto
detect_docker_compose() {
    local env_type="development"

    if [ -f "infrastructure/docker/docker-compose.yml" ]; then
        DOCKER_COMPOSE_FILE="infrastructure/docker/docker-compose.yml"

        if [ -f "infrastructure/docker/docker-compose.override.yml" ]; then
            DOCKER_COMPOSE_FILE="-f infrastructure/docker/docker-compose.yml -f infrastructure/docker/docker-compose.override.yml"
        fi

        if [ "$ENVIRONMENT" = "production" ] && [ -f "docker-compose.yml" ]; then
            DOCKER_COMPOSE_FILE="-f docker-compose.yml"
            env_type="production"
        elif [ "$ENVIRONMENT" = "staging" ] && [ -f "infrastructure/docker/docker-compose.staging.yml" ]; then
            DOCKER_COMPOSE_FILE="-f infrastructure/docker/docker-compose.yml -f infrastructure/docker/docker-compose.staging.yml"
            env_type="staging"
        fi
    else
        error "Arquivo infrastructure/docker/docker-compose.yml não encontrado!"
        exit 1
    fi

    log "🔧 Usando configuração para ambiente: $env_type"
    export DOCKER_COMPOSE_FILE
}

# Usar arquivo de migração específico se existir, senão usar fallback
if [ -f "infrastructure/docker/docker-compose.migration.yml" ]; then
    DOCKER_COMPOSE_FILE="-f infrastructure/docker/docker-compose.migration.yml"
else
    warning "Arquivo infrastructure/docker/docker-compose.migration.yml não encontrado, usando fallback infrastructure/docker/docker-compose.yml"
    DOCKER_COMPOSE_FILE="-f infrastructure/docker/docker-compose.yml"
fi

# Carregar variáveis de ambiente do .env e sanear valores
if [ -f ".env" ]; then
    # Ler .env linha a linha e exportar de forma segura apenas chaves válidas
    while IFS='=' read -r key value || [ -n "$key" ]; do
        # Ignorar comentários e linhas vazias
        if [[ -z "$key" || "$key" =~ ^# ]]; then
            continue
        fi

        # Trim spaces around key and value
        key=$(echo "$key" | xargs)
        value=$(echo "${value:-}" | sed -e 's/^\s*//g' -e 's/\s*$//g')

        # Remove surrounding quotes and square brackets but keep commas
        value=$(echo "$value" | sed -e 's/^"//' -e 's/"$//' -e "s/^'//" -e "s/'$//" -e 's/^\[//' -e 's/\]$//')

        # Exportar variáveis conhecidas explicitamente para evitar quebras por caracteres estranhos
        case "$key" in
            ASYNC_DATABASE_URL|DATABASE_URL|TEST_DATABASE_URL|SECRET_KEY|ALGORITHM|ACCESS_TOKEN_EXPIRE_MINUTES|ENVIRONMENT|DEBUG|DATABASE_ECHO|ALLOWED_ORIGINS|BACKEND_CORS_ORIGINS|LOG_LEVEL|POSTGRES_*|POSTGRES*|BACKUP_*|REDIS_*|MINIO_*|REACT_APP_*|PYTHON*|PROJECT_NAME)
                export "$key=$value"
                ;;
            *)
                # Exportar outras variáveis sem espaços problemáticos
                export "$key=$value" 2>/dev/null || true
                ;;
        esac
    done < .env
else
    error "Arquivo .env não encontrado!"
    exit 1
fi

# Definir variáveis padrão se não existirem
POSTGRES_USER=${POSTGRES_USER:-postgres}
POSTGRES_DB=${POSTGRES_DB:-sila_dev}
POSTGRES_PASSWORD=${POSTGRES_PASSWORD:-postgres}
POSTGRES_PORT=5434  # Nova porta para migração
export POSTGRES_PORT

# 1. Limpeza completa do ambiente Docker
log "🧹 Realizando limpeza do ambiente Docker..."

# Parar todos os containers relacionados
docker-compose $DOCKER_COMPOSE_FILE down --remove-orphans 2>/dev/null || true

# Remover containers órfãos e networks não utilizadas
log "�️ Removendo containers órfãos e networks..."
docker container prune -f
docker network prune -f

# Verificar e matar processos na porta original (5432) e nova (5434)
for port in 5432 5434; do
    pid=$(lsof -t -i:$port 2>/dev/null)
    if [ ! -z "$pid" ]; then
        log "🔄 Liberando porta $port (PID: $pid)..."
        kill -9 $pid 2>/dev/null || true
    fi
done

# Aguardar um momento para garantir que as portas foram liberadas
sleep 2

# 2. Iniciar e verificar PostgreSQL
log "🚀 Iniciando PostgreSQL na porta 5434..."
export POSTGRES_PORT=5434  # Atualizar porta para ambiente de migração
docker-compose $DOCKER_COMPOSE_FILE up -d db

# Aguardar PostgreSQL iniciar
log "⏳ Aguardando PostgreSQL inicializar..."
for i in {1..30}; do
    if docker-compose $DOCKER_COMPOSE_FILE exec -T db pg_isready -U ${POSTGRES_USER:-postgres} -h localhost -p 5432 >/dev/null 2>&1; then
        log "✅ PostgreSQL está pronto!"

        # Aguardar um pouco mais para o banco inicializar completamente
        sleep 5

        # Verificar conexão com dados corretos
        if docker-compose $DOCKER_COMPOSE_FILE exec -T db bash -c "PGPASSWORD=${POSTGRES_PASSWORD:-postgres} psql -U ${POSTGRES_USER:-postgres} -d ${POSTGRES_DB:-sila_db} -c 'SELECT 1'" >/dev/null 2>&1; then
            log "✅ Conexão com banco de dados verificada!"
            break
        else
            log "⚠️ Tentando criar o banco de dados..."
            docker-compose $DOCKER_COMPOSE_FILE exec -T db bash -c "PGPASSWORD=${POSTGRES_PASSWORD:-postgres} createdb -U ${POSTGRES_USER:-postgres} ${POSTGRES_DB:-sila_db}" >/dev/null 2>&1
            if [ $? -eq 0 ]; then
                log "✅ Banco de dados criado com sucesso!"
                # Criar extensão pgcrypto
                log "🔐 Instalando extensão pgcrypto..."
                docker-compose $DOCKER_COMPOSE_FILE exec -T db bash -c "PGPASSWORD=${POSTGRES_PASSWORD:-postgres} psql -U ${POSTGRES_USER:-postgres} -d ${POSTGRES_DB:-sila_db} -c 'CREATE EXTENSION IF NOT EXISTS pgcrypto;'" >/dev/null 2>&1
                if [ $? -eq 0 ]; then
                    log "✅ Extensão pgcrypto instalada com sucesso!"
                else
                    error "❌ Falha ao instalar extensão pgcrypto"
                    docker-compose $DOCKER_COMPOSE_FILE logs db
                    exit 1
                fi
                break
            else
                error "❌ Falha na criação do banco de dados"
                docker-compose $DOCKER_COMPOSE_FILE logs db
                exit 1
            fi
        fi
    fi
    if [ $i -eq 30 ]; then
        error "❌ Timeout aguardando PostgreSQL inicializar"
        docker-compose $DOCKER_COMPOSE_FILE logs db
        exit 1
    fi
    sleep 1
done

# 3. Criar backup
log "📦 Criando backup do banco de dados..."
BACKUP_DIR="backups"
mkdir -p $BACKUP_DIR
BACKUP_FILE="$BACKUP_DIR/db_backup_$(date +%Y%m%d_%H%M%S).sql"

log "🔍 Executando backup..."
if docker-compose $DOCKER_COMPOSE_FILE ps -q db 2>/dev/null; then
    log "✅ PostgreSQL já está rodando, executando backup..."
    docker-compose $DOCKER_COMPOSE_FILE exec -T db pg_dump -U ${POSTGRES_USER:-postgres} ${POSTGRES_DB:-postgres} > "$BACKUP_FILE" 2>/tmp/pg_dump.error
    if [ $? -ne 0 ]; then
        error "❌ Falha no backup: $(cat /tmp/pg_dump.error)"
        exit 1
    fi
else
    log "🚀 Iniciando PostgreSQL temporariamente..."
    docker-compose $DOCKER_COMPOSE_FILE up -d db

    # Aguardar PostgreSQL iniciar
    log "⏳ Aguardando PostgreSQL inicializar..."
    for i in {1..30}; do
        if docker-compose $DOCKER_COMPOSE_FILE exec -T db pg_isready -U ${POSTGRES_USER:-postgres} >/dev/null 2>&1; then
            log "✅ PostgreSQL está pronto!"
            break
        fi
        if [ $i -eq 30 ]; then
            error "❌ Timeout aguardando PostgreSQL inicializar"
            exit 1
        fi
        sleep 1
    done

    # Tentar backup
    log "📦 Executando backup..."
    docker-compose $DOCKER_COMPOSE_FILE exec -T db pg_dump -U ${POSTGRES_USER:-postgres} ${POSTGRES_DB:-postgres} > "$BACKUP_FILE" 2>/tmp/pg_dump.error
    if [ $? -ne 0 ]; then
        error "❌ Falha no backup: $(cat /tmp/pg_dump.error)"
        exit 1
    fi
fi
check_status "Backup do banco de dados" || exit 1

# 3. Criar e configurar ambiente virtual Python
log "🔧 Criando ambiente virtual Python..."
python3 -m venv .venv
source .venv/bin/activate

# Instalar dependências Python necessárias
log "📦 Instalando dependências Python..."
pip install bcrypt psycopg2-binary
check_status "Instalação de dependências" || exit 1

# 4. Executar migração de senhas em modo de teste
log "🔑 Executando migração de senhas em modo de teste..."
python3 tools/migration/migrate_user_passwords.py --test-mode --batch-size 10
check_status "Teste de migração de senhas" || exit 1

# 5. Solicitar confirmação para continuar
read -p "Continuar com a migração em produção? (s/N) " response
if [[ ! "$response" =~ ^[Ss]$ ]]; then
    warning "Migração cancelada pelo usuário"
    exit 0
fi

# 6. Executar migração de senhas em produção
log "🔐 Executando migração de senhas em produção..."
python3 tools/migration/migrate_user_passwords.py --batch-size 100
check_status "Migração de senhas em produção" || exit 1

# 7. Iniciar serviços
log "🚀 Iniciando serviços..."
docker-compose $DOCKER_COMPOSE_FILE up -d
check_status "Inicialização dos serviços" || exit 1

# 8. Verificar logs por erros
log "📋 Verificando logs por erros..."
# Aguardar backend inicializar
log "⏳ Aguardando backend inicializar..."
for i in {1..30}; do
    if curl -s -o /dev/null -w "%{http_code}" http://localhost:3000/docs > /dev/null 2>&1; then
        log "✅ Backend está pronto!"
        break
    fi
    if [ $i -eq 30 ]; then
        error "❌ Timeout aguardando backend inicializar"
        exit 1
    fi
    sleep 2
done

docker-compose $DOCKER_COMPOSE_FILE logs --tail=100 > service_logs.txt

# Verificar erros críticos
CRITICAL_ERRORS=$(grep -i "critical\|fatal\|panic" service_logs.txt || true)
if [ ! -z "$CRITICAL_ERRORS" ]; then
    error "⚠️ Erros críticos encontrados:"
    echo "$CRITICAL_ERRORS"
    warning "Verifique service_logs.txt para mais detalhes"
else
    # Verificar outros erros
    OTHER_ERRORS=$(grep -i "error\|exception\|failed" service_logs.txt || true)
    if [ ! -z "$OTHER_ERRORS" ]; then
        warning "Encontrados possíveis erros nos logs. Verifique service_logs.txt"
    else
        success "Nenhum erro encontrado nos logs iniciais"
    fi
fi

# Verificar status dos serviços
log "🔍 Verificando status dos serviços..."
docker-compose $DOCKER_COMPOSE_FILE ps > services_status.txt
if grep -i "exit" services_status.txt; then
    error "Alguns serviços podem ter falhado ao iniciar. Verifique services_status.txt"
else
    success "Todos os serviços parecem estar rodando corretamente"
fi

# 9. Testar endpoint de autenticação
log "🔒 Testando endpoint de autenticação..."
curl -s -o /dev/null -w "%{http_code}" http://localhost:3000/api/auth/test
if [ $? -eq 200 ]; then
    success "Endpoint de autenticação respondendo corretamente"
else
    warning "Endpoint de autenticação pode ter problemas. Verifique manualmente."
fi

# Relatório final
log "\n📑 Relatório Final de Migração:"
echo "----------------------------------------"
echo "1. Backup do banco: $BACKUP_FILE"
echo "2. Log de migração: Verifique password_migration_*.log"
echo "3. Estatísticas: password_migration_stats.json"
echo "4. Logs dos serviços: service_logs.txt"
echo "----------------------------------------"

success "Processo de migração concluído!"
echo -e "${YELLOW}Por favor, teste o login manualmente antes de liberar para todos os usuários.${NC}"
