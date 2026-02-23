#!/bin/bash
# SILA System - Teste Rápido de Validação (2026-02-22)

echo "════════════════════════════════════════════════════════════════"
echo "  SILA SYSTEM - TESTE RÁPIDO DE VALIDAÇÃO"
echo "════════════════════════════════════════════════════════════════"
echo ""

cd apps/backend
source .venv/bin/activate

echo "1️⃣ Verificando users criados..."
PYTHONPATH=$(pwd):$PYTHONPATH python -c "
import psycopg2
import os
from dotenv import load_dotenv
from pathlib import Path

backend_root = Path.cwd()
load_dotenv(backend_root / '.env')

conn = psycopg2.connect(
    host=os.getenv('DB_HOST', '127.0.0.1'),
    port=int(os.getenv('DB_PORT', '5432')),
    database=os.getenv('DB_NAME', 'sila_db'),
    user=os.getenv('DB_USER', 'sila_user'),
    password=os.getenv('DB_PASSWORD', 'Trumanmarcelo_1983'),
)
cursor = conn.cursor()
cursor.execute('SELECT COUNT(*) FROM users')
count = cursor.fetchone()[0]
print(f'   ✅ Users no BD: {count}')

cursor.execute('SELECT email, administrative_level FROM users ORDER BY email')
for email, level in cursor.fetchall():
    print(f'      • {email} ({level})')

conn.close()
" || echo "   ❌ Erro ao conectar no BD"

echo ""
echo "2️⃣ Verificando imports..."
python -c "
from modules.identity.models.user import User
print('   ✅ User import OK')
" || echo "   ❌ Erro nos imports"

echo ""
echo "3️⃣ Verificando configuração..."
python -c "
from app.core.settings import settings
print(f'   ✅ Database: {settings.DATABASE_URL.split(\"/\")[-1]}')
" || echo "   ❌ Erro na configuração"

echo ""
echo "════════════════════════════════════════════════════════════════"
echo "✅ TESTE CONCLUÍDO"
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "Próximos passos:"
echo "1. Iniciar servidor: python -m uvicorn main:app --reload"
echo "2. Testar login: POST /api/auth/login"
echo "3. Ver documentação: cat ../../../SANEAMENTO_COMPLETO.md"
echo ""
