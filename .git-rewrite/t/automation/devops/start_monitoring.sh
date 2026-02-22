#!/bin/bash
# Script para equipe DevOps

echo "📊 Iniciando ambiente Monitoring SILA"
COMPOSE_FILE="/opt/sila-system/devops/docker-compose.yml"

# Verificar portas necessárias
check_ports() {
    echo "🔍 Verificando portas..."
    if lsof -i :3000 > /dev/null || lsof -i :9090 > /dev/null; then
        echo "❌ Portas de monitoramento já em uso (3000 - Grafana, 9090 - Prometheus)!"
        return 1
    fi
    return 0
}

# Parar containers de monitoramento
stop_monitoring() {
    echo "🛑 Parando serviços de monitoramento..."
    docker compose -f "$COMPOSE_FILE" stop grafana prometheus node-exporter || true
    docker compose -f "$COMPOSE_FILE" rm -f grafana prometheus node-exporter || true
}

# Iniciar stack de monitoramento
start_monitoring() {
    echo "📈 Iniciando serviços de monitoramento..."
    docker compose -f "$COMPOSE_FILE" --profile infra up -d grafana prometheus node-exporter

    echo "⏳ Aguardando Grafana ficar pronto..."
    for i in {1..30}; do
        if curl -s http://localhost:3000/api/health > /dev/null; then
            echo "✅ Grafana está pronto!"
            break
        fi
        echo -n "."
        sleep 1
    done

    echo "⏳ Aguardando Prometheus ficar pronto..."
    for i in {1..30}; do
        if curl -s http://localhost:9090/-/healthy > /dev/null; then
            echo "✅ Prometheus está pronto!"
            return 0
        fi
        echo -n "."
        sleep 1
    done
    echo "❌ Timeout aguardando serviços de monitoramento"
    return 1
}

# Verificar métricas
check_metrics() {
    echo "📊 Verificando coleta de métricas..."

    # Verificar node-exporter
    if curl -s http://localhost:9100/metrics > /dev/null; then
        echo "✅ Node Exporter está coletando métricas"
    else
        echo "⚠️ Node Exporter não está respondendo"
    fi

    # Verificar targets no Prometheus
    local targets=$(curl -s http://localhost:9090/api/v1/targets | grep "health=\"up\"" | wc -l)
    echo "📡 Targets ativos no Prometheus: $targets"
}

# Executar pipeline
main() {
    check_ports || exit 1
    stop_monitoring
    start_monitoring
    check_metrics

    echo "📝 Status final:"
    docker compose -f "$COMPOSE_FILE" ps grafana prometheus node-exporter
    echo "📊 Grafana: http://localhost:3000"
    echo "🔍 Prometheus: http://localhost:9090"
}

main
