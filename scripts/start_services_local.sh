#!/bin/bash
###############################################################################
# SILA 3.0 - Local Service Orchestrator (Phase 18.3)
# Bare-Metal Orchestration for WSL2 without Docker
# Maps container DNS names to localhost endpoints
###############################################################################

set -euo pipefail

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Global configuration
export SILA_ENV="development"
export ALERT_HANDLER_PORT=${ALERT_HANDLER_PORT:-8080}
export PROMETHEUS_PORT=${PROMETHEUS_PORT:-9090}
export ALERTMANAGER_PORT=${ALERTMANAGER_PORT:-9093}
export GRAFANA_PORT=${GRAFANA_PORT:-3000}
export ELASTICSEARCH_PORT=${ELASTICSEARCH_PORT:-9200}
export LOGSTASH_PORT=${LOGSTASH_PORT:-9600}
export SILA_BACKEND_PORT=${SILA_BACKEND_PORT:-8000}

# Timestamp logging
LOG_DIR="${SILA_LOG_DIR:-./logs}"
PID_FILE="${LOG_DIR}/.sila_processes.pid"
mkdir -p "$LOG_DIR"

# Trap cleanup on exit
trap cleanup SIGTERM SIGINT EXIT

###############################################################################
# UTILITY FUNCTIONS
###############################################################################

log_info() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} ${GREEN}✓${NC} $1"
}

log_warn() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} ${YELLOW}⚠${NC} $1"
}

log_error() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} ${RED}✗${NC} $1"
}

log_header() {
    echo ""
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
}

# Check if port is in use
is_port_in_use() {
    local port=$1
    netstat -tuln 2>/dev/null | grep -q ":$port " && return 0 || return 1
}

# Kill process on port
kill_port_process() {
    local port=$1
    if is_port_in_use "$port"; then
        log_warn "Port $port is in use. Attempting to kill process..."
        if command -v fuser &> /dev/null; then
            fuser -k "$port/tcp" 2>/dev/null || true
        else
            # Fallback for systems without fuser
            local pid=$(netstat -tuln 2>/dev/null | grep ":$port " | awk '{print $NF}' | cut -d'/' -f1)
            if [ -n "$pid" ] && [ "$pid" != "-" ]; then
                kill -9 "$pid" 2>/dev/null || true
            fi
        fi
        sleep 1
    fi
}

save_pid() {
    local service=$1
    local pid=$2
    echo "$service:$pid" >> "$PID_FILE"
    log_info "Tracked PID for $service: $pid"
}

cleanup() {
    log_header "🛑 SILA Shutdown Sequence"
    if [ -f "$PID_FILE" ]; then
        while IFS=: read -r service pid; do
            if kill -0 "$pid" 2>/dev/null; then
                log_info "Stopping $service (PID: $pid)..."
                kill -TERM "$pid" 2>/dev/null || true
                sleep 1
                kill -9 "$pid" 2>/dev/null || true
            fi
        done < "$PID_FILE"
        rm -f "$PID_FILE"
    fi
    log_info "All services stopped"
}

###############################################################################
# PORT VALIDATION
###############################################################################

validate_ports() {
    log_header "🔍 Port Availability Check"
    
    local ports=("$ALERT_HANDLER_PORT" "$PROMETHEUS_PORT" "$ALERTMANAGER_PORT" \
                 "$GRAFANA_PORT" "$ELASTICSEARCH_PORT" "$LOGSTASH_PORT" "$SILA_BACKEND_PORT")
    local port_names=("Alert Handler" "Prometheus" "Alertmanager" \
                      "Grafana" "Elasticsearch" "Logstash" "SILA Backend")
    
    for i in "${!ports[@]}"; do
        local port=${ports[$i]}
        local name=${port_names[$i]}
        
        if is_port_in_use "$port"; then
            log_error "Port $port ($name) is already in use"
            log_warn "Attempting to free port $port..."
            kill_port_process "$port"
            
            if is_port_in_use "$port"; then
                log_error "Failed to free port $port. Exiting."
                exit 1
            fi
        else
            log_info "Port $port ($name) is available ✓"
        fi
    done
}

###############################################################################
# ENVIRONMENT CONFIGURATION
###############################################################################

setup_environment() {
    log_header "⚙️  Environment Configuration"
    
    # Set PYTHONPATH to include backend modules
    export PYTHONPATH="${PYTHONPATH:+$PYTHONPATH:}$(pwd)/apps/backend:$(pwd)"
    log_info "PYTHONPATH set: $PYTHONPATH"
    
    # Load .env if exists
    if [ -f ".env.local" ]; then
        log_info "Loading .env.local..."
        set -a
        source .env.local
        set +a
    fi
    
    # Validate critical environment variables
    local required_vars=("SILA_ENV" "ALERT_HANDLER_PORT" "PROMETHEUS_PORT")
    for var in "${required_vars[@]}"; do
        if [ -z "${!var:-}" ]; then
            log_error "Required variable $var is not set"
            exit 1
        fi
    done
    
    # Alert service configuration
    export SLACK_WEBHOOK_URL="${SLACK_WEBHOOK_URL:-http://localhost:9001/slack}"
    export SMTP_SERVER="${SMTP_SERVER:-localhost}"
    export SMTP_PORT="${SMTP_PORT:-587}"
    export SMTP_USER="${SMTP_USER:-admin}"
    export SMTP_PASSWORD="${SMTP_PASSWORD:-password}"
    export ALERT_FROM_EMAIL="${ALERT_FROM_EMAIL:-alerts@sila.local}"
    export SECURITY_EMAIL="${SECURITY_EMAIL:-security@sila.local}"
    
    log_info "Alert Handler configured for port $ALERT_HANDLER_PORT"
    log_info "Prometheus configured for port $PROMETHEUS_PORT"
    log_info "Alertmanager configured for port $ALERTMANAGER_PORT"
}

