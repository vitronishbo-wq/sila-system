#!/bin/bash
# EVENT BUS QUICK START - Comandos essenciais
# Data: 10 Março 2026

echo "🚀 SILA Event-Driven Architecture - Quick Start"
echo "================================================"
echo ""

# 1. START REDIS
echo "1️⃣  Iniciando Redis..."
docker-compose -f docker-compose.events.yml up -d
sleep 2

# 2. CHECK REDIS
echo ""
echo "2️⃣  Verificando Redis..."
redis-cli PING

# 3. RUN TESTS
echo ""
echo "3️⃣  Rodando testes..."
cd /home/dev03wsl/sila-system
python -m pytest apps/backend/app/core/events/test_event_bus.py -v --tb=short

# 4. RUN VALIDATION
echo ""
echo "4️⃣  Validando implementação..."
python validate_event_bus.py

# 5. SUBSCRIBE TO CHANNEL (em background)
echo ""
echo "5️⃣  Listening for events (pressione Ctrl+C para sair)..."
redis-cli -h 127.0.0.1 SUBSCRIBE USER_LOGGED_IN &
REDIS_SUB_PID=$!

# 6. START EVENT WORKER (em background)
echo ""
echo "6️⃣  Iniciando Event Worker..."
python apps/backend/app/workers/event_worker.py &
WORKER_PID=$!

# 7. MESSAGES
echo ""
echo "$======================================="
echo "✅ TUDO PRONTO!"
echo "================================================"
echo ""
echo "📝 Próximos passos:"
echo "  1. Integrar EventBus em apps/backend/main.py"
echo "  2. Deploy Event Worker container"
echo "  3. Configurar Grafana dashboards"
echo ""
echo "📊 Monitorar em:"
echo "  - Redis CLI: redis-cli MONITOR"
echo "  - Redis Commander: http://localhost:8081"
echo "  - Loki: grep request_id in logs"
echo ""
echo "🔗 Documentação:"
echo "  - EVENT_BUS_ARCHITECTURE.md"
echo "  - EVENT_BUS_COMPLIANCE_REPORT.md"
echo ""
echo "Pressione Ctrl+C para sair..."
echo "======================================="

wait $REDIS_SUB_PID $WORKER_PID
