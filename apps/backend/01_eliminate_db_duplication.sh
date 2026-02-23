#!/bin/bash
echo "🔥 ELIMINANDO DUPLICAÇÃO DE DATABASE"
echo "====================================="

# Encontrar todos os diretórios DB problemáticos
DB_DIRS=$(find app/modules -path "*/infrastructure/db" -type d 2>/dev/null)

if [ -z "$DB_DIRS" ]; then
    echo "✅ Nenhum diretório DB duplicado encontrado"
else
    echo "$DB_DIRS" | while read dir; do
        echo "📁 Encontrado: $dir"
        
        # Encontrar imports deste diretório
        grep -r "from.*$dir" app/modules --include="*.py" 2>/dev/null | cut -d: -f1 | sort -u | while read file; do
            echo "   ↳ Corrigindo: $file"
            sed -i 's|from .*db import get_db|from app.core.db import get_db|g' "$file"
            sed -i 's|from .*db import AsyncSessionLocal|from app.core.db import AsyncSessionLocal|g' "$file"
            sed -i 's|from .*db import Base|from app.core.db import Base|g' "$file"
        done
        
        # Backup e desativar
        backup_name="${dir}.bak.$(date +%s)"
        mv "$dir" "$backup_name" 2>/dev/null && echo "   ✅ Desativado: $backup_name"
    done
fi

# Verificar create_async_engine residual
echo ""
echo "🔍 Verificando create_async_engine residual..."
residual=$(find app/modules -name "*.py" -exec grep -l "create_async_engine" {} \; 2>/dev/null)

if [ -z "$residual" ]; then
    echo "✅ Nenhum create_async_engine em módulos"
else
    echo "$residual" | while read file; do
        echo "   ❌ Encontrado em: $file"
        sed -i '/create_async_engine/d' "$file"
        sed -i '/AsyncSessionLocal/d' "$file"
        sed -i 's|import AsyncSession|from app.core.db import AsyncSessionLocal; # AsyncSessionLocal|g' "$file"
        echo "      ✅ Corrigido"
    done
fi

echo ""
echo "✅ FASE 1 CONCLUÍDA"
