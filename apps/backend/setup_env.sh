#!/bin/bash
# apps/backend/setup_env.sh

echo "🛠️ Configurando ambiente virtual Python para SILA Backend..."

# Navega até o diretório do backend
cd /home/truman/dev/sila-system/apps/backend || { echo "❌ Diretório não encontrado"; exit 1; }

# Cria o ambiente virtual se não existir
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
    echo "✅ Venv criada."
fi

# Ativa o ambiente e instala dependências
source .venv/bin/activate
pip install --upgrade pip
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    echo "✅ Dependências instaladas."
else
    echo "⚠️ requirements.txt não encontrado."
fi

# Exporta variáveis para a sessão atual (útil para rodar scripts locais)
export POSTGRES_PASSWORD=Trumanmarcelo_1983
export DATABASE_URL=postgresql+asyncpg://sila_user:Trumanmarcelo_1983@db:5432/sila_db

echo "🚀 Ambiente pronto! Use 'source .venv/bin/activate' para entrar."