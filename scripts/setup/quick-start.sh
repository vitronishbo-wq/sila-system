#!/bin/bash

# ============================================================================
# SILA DevContainer Quick Start
# ============================================================================

set -euo pipefail

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

COMPOSE_FILE=".devcontainer/docker-compose.yml"
COMPOSE_CMD=(docker compose -f "$COMPOSE_FILE")
RUNTIME_SERVICES=(db redis)
PULL_LOG="$(mktemp -t sila-quickstart-pull.XXXXXX.log)"
PULL_PID=""
PULL_TARGET_LABEL="PostgreSQL/Redis images"
MISSING_RUNTIME_SERVICES=()

cleanup() {
    rm -f "$PULL_LOG"
}

trap cleanup EXIT

print_info() {
    echo -e "${BLUE}$1${NC}"
}

print_success() {
    echo -e "${GREEN}$1${NC}"
}

print_warning() {
    echo -e "${YELLOW}$1${NC}"
}

print_error() {
    echo -e "${RED}$1${NC}"
}

wait_for_background_pull() {
    if [ -z "${PULL_PID:-}" ]; then
        return 0
    fi

    local elapsed=0
    printf "  - Pulling %s" "$PULL_TARGET_LABEL"
    while kill -0 "$PULL_PID" 2>/dev/null; do
        printf "."
        sleep 2
        elapsed=$((elapsed + 2))
    done
    printf "\n"

    if wait "$PULL_PID"; then
        print_success "✓ Runtime images ready (${elapsed}s)"
    else
        print_error "✗ Failed to pull PostgreSQL/Redis images"
        sed -n '1,120p' "$PULL_LOG"
        exit 1
    fi
}

detect_missing_runtime_images() {
    MISSING_RUNTIME_SERVICES=()

    local service=""
    local image=""
    for service in "${RUNTIME_SERVICES[@]}"; do
        image="$("${COMPOSE_CMD[@]}" config --images "$service" | head -n 1)"

        if [ -z "$image" ]; then
            continue
        fi

        if ! docker image inspect "$image" >/dev/null 2>&1; then
            MISSING_RUNTIME_SERVICES+=("$service")
        fi
    done
}

start_runtime_pull_if_needed() {
    detect_missing_runtime_images

    if [ "${#MISSING_RUNTIME_SERVICES[@]}" -eq 0 ]; then
        print_success "✓ Runtime images already cached locally"
        return 0
    fi

    PULL_TARGET_LABEL="$(IFS=', '; echo "${MISSING_RUNTIME_SERVICES[*]} images")"
    print_info "  - Pulling only missing runtime images (${MISSING_RUNTIME_SERVICES[*]})"
    "${COMPOSE_CMD[@]}" pull -q "${MISSING_RUNTIME_SERVICES[@]}" >"$PULL_LOG" 2>&1 &
    PULL_PID=$!
}

echo ""
echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║     SILA Enterprise - DevContainer Autonomous Setup        ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

# 1. Check prerequisites
echo -e "${YELLOW}[1/5] Checking prerequisites...${NC}"

if ! command -v docker &> /dev/null; then
    echo -e "${RED}✗ Docker not found. Please install Docker first.${NC}"
    exit 1
fi

if ! command -v git &> /dev/null; then
    echo -e "${RED}✗ Git not found. Please install Git first.${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Docker${NC} $(docker --version | cut -d' ' -f3)"
echo -e "${GREEN}✓ Git${NC} $(git --version | cut -d' ' -f3)"

# 2. Check .env file
echo ""
echo -e "${YELLOW}[2/5] Checking environment configuration...${NC}"

if [ ! -f ".env" ]; then
    echo -e "${RED}✗ .env file not found!${NC}"
    echo "Please create .env with database credentials:"
    echo "  POSTGRES_USER=sila_user"
    echo "  POSTGRES_PASSWORD=Trumanmarcelo_1983"
    echo "  POSTGRES_DB=sila_db"
    exit 1
fi

echo -e "${GREEN}✓ .env file present${NC}"

# 3. Build DevContainer
echo ""
echo -e "${YELLOW}[3/5] Building DevContainer (this may take 2-3 minutes)...${NC}"

start_runtime_pull_if_needed

if "${COMPOSE_CMD[@]}" build app; then
    print_success "✓ Build successful"
else
    print_error "✗ Build failed"
    exit 1
fi

wait_for_background_pull

# 4. Start services
echo ""
echo -e "${YELLOW}[4/5] Starting services...${NC}"

"${COMPOSE_CMD[@]}" up -d --no-build --wait --wait-timeout 120

print_success "✓ Services started"
echo "  - App container: sila-dev-agent"
echo "  - PostgreSQL: localhost:5432"
echo "  - Redis: localhost:6379"

# 5. Run migrations
echo ""
echo -e "${YELLOW}[5/5] Running database migrations...${NC}"

if "${COMPOSE_CMD[@]}" exec -T app bash -lc "cd apps/backend && alembic upgrade heads"; then
    print_success "✓ Database ready"
else
    print_error "✗ Database migration failed"
    exit 1
fi

# Final instructions
echo ""
echo -e "${GREEN}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║                  ✅ READY TO START!                        ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BLUE}📌 Next Steps:${NC}"
echo ""
echo "Option 1️⃣ : Open in VS Code DevContainer"
echo "  - Open VS Code"
echo "  - Press F1 → 'Dev Containers: Reopen in Container'"
echo "  - Choose '.devcontainer'"
echo ""
echo "Option 2️⃣ : Use the container directly"
echo "  docker exec -it sila-dev-agent bash"
echo ""
echo -e "${BLUE}🧪 Then run:${NC}"
echo "  make help           # See all available commands"
echo "  make test          # Run test suite"
echo "  make pipeline      # Run full CI/CD pipeline"
echo "  make codex-agent   # Start Codex in autonomous mode"
echo ""
echo -e "${YELLOW}📚 Documentation:${NC}"
echo "  .codex-instructions.md  # Agent operating instructions"
echo "  README-DEVCONTAINER.md  # Full setup guide"
echo ""
