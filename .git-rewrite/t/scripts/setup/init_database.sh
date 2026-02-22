#!/bin/bash
# Script para inicializar o banco de dados SILA System

echo "🚀 Inicializando banco de dados SILA System..."

# Parar containers se estiverem rodando
echo "📦 Parando containers..."
docker compose down

# Remover volume do banco para começar limpo
echo "🗑️ Removendo volume do banco de dados..."
docker volume rm sila-system_sila_db_data 2>/dev/null || true

# Iniciar apenas o banco de dados
echo "🐘 Iniciando PostgreSQL..."
docker compose up db -d

# Aguardar o banco estar pronto
echo "⏳ Aguardando PostgreSQL estar pronto..."
sleep 10

# Verificar se o banco está rodando
echo "🔍 Verificando conexão com o banco..."
docker compose exec db pg_isready -U postgres

# Iniciar o backend
echo "🔧 Iniciando backend..."
docker compose up backend -d

# Aguardar o backend estar pronto
echo "⏳ Aguardando backend estar pronto..."
sleep 15

# Executar migrações
echo "📊 Executando migrações do banco de dados..."
docker compose exec backend alembic upgrade head

# Verificar se o backend está funcionando
echo "🔍 Testando backend..."
curl -s http://localhost:8000/docs > /dev/null && echo "✅ Backend funcionando!" || echo "❌ Backend com problemas"

echo "🎉 Inicialização concluída!"
echo "📋 Serviços disponíveis:"
echo "   - Backend API: http://localhost:8000"
echo "   - Documentação: http://localhost:8000/docs"
echo "   - Banco de dados: localhost:5433"
