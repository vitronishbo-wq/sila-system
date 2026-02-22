#!/bin/bash
# Script para equipe Backend

echo "⚙️ Iniciando ambiente Backend SILA"
COMPOSE_FILE="/opt/sila-system/devops/docker-compose.yml"

# Verificar portas necessárias
check_ports() {
    echo "🔍 Verificando portas..."
    if lsof -i :8000 > /dev/null || lsof -i :5434 > /dev/null; then
        echo "❌ Porta 8000 (API) ou 5434 (DB) já está em uso!"
        return 1
    fi
    return 0
}

# Backup do banco antes de qualquer operação
backup_database() {
    echo "💾 Criando backup do banco..."
    BACKUP_FILE="backups/sila_$(date +%Y%m%d_%H%M%S).sql"
    mkdir -p backups

    if docker compose -f "$COMPOSE_FILE" exec -T db pg_dump -U postgres sila > "$BACKUP_FILE" 2>/dev/null; then
        echo "✅ Backup criado em: $BACKUP_FILE"
        return 0
    else
        echo "⚠️ Backup não foi necessário - banco não existe ou está vazio"
        return 0
    fi
}

# Parar containers backend
stop_backend() {
    echo "🛑 Parando serviços backend..."
    docker compose -f "$COMPOSE_FILE" stop backend db || true
    docker compose -f "$COMPOSE_FILE" rm -f backend db || true
}

# Iniciar backend e banco
start_backend() {
    echo "🐘 Iniciando PostgreSQL..."
    docker compose -f "$COMPOSE_FILE" --profile infra up -d db

    echo "⏳ Aguardando PostgreSQL ficar pronto..."
    for i in {1..30}; do
        if docker compose -f "$COMPOSE_FILE" exec db pg_isready -U postgres > /dev/null 2>&1; then
            echo "✅ PostgreSQL está pronto!"
            break
        fi
        echo -n "."
        sleep 1
    done

    echo "🚀 Iniciando backend..."
    docker compose -f "$COMPOSE_FILE" --profile backend --profile infra up -d backend

    echo "⏳ Aguardando backend ficar pronto..."
    for i in {1..30}; do
        if curl -s http://localhost:8000/docs > /dev/null; then
            echo "✅ Backend está pronto!"
            return 0
        fi
        echo -n "."
        sleep 1
    done
    echo "❌ Timeout aguardando backend"
    return 1
}

# Aplicar migrações
run_migrations() {
    echo "📊 Aplicando migrações..."
    docker compose -f "$COMPOSE_FILE" exec -T backend alembic upgrade head
}

# Executar pipeline
main() {
    stop_backend
    check_ports || exit 1
    backup_database
    start_backend
    run_migrations

    echo "📝 Status final:"
    docker compose -f "$COMPOSE_FILE" ps backend db
    echo "🔗 Backend API disponível em: http://localhost:8000"
    echo "📚 Documentação API: http://localhost:8000/docs"
}

main
