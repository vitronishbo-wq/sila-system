#!/bin/bash

# Diagnóstico inicial
echo "📂 Conteúdo atual de ~/.continue/:"
ls -la ~/.continue/

# Apagar configs conflitantes
echo "🧹 Limpando configs extras..."
rm -f ~/.continue/config.ts
rm -f ~/.continue/config.json.bak

# Recriar .continuerc.json limpo
echo "🔧 Recriando .continuerc.json..."
echo '{ "disableIndexing": false }' > ~/.continue/.continuerc.json

# Corrigir permissões do config.yaml
echo "🔑 Corrigindo permissões..."
chmod 644 ~/.continue/config.yaml

# Mostrar resultado final
echo "✅ Configuração final:"
ls -la ~/.continue/
