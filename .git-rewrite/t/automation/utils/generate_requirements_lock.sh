#!/bin/bash
# ==================================================
# Script para gerar requirements.lock
# ==================================================

set -e

echo "🔒 Gerando requirements.lock..."

# Diretório do projeto
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

# Criar um ambiente virtual temporário
echo "📦 Criando ambiente virtual temporário..."
python3 -m venv .venv_lock_temp

# Ativar o ambiente virtual
source .venv_lock_temp/bin/activate

# Atualizar pip
echo "⬆️  Atualizando pip..."
pip install --upgrade pip setuptools wheel

# Instalar dependências do requirements.txt
echo "📥 Instalando dependências..."
pip install -r requirements.txt

# Gerar requirements.lock
echo "💾 Gerando requirements.lock..."
pip freeze > requirements.lock

# Desativar e remover o ambiente virtual temporário
deactivate
rm -rf .venv_lock_temp

echo "✅ requirements.lock gerado com sucesso!"
echo "📍 Localização: $PROJECT_ROOT/requirements.lock"

# Mostrar resumo
echo ""
echo "📊 Resumo:"
wc -l requirements.lock
