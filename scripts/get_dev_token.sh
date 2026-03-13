#!/bin/bash
# -*- coding: utf-8 -*-

# get_dev_token.sh
# Retrieve a development auth token from the backend
# Usage: ./scripts/get_dev_token.sh
# Output: Bearer token on stdout

set -e

BACKEND_URL="${BACKEND_URL:-http://localhost:8000}"
TEST_EMAIL="${TEST_EMAIL:-test@sila.gov.ao}"
TEST_PASSWORD="${TEST_PASSWORD:-TestPassword123!}"
TIMEOUT="${TIMEOUT:-10}"

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1" >&2
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1" >&2
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1" >&2
}

# Check prerequisites
if ! command -v curl &> /dev/null; then
    log_error "curl is required but not installed"
    exit 1
fi

if ! command -v jq &> /dev/null; then
    log_warn "jq not available; using basic string extraction"
    HAS_JQ=false
else
    HAS_JQ=true
fi

log_info "Authenticating as: $TEST_EMAIL"
log_info "Backend URL: $BACKEND_URL"

# Attempt login
RESPONSE=$(curl -s -w "\n%{http_code}" \
    --max-time "$TIMEOUT" \
    -X POST \
    -H "Content-Type: application/json" \
    -d "{\"username\": \"$TEST_EMAIL\", \"password\": \"$TEST_PASSWORD\"}" \
    "$BACKEND_URL/api/auth/login" 2>/dev/null || echo "CURL_ERROR\n000")

HTTP_STATUS=$(echo "$RESPONSE" | tail -1)
BODY=$(echo "$RESPONSE" | sed '$d')

if [ "$HTTP_STATUS" != "200" ] && [ "$HTTP_STATUS" != "201" ]; then
    log_error "Login failed with HTTP $HTTP_STATUS"
    [ -n "$BODY" ] && log_error "Response: $BODY"
    exit 1
fi

log_info "Login successful (HTTP $HTTP_STATUS)"

# Extract token
if [ "$HAS_JQ" = true ]; then
    TOKEN=$(echo "$BODY" | jq -r '.access_token // .token // empty' 2>/dev/null)
else
    # Fallback: basic grep/sed extraction
    TOKEN=$(echo "$BODY" | grep -o '"access_token":"[^"]*"' | cut -d'"' -f4 | head -1)
    if [ -z "$TOKEN" ]; then
        TOKEN=$(echo "$BODY" | grep -o '"token":"[^"]*"' | cut -d'"' -f4 | head -1)
    fi
fi

if [ -z "$TOKEN" ]; then
    log_error "Could not extract token from response"
    log_error "Raw response: $BODY"
    exit 1
fi

# Output token (without any prefix - let the script add Bearer if needed)
echo "$TOKEN"
exit 0
