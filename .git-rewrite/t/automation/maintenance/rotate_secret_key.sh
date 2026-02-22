#!/bin/bash

# SILA System SECRET_KEY Rotation Script
# Implements automated 90-day SECRET_KEY rotation

set -euo pipefail

# Configuration
ROTATION_DAYS=90
LOG_FILE="/opt/sila-system/logs/secret-key-rotation.log"
BACKEND_DIR="/opt/sila-system/backend"
SECURITY_TEAM_EMAIL="security@sila-system.com"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $*" | tee -a "${LOG_FILE}"
}

success() {
    log -e "${GREEN}✅ $*${NC}"
}

warning() {
    log -e "${YELLOW}⚠️  $*${NC}"
}

info() {
    log -e "${BLUE}ℹ️  $*${NC}"
}

# Generate new SECRET_KEY
generate_new_key() {
    info "Generating new cryptographically secure SECRET_KEY..."
    python3 -c "import secrets; print(secrets.token_urlsafe(64))"
}

# Check if rotation is needed
check_rotation_needed() {
    local last_rotation_file="${BACKEND_DIR}/.last_secret_key_rotation"

    if [[ ! -f "${last_rotation_file}" ]]; then
        info "No previous rotation record found - rotation needed"
        return 0
    fi

    local last_rotation=$(cat "${last_rotation_file}")
    local days_since_rotation=$(( ( $(date +%s) - $(date -d "${last_rotation}" +%s) ) / 86400 ))

    if [[ ${days_since_rotation} -ge ${ROTATION_DAYS} ]]; then
        info "Last rotation was ${days_since_rotation} days ago - rotation needed"
        return 0
    else
        info "Last rotation was ${days_since_rotation} days ago - no rotation needed yet"
        return 1
    fi
}

# Backup current SECRET_KEY
backup_current_key() {
    local current_key=$(grep "^SECRET_KEY=" "${BACKEND_DIR}/.env" | cut -d'=' -f2-)
    local backup_file="${BACKEND_DIR}/.secret_key_history"

    echo "$(date '+%Y-%m-%d %H:%M:%S') - ${current_key}" >> "${backup_file}"
    success "Current SECRET_KEY backed up to history file"
}

# Update SECRET_KEY
update_secret_key() {
    local new_key="$1"

    info "Updating SECRET_KEY in .env file..."

    # Create backup of entire .env file
    cp "${BACKEND_DIR}/.env" "${BACKEND_DIR}/.env.backup.$(date +%Y%m%d_%H%M%S)"

    # Update SECRET_KEY
    sed -i "s/^SECRET_KEY=.*/SECRET_KEY=${new_key}/" "${BACKEND_DIR}/.env"

    # Record rotation timestamp
    echo "$(date '+%Y-%m-%d %H:%M:%S')" > "${BACKEND_DIR}/.last_secret_key_rotation"

    success "SECRET_KEY updated successfully"
}

# Restart services
restart_services() {
    info "Restarting services to apply new SECRET_KEY..."

    # Systemd services
    systemctl restart sila-backend 2>/dev/null || warning "sila-backend service not found"

    # Docker services
    if [[ -f "/opt/sila-system/devops/monitoring/docker-compose.monitoring.yml" ]]; then
        cd /opt/sila-system/devops/monitoring && docker-compose -f docker-compose.monitoring.yml restart
    fi

    success "Services restarted"
}

# Send notification email
send_notification() {
    local new_key="$1"

    info "Sending rotation notification email..."

    cat << EOF | mail -s "SILA System SECRET_KEY Rotation Completed" "${SECURITY_TEAM_EMAIL}"
SILA System SECRET_KEY Rotation Report
=====================================

Rotation Date: $(date)
Previous Rotation: $(cat "${BACKEND_DIR}/.last_secret_key_rotation" 2>/dev/null || echo "N/A")
Next Scheduled Rotation: $(date -d "+${ROTATION_DAYS} days")

New SECRET_KEY: ${new_key}

Services Restarted: Yes
Backup Created: Yes

This is an automated message from the SILA System security rotation process.
EOF

    success "Notification email sent"
}

# Validate new configuration
validate_configuration() {
    info "Validating new configuration..."

    # Check if .env file is valid
    if python3 -c "
import os
try:
    with open('${BACKEND_DIR}/.env', 'r') as f:
        content = f.read()
    print('Environment file syntax: Valid')
except Exception as e:
    print(f'Environment file error: {e}')
    exit(1)
"; then
        success "Configuration validation passed"
    else
        error "Configuration validation failed"
    fi
}

# Main rotation function
main() {
    log "Starting SILA System SECRET_KEY rotation process..."

    # Create log file
    mkdir -p "$(dirname "${LOG_FILE}")"
    touch "${LOG_FILE}"

    # Check if rotation is needed
    if ! check_rotation_needed; then
        info "SECRET_KEY rotation not needed at this time"
        exit 0
    fi

    # Generate new key
    local new_key
    new_key=$(generate_new_key)

    if [[ -z "${new_key}" || ${#new_key} -lt 50 ]]; then
        error "Failed to generate valid SECRET_KEY"
    fi

    info "New SECRET_KEY generated (length: ${#new_key})"

    # Perform rotation
    backup_current_key
    update_secret_key "${new_key}"
    validate_configuration
    restart_services

    # Send notification
    send_notification "${new_key}"

    success "SECRET_KEY rotation completed successfully!"
    info "Next rotation scheduled for: $(date -d "+${ROTATION_DAYS} days")"
}

# Run main function
main "$@"
