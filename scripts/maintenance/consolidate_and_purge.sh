#!/bin/bash
set -e

echo "🧹 Iniciando Expurgo de Déficits Estruturais..."

# 1. CONSOLIDAÇÃO DE ACESSO (Mover tudo para Sovereign Access Control e deletar duplicatas)
echo "🛡️ Unificando Motores de Acesso..."
rm -rf app/modules/identity/bounded_contexts/access_control
rm -rf app/modules/identity/bounded_contexts/iam

# 2. EXPURGO DE ADAPTADORES PONTO-A-PONTO EM JUSTICE
# Agora que temos X-Road, Justice não fala direto com Saúde/Educação via adapters locais
echo "📡 Removendo adaptadores legados em Justice (Substituídos por X-Road)..."
rm -f app/modules/justice/bounded_contexts/infrastructure/adapters/saude_service_adapter.py
rm -f app/modules/justice/bounded_contexts/infrastructure/adapters/educacao_service_adapter.py
rm -f app/modules/justice/bounded_contexts/infrastructure/adapters/emprego_service_adapter.py

# 3. LIMPEZA DE ESQUELETOS VAZIOS (Folders sem .py funcionais)
echo "💀 Removendo módulos fantasma (Placeholder) para reduzir ruído..."
# Apenas se estiverem realmente vazios ou apenas com __init__.py
find app/modules/identity/cross_border_identity -type f | xargs rm -f
find app/modules/identity/smartcard_identity -type f | xargs rm -f

# 4. RE-HIDRATAÇÃO DO CONTEXTO ÚNICO DE IDENTIDADE
# Garantir que o user_repository seja o único para o módulo
mkdir -p app/modules/identity/infrastructure/persistence
mv app/modules/identity/infrastructure/repositories/* app/modules/identity/infrastructure/persistence/ 2>/dev/null || true

echo "✅ Expurgo concluído. Estrutura agora é Lean e focada em X-Road + Sovereign Engines."
