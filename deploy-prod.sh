#!/bin/bash
# ========================================
# SILA System - Production Deployment Script
# ========================================

set -e

echo "🇦🇴 SILA System - Iniciando Deploy de Produção..."

# Check if .env.prod exists
if [ ! -f "./apps/backend/.env.prod" ]; then
    echo "❌ Erro: .env.prod não encontrado!"
    echo "Por favor, copie .env.prod.example para .env.prod e configure as variáveis."
    exit 1
fi

# Create necessary directories
echo "📁 Criando diretórios necessários..."
mkdir -p ./backups
mkdir -p ./certs
mkdir -p ./nginx

# Pull latest images
echo "📦 Baixando imagens base..."
docker compose -f docker-compose.prod.yml pull db redis nginx

# Build custom images
echo "🔨 Construindo imagens personalizadas..."
docker compose -f docker-compose.prod.yml build --no-cache

# Stop existing containers
echo "🛑 Parando containers existentes..."
docker compose -f docker-compose.prod.yml down

# Start services
echo "🚀 Iniciando serviços..."
docker compose -f docker-compose.prod.yml up -d

# Wait for database
echo "⏳ Aguardando inicialização do banco de dados..."
sleep 10

# Run migrations
echo "📊 Executando migrações..."
docker compose -f docker-compose.prod.yml exec -T backend alembic upgrade head

# Check health
echo "🏥 Verificando saúde dos serviços..."
sleep 5
docker compose -f docker-compose.prod.yml ps

echo ""
echo "✅ Deploy concluído com sucesso!"
echo ""
echo "📊 Status dos serviços:"
docker compose -f docker-compose.prod.yml ps
echo ""
echo "🌐 Sistema disponível em: http://localhost"
echo "📡 API disponível em: http://localhost/api/v1"
echo ""
echo "🇦🇴 SILA System operacional - Servindo a República de Angola!"
