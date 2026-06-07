#!/bin/bash
###############################################################################
# Phase 19 - Event Bus Worker Initialization Script
# Manages Outbox Worker and Event Worker processes
###############################################################################

set -euo pipefail

BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

SILA_HOME="${SILA_HOME:-/home/dev03wsl/sila-system}"
LOG_DIR="${SILA_HOME}/logs"
PID_DIR="${LOG_DIR}/.pids"

mkdir -p "$PID_DIR" "$LOG_DIR"

log_info() { echo -e "${GREEN}✓${NC} $1"; }
log_error() { echo -e "${RED}✗${NC} $1"; }
log_header() { echo -e "\n${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n${BLUE}$1${NC}\n${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"; }

trap cleanup EXIT

cleanup() {
    log_info "Cleaning up workers..."
    
    if [ -f "$PID_DIR/outbox_worker.pid" ]; then
        kill $(cat "$PID_DIR/outbox_worker.pid") 2>/dev/null || true
    fi
    
    if [ -f "$PID_DIR/event_worker.pid" ]; then
        kill $(cat "$PID_DIR/event_worker.pid") 2>/dev/null || true
    fi
}

start_outbox_worker() {
    log_header "Starting Outbox Worker"
    
    cd "$SILA_HOME/apps/backend"
    
    PYTHONPATH=".:$SILA_HOME/apps/backend:$SILA_HOME" \
    python3 -m apps.backend.app.core.events.workers.outbox_worker \
        > "$LOG_DIR/outbox_worker.log" 2>&1 &
    
    local pid=$!
    echo $pid > "$PID_DIR/outbox_worker.pid"
    
    log_info "Outbox Worker started (PID: $pid)"
    log_info "Logs: $LOG_DIR/outbox_worker.log"
}

start_event_worker() {
    log_header "Starting Event Worker"
    
    cd "$SILA_HOME/apps/backend"
    
    PYTHONPATH=".:$SILA_HOME/apps/backend:$SILA_HOME" \
    python3 -m apps.backend.app.core.events.workers.event_worker \
        > "$LOG_DIR/event_worker.log" 2>&1 &
    
    local pid=$!
    echo $pid > "$PID_DIR/event_worker.pid"
    
    log_info "Event Worker started (PID: $pid)"
    log_info "Logs: $LOG_DIR/event_worker.log"
}

verify_redis() {
    log_header "Verifying Redis"
    
    if ! command -v redis-cli &> /dev/null; then
        log_error "redis-cli not found"
        log_info "Install with: sudo apt install redis-server -y"
        return 1
    fi
    
    if ! redis-cli ping &>/dev/null; then
        log_error "Redis server not responding"
        log_info "Start with: sudo service redis-server start"
        return 1
    fi
    
    log_info "Redis is running"
}

verify_database() {
    log_header "Verifying Database"
    
    # Simple check - adjust based on your DB setup
    log_info "Database verification skipped (run migrations separately)"
}

main() {
    log_header "PHASE 19: Event Bus Worker Initialization"
    
    verify_redis || exit 1
    verify_database || exit 1
    
    start_outbox_worker
    start_event_worker
    
    log_header "Event Bus Workers Online"
    log_info "Outbox Worker: publishing from DB to Redis Streams"
    log_info "Event Worker: consuming from Redis and invoking handlers"
    log_info "Logs: $LOG_DIR/*.log"
    
    # Keep process alive
    wait
}

main "$@"
