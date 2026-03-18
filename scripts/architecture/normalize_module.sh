#!/bin/bash
# Universal Module Normalization Script
# Applies DDD + Hexagonal Architecture pattern to any SILA module

MODULE_PATH="$1"
MODULE_NAME=$(basename "$MODULE_PATH")

if [ -z "$MODULE_PATH" ] || [ ! -d "$MODULE_PATH" ]; then
  echo "Usage: $0 /path/to/module"
  exit 1
fi

cd "$MODULE_PATH" || exit 1

echo "📦 NORMALIZING: $MODULE_NAME"
echo ""

# BATCH 1: Remove nested duplicate layers
echo "  BATCH 1: Removendo camadas duplicadas..."
rm -rf api/api api/application api/domain api/infrastructure 2>/dev/null
rm -rf application/api application/application application/domain application/infrastructure 2>/dev/null
rm -rf domain/api domain/application 2>/dev/null
rm -rf infrastructure/api infrastructure/application infrastructure/domain 2>/dev/null
echo "    ✓ Camadas aninhadas removidas"

# BATCH 2: Create proper structure
echo "  BATCH 2: Criando estrutura correta..."
mkdir -p application/{commands,dto,queries,services}
mkdir -p domain/{entities,events,exceptions,models,ports,repositories,services,value_objects}
mkdir -p infrastructure/{adapters,orm,repositories}
mkdir -p api/endpoints
echo "    ✓ Diretórios criados"

# BATCH 3: Create __init__.py files
echo "  BATCH 3: Criando __init__.py..."
touch application/{commands,dto,queries,services}/__init__.py
touch domain/{entities,events,exceptions,models,ports,repositories,services,value_objects}/__init__.py
touch infrastructure/{adapters,orm,repositories}/__init__.py
touch api/endpoints/__init__.py
echo "    ✓ __init__.py criados"

# BATCH 4: Consolidate isolated exception files
echo "  BATCH 4: Consolidando arquivos isolados..."
[ -f domain/exceptions.py ] && mv domain/exceptions.py domain/exceptions/__init__.py 2>/dev/null
echo "    ✓ Consolidação concluída"

# Summary
echo ""
echo "✅ $MODULE_NAME NORMALIZADO"
echo ""
printf "  Arquivos Python: %d\n" "$(find . -name '*.py' -not -path '*__pycache__*' 2>/dev/null | wc -l)"
printf "  Estrutura válida: "
[ -d api/endpoints ] && [ -d application/services ] && [ -d domain/services ] && [ -d infrastructure/repositories ] && echo "✓" || echo "✗"