###############################################################################
# SERVICE STARTUP
###############################################################################

start_alert_handler() {
    log_header "🚀 Starting Alert Handler"
    
    if ! command -v python3 &> /dev/null; then
        log_error "python3 is not installed"
        exit 1
    fi
    
    cd apps/backend
    PYTHONPATH=".:$(pwd):$(pwd)/.." \
    python3 app/core/observability/alert_handler.py \
        --host 127.0.0.1 \
        --port "$ALERT_HANDLER_PORT" \
        > "$LOG_DIR/alert_handler.log" 2>&1 &
    
    local pid=$!
    save_pid "alert-handler" "$pid"
    cd - > /dev/null
    sleep 2
    
    if ps -p "$pid" > /dev/null; then
        log_info "Alert Handler started (PID: $pid)"
    else
        log_error "Alert Handler failed to start. Check logs at $LOG_DIR/alert_handler.log"
        exit 1
    fi
}

start_prometheus() {
    log_header "🔍 Starting Prometheus"
    
    if ! command -v prometheus &> /dev/null; then
        log_warn "prometheus binary not found in PATH"
        log_warn "Please install Prometheus: https://prometheus.io/download/"
        return 1
    fi
    
    prometheus \
        --config.file="prometheus.yml" \
        --web.listen-address="127.0.0.1:$PROMETHEUS_PORT" \
        --web.telemetry-path="/metrics" \
        --log.level=info \
        > "$LOG_DIR/prometheus.log" 2>&1 &
    
    local pid=$!
    save_pid "prometheus" "$pid"
    sleep 2
    
    if ps -p "$pid" > /dev/null; then
        log_info "Prometheus started (PID: $pid) - http://localhost:$PROMETHEUS_PORT"
    else
        log_error "Prometheus failed to start. Check logs at $LOG_DIR/prometheus.log"
    fi
}

start_alertmanager() {
    log_header "🚨 Starting Alertmanager"
    
    if ! command -v alertmanager &> /dev/null; then
        log_warn "alertmanager binary not found in PATH"
        log_warn "Please install Alertmanager: https://prometheus.io/download/"
        return 1
    fi
    
    alertmanager \
        --config.file="alertmanager.yml" \
        --web.listen-address="127.0.0.1:$ALERTMANAGER_PORT" \
        > "$LOG_DIR/alertmanager.log" 2>&1 &
    
    local pid=$!
    save_pid "alertmanager" "$pid"
    sleep 2
    
    if ps -p "$pid" > /dev/null; then
        log_info "Alertmanager started (PID: $pid) - http://localhost:$ALERTMANAGER_PORT"
    else
        log_error "Alertmanager failed to start. Check logs at $LOG_DIR/alertmanager.log"
    fi
}

start_anomaly_detector() {
    log_header "🤖 Starting Anomaly Detector"
    
    cd apps/backend
    PYTHONPATH=".:$(pwd):$(pwd)/.." \
    python3 -m app.core.observability.anomaly_detector \
        > "$LOG_DIR/anomaly_detector.log" 2>&1 &
    
    local pid=$!
    save_pid "anomaly-detector" "$pid"
    cd - > /dev/null
    sleep 2
    
    if ps -p "$pid" > /dev/null; then
        log_info "Anomaly Detector started (PID: $pid)"
    else
        log_warn "Anomaly Detector may have failed. Check logs at $LOG_DIR/anomaly_detector.log"
    fi
}

###############################################################################
# HEALTH CHECKS
###############################################################################

health_check() {
    log_header "💓 Health Check"
    
    local services=(
        "Alert Handler|http://127.0.0.1:$ALERT_HANDLER_PORT/health"
        "Prometheus|http://127.0.0.1:$PROMETHEUS_PORT/-/healthy"
        "Alertmanager|http://127.0.0.1:$ALERTMANAGER_PORT/-/healthy"
    )
    
    for service_info in "${services[@]}"; do
        IFS='|' read -r name url <<< "$service_info"
        
        if command -v curl &> /dev/null; then
            if curl -s "$url" > /dev/null 2>&1; then
                log_info "$name is healthy ✓"
            else
                log_warn "$name health check failed"
            fi
        else
            log_warn "curl not available, skipping health check for $name"
        fi
    done
}

###############################################################################
# MAIN ORCHESTRATION
###############################################################################

main() {
    log_header "🚀 SILA 3.0 - Local Service Orchestrator (Phase 18.3)"
    log_info "Environment: $SILA_ENV"
    log_info "Starting at $(date)"
    
    # Pre-flight checks
    validate_ports
    setup_environment
    
    # Start services
    start_alert_handler
    start_prometheus || true    # Soft fail if prometheus not installed
    start_alertmanager || true  # Soft fail if alertmanager not installed
    start_anomaly_detector || true
    
    # Health checks
    sleep 3
    health_check
    
    log_header "✅ SILA 3.0 Observability Stack Online"
    log_info "Services running with PIDs stored at: $PID_FILE"
    log_info "Logs available at: $LOG_DIR"
    log_info ""
    log_info "Quick Links:"
    log_info "  Alert Handler: http://localhost:$ALERT_HANDLER_PORT"
    log_info "  Prometheus:    http://localhost:$PROMETHEUS_PORT"
    log_info "  Alertmanager:  http://localhost:$ALERTMANAGER_PORT"
    log_info "  Grafana:       http://localhost:$GRAFANA_PORT (if running separately)"
    log_info ""
    log_info "Tail logs with: tail -f $LOG_DIR/*.log"
    log_info "Stop all services with: Ctrl+C or pkill -f start_services_local"
    
    # Keep process alive
    wait
}

# Execute main
main "$@"
