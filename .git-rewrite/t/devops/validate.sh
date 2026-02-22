#!/bin/bash
# Validação rápida da configuração Docker Compose
cd "$(dirname "$0")"

export COMPOSE_FILE="docker-compose.yml"
export COMPOSE_PROJECT_NAME="sila-devops"

echo "=== Validação Docker Compose ==="
echo ""

# 1. Validar YAML
echo "1. Validando YAML..."
if docker compose config > /dev/null 2>&1; then
    echo "   ✅ YAML válido"
else
    echo "   ❌ YAML inválido"
    exit 1
fi

# 2. Listar serviços
echo "2. Serviços disponíveis:"
docker compose config --services | while read -r svc; do
    echo "   - $svc"
done

# 3. Verificar profiles
echo "3. Profiles disponíveis:"
docker compose config --profiles | while read -r prof; do
    echo "   - $prof"
done

# 4. Verificar se db e backend existem
echo "4. Verificando serviços críticos..."
CONFIG=$(docker compose config)
if echo "$CONFIG" | grep -q "container_name: sila-db"; then
    echo "   ✅ Serviço 'db' encontrado"
else
    echo "   ❌ Serviço 'db' NÃO encontrado"
    exit 1
fi

if echo "$CONFIG" | grep -q "container_name: sila-backend"; then
    echo "   ✅ Serviço 'backend' encontrado"
else
    echo "   ❌ Serviço 'backend' NÃO encontrado"
    exit 1
fi

# 5. Verificar depends_on
echo "5. Verificando dependências..."
if echo "$CONFIG" | grep -A5 "sila-backend" | grep -q "depends_on"; then
    echo "   ✅ Backend tem dependências configuradas"
else
    echo "   ⚠️  Backend sem dependências"
fi

echo ""
echo "=== ✅ Validação Concluída com Sucesso ==="
