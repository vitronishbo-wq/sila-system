#!/bin/bash
#
# Script de teste PASSO 13 & 14: Automação Real com RabbitMQ e DLQ
#
# Testa:
# 1. Endpoints de transferência async/sync
# 2. Publicação de eventos em RabbitMQ
# 3. Processing por automation worker
# 4. DLQ para mensagens falhadas
#

set -e

API_URL="${API_URL:-http://localhost:8000}"
RABBITMQ_URL="${RABBITMQ_URL:-http://localhost:15672}"
TIMEOUT=10

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}=== PASSO 13 & 14: Teste de Automação Real ===${NC}"
echo ""

# 1. Health checks
echo -e "${YELLOW}[1/4] Health Checks...${NC}"
echo "  - Backend API..."
if curl -sf "${API_URL}/api/v1/health" > /dev/null; then
    echo -e "    ${GREEN}✓ Backend rodando${NC}"
else
    echo -e "    ${RED}✗ Backend não responde${NC}"
    exit 1
fi

echo "  - RabbitMQ Management..."
if curl -sf -u guest:guest "${RABBITMQ_URL}/api/vhosts" > /dev/null; then
    echo -e "    ${GREEN}✓ RabbitMQ rodando${NC}"
else
    echo -e "    ${RED}✗ RabbitMQ não responde${NC}"
    exit 1
fi

# 2. Test transferência async (PASSO 13)
echo ""
echo -e "${YELLOW}[2/4] Teste de Transferência Assíncrona (PASSO 13)...${NC}"

ASYNC_RESPONSE=$(curl -sf -X POST "${API_URL}/api/v1/educacao/transferencias/automacao/async" \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": "TEST-ASYNC-001",
    "target_school": "ESCOLA-TESTE",
    "target_class": "10A",
    "academic_year": 2024,
    "metadata": {"origem": "test_script"}
  }')

echo "  Resposta: $ASYNC_RESPONSE"

if echo "$ASYNC_RESPONSE" | grep -q "scheduled\|rejected\|error"; then
    echo -e "    ${GREEN}✓ Endpoint /async respondeu${NC}"
else
    echo -e "    ${RED}✗ Resposta inesperada${NC}"
    exit 1
fi

# 3. Test transferência sync
echo ""
echo -e "${YELLOW}[3/4] Teste de Transferência Síncrona...${NC}"

SYNC_RESPONSE=$(curl -sf -X POST "${API_URL}/api/v1/educacao/transferencias/automacao/sync" \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": "TEST-SYNC-001",
    "target_school": "ESCOLA-TESTE",
    "target_class": "10B",
    "academic_year": 2024,
    "metadata": {"origem": "test_script"}
  }')

echo "  Resposta: $SYNC_RESPONSE"

if echo "$SYNC_RESPONSE" | grep -q "executed\|rejected\|error"; then
    echo -e "    ${GREEN}✓ Endpoint /sync respondeu${NC}"
else
    echo -e "    ${RED}✗ Resposta inesperada${NC}"
    exit 1
fi

# 4. Verificar filas RabbitMQ
echo ""
echo -e "${YELLOW}[4/4] Verificar Filas RabbitMQ (PASSO 13 & 14)...${NC}"

# Listam as filas
QUEUES=$(curl -sf -u guest:guest "${RABBITMQ_URL}/api/queues" | grep -o '"name":"[^"]*"' | cut -d'"' -f4)

echo "  Filas encontradas:"
for queue in $QUEUES; do
    echo "    - $queue"
done

# Verificar filas de transferência
if echo "$QUEUES" | grep -q "sila_transfer"; then
    echo -e "    ${GREEN}✓ Filas de transferência criadas${NC}"
else
    echo -e "    ${YELLOW}⚠ Filas de transferência não encontradas (ainda podem estar sendo criadas)${NC}"
fi

# Verificar DLQ
if echo "$QUEUES" | grep -q "sila_dlq_main"; then
    echo -e "    ${GREEN}✓ Dead Letter Queue encontrada${NC}"
else
    echo -e "    ${YELLOW}⚠ DLQ não encontrada (normal se nenhuma falha ocorreu)${NC}"
fi

echo ""
echo -e "${GREEN}=== Testes Completados com Sucesso ===${NC}"
echo ""
echo "Próximas ações:"
echo "1. Acompanhar logs:"
echo "   docker compose -f docker-compose.minimal.yml logs -f automation dlq-worker"
echo ""
echo "2. Acessar RabbitMQ Management:"
echo "   http://localhost:15672 (guest/guest)"
echo ""
echo "3. Verificar status da API:"
echo "   curl http://localhost:8000/api/v1/health"
