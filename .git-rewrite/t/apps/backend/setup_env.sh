#!/bin/bash
echo "🔧 Iniciando configuração do ambiente virtual..."
cd /home/truman/dev/sila-system/apps/backend || exit
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
echo "✅ Ambiente virtual configurado com sucesso!"
echo "    source /home/truman/dev/sila-system/apps/backend/.venv/bin/activate"
