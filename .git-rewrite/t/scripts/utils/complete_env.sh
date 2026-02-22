#!/bin/bash

# SILA System - Environment Variables Auto-Completion Script
# This script automatically fills in missing environment variables

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENV_FILE="$SCRIPT_DIR/.env"
ENV_EXAMPLE_FILE="$SCRIPT_DIR/.env.example"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${GREEN}[INFO]${NC} $*"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $*"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $*"
}

# Generate secure password
generate_password() {
    openssl rand -base64 16 | tr -d "=+/" | cut -c1-16
}

# Add missing variable to .env file
add_env_var() {
    local var_name="$1"
    local var_value="$2"
    local comment="$3"

    if ! grep -q "^${var_name}=" "$ENV_FILE" 2>/dev/null; then
        if [ -n "$comment" ]; then
            echo "# $comment" >> "$ENV_FILE"
        fi
        echo "${var_name}=${var_value}" >> "$ENV_FILE"
        log_info "Added $var_name to .env"
    else
        log_warning "$var_name already exists in .env"
    fi
}

# Main function to complete .env file
complete_env_file() {
    log_info "Completing .env file with missing variables..."

    # Ensure .env file exists
    if [ ! -f "$ENV_FILE" ]; then
        if [ -f "$ENV_EXAMPLE_FILE" ]; then
            cp "$ENV_EXAMPLE_FILE" "$ENV_FILE"
            log_info "Created .env from .env.example"
        else
            touch "$ENV_FILE"
            log_info "Created empty .env file"
        fi
    fi

    # Database Configuration
    add_env_var "POSTGRES_PASSWORD" "S1l4D3v2025!Str0ng" "PostgreSQL password for database authentication"
    add_env_var "POSTGRES_HOST" "db" "PostgreSQL host (Docker service name)"
    add_env_var "POSTGRES_PORT" "5432" "PostgreSQL port"
    add_env_var "POSTGRES_USER" "postgres" "PostgreSQL username"
    add_env_var "POSTGRES_DB" "sila_dev" "PostgreSQL database name"

    # Redis Configuration (Production)
    add_env_var "REDIS_URL" "redis://sila-redis:6379/0" "Redis connection URL for caching"
    add_env_var "REDIS_PASSWORD" "S1l4R3d1s2025!Str0ng" "Redis password for authentication"
    add_env_var "CELERY_BROKER_URL" "redis://sila-redis:6379/1" "Celery broker URL for background tasks"

    # MinIO Configuration (Production)
    add_env_var "MINIO_ENDPOINT" "sila-minio:9000" "MinIO S3-compatible endpoint"
    add_env_var "MINIO_ACCESS_KEY" "sila_minio_admin" "MinIO access key"
    add_env_var "MINIO_SECRET_KEY" "S1l4M1n102025!Str0ng" "MinIO secret key"
    add_env_var "MINIO_ROOT_USER" "sila_minio_admin" "MinIO root user"
    add_env_var "MINIO_ROOT_PASSWORD" "S1l4M1n102025!Str0ng" "MinIO root password"

    # Monitoring Stack (Production)
    add_env_var "GRAFANA_PASSWORD" "S1l4Gr4f4n42025!Str0ng" "Grafana admin password"
    add_env_var "SENTRY_DSN" "" "Sentry DSN for error tracking (leave empty if not used)"
    add_env_var "PROMETHEUS_GATEWAY" "sila-prometheus:9090" "Prometheus gateway URL"
    add_env_var "JAEGER_ENDPOINT" "http://sila-jaeger:14268" "Jaeger tracing endpoint"

    # Production Environment Variables
    add_env_var "REACT_APP_API_URL" "http://localhost:8000" "Frontend API URL"
    add_env_var "REACT_APP_ENVIRONMENT" "production" "React app environment"
    add_env_var "REACT_APP_SENTRY_DSN" "" "React Sentry DSN (leave empty if not used)"

    # SSL/TLS Configuration (Production)
    add_env_var "SSL_CERT_PATH" "./devops/ssl" "Path to SSL certificates"
    add_env_var "SSL_KEY_PATH" "./devops/ssl" "Path to SSL private keys"

    # Backup Configuration
    add_env_var "BACKUP_ENABLED" "true" "Enable automatic backups"
    add_env_var "BACKUP_SCHEDULE" "0 2 * * *" "Cron schedule for backups (2 AM daily)"
    add_env_var "BACKUP_RETENTION_DAYS" "30" "Days to keep backups"

    # Email Configuration (Optional)
    add_env_var "SMTP_HOST" "smtp.gmail.com" "SMTP server hostname"
    add_env_var "SMTP_PORT" "587" "SMTP server port"
    add_env_var "SMTP_USER" "" "SMTP username (leave empty if not used)"
    add_env_var "SMTP_PASSWORD" "" "SMTP password (leave empty if not used)"

    # External APIs (Optional)
    add_env_var "OPENAI_API_KEY" "" "OpenAI API key (leave empty if not used)"
    add_env_var "STRIPE_SECRET_KEY" "" "Stripe secret key (leave empty if not used)"
    add_env_var "STRIPE_PUBLISHABLE_KEY" "" "Stripe publishable key (leave empty if not used)"

    # File Upload Limits
    add_env_var "MAX_UPLOAD_SIZE" "10485760" "Maximum upload size in bytes (10MB)"
    add_env_var "ALLOWED_EXTENSIONS" "jpg,jpeg,png,pdf,doc,docx,txt" "Allowed file extensions"

    # Rate Limiting
    add_env_var "RATE_LIMIT_PER_MINUTE" "60" "Rate limit requests per minute"
    add_env_var "RATE_LIMIT_BURST" "10" "Rate limit burst capacity"

    # Session Configuration
    add_env_var "SESSION_TIMEOUT_MINUTES" "60" "Session timeout in minutes"
    add_env_var "SESSION_COOKIE_SECURE" "false" "Use secure session cookies"

    # Cache Configuration
    add_env_var "CACHE_TTL_SECONDS" "3600" "Cache time-to-live in seconds"
    add_env_var "CACHE_BACKEND" "redis" "Cache backend (redis/memory)"

    # Telemetry & Analytics (Optional)
    add_env_var "TELEMETRY_ENABLED" "false" "Enable telemetry collection"
    add_env_var "ANALYTICS_ID" "" "Analytics tracking ID (leave empty if not used)"

    # Feature Flags
    add_env_var "FEATURE_AUTO_HEALER" "true" "Enable auto-healer functionality"
    add_env_var "FEATURE_MONITORING" "true" "Enable monitoring features"
    add_env_var "FEATURE_BACKUP" "true" "Enable backup features"

    # Development Only
    add_env_var "PYTHONDONTWRITEBYTECODE" "1" "Prevent Python bytecode generation"
    add_env_var "PYTHONUNBUFFERED" "1" "Enable unbuffered Python output"

    log_info ".env file completed successfully!"
    echo
    log_info "Summary of changes:"
    echo "  - Added PostgreSQL configuration"
    echo "  - Added Redis configuration for production"
    echo "  - Added MinIO S3-compatible storage"
    echo "  - Added monitoring stack configuration"
    echo "  - Added production environment variables"
    echo "  - Added SSL/TLS, backup, and email configurations"
    echo "  - Added rate limiting and session management"
    echo "  - Added feature flags and development settings"
    echo
    log_warning "Note: Some variables are left empty for optional services."
    log_warning "Configure them as needed for your specific use case."
}

# Validate .env file
validate_env_file() {
    log_info "Validating .env file..."

    local required_vars=("POSTGRES_PASSWORD" "SECRET_KEY" "DATABASE_URL")
    local missing_vars=()

    for var in "${required_vars[@]}"; do
        if ! grep -q "^${var}=" "$ENV_FILE" 2>/dev/null; then
            missing_vars+=("$var")
        fi
    done

    if [ ${#missing_vars[@]} -eq 0 ]; then
        log_info "All required environment variables are present!"
        return 0
    else
        log_warning "Missing required variables: ${missing_vars[*]}"
        return 1
    fi
}

# Show usage
show_usage() {
    echo "SILA System - Environment Variables Manager"
    echo
    echo "Usage: $0 [COMMAND]"
    echo
    echo "Commands:"
    echo "  complete    Complete .env file with missing variables"
    echo "  validate    Validate .env file for required variables"
    echo "  help        Show this help message"
    echo
    echo "Examples:"
    echo "  $0 complete    # Complete .env file"
    echo "  $0 validate    # Validate .env file"
}

# Main script logic
main() {
    case "${1:-complete}" in
        "complete")
            complete_env_file
            ;;
        "validate")
            if validate_env_file; then
                log_info "Environment validation passed!"
            else
                log_error "Environment validation failed!"
                exit 1
            fi
            ;;
        "help"|"-h"|"--help")
            show_usage
            ;;
        *)
            log_error "Unknown command: $1"
            echo
            show_usage
            exit 1
            ;;
    esac
}

main "$@"
