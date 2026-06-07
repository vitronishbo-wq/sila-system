FROM mcr.microsoft.com/devcontainers/python:3.11-bullseye

# ============================================================================
# SILA System - Development Container with Codex Full Autonomy
# ============================================================================

# UID/GID synchronization (aligns container user with host)
ARG USER_UID=1000
ARG USER_GID=1000

RUN groupmod -g $USER_GID vscode && \
    usermod -u $USER_UID -g $USER_GID vscode && \
    echo "[✓] User 'vscode' synced: UID=$USER_UID GID=$USER_GID"

# Install system dependencies.
# The base Dev Container image ships with a Yarn apt source whose key is
# currently invalid in some environments, causing `apt-get update` to fail.
RUN rm -f /etc/apt/sources.list.d/yarn.list /usr/share/keyrings/yarn-archive-keyring.gpg \
    && apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    wget \
    build-essential \
    libpq-dev \
    postgresql-client \
    graphviz \
    && rm -rf /var/lib/apt/lists/*

# Node.js (required by Codex and tooling)
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && npm install -g npm@latest \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies globally for quick access
WORKDIR /tmp

# Environment optimization
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PIP_NO_CACHE_DIR=1

# Base Python tools
RUN pip install --upgrade pip setuptools wheel && \
    pip install \
    pytest==7.4.0 \
    pytest-asyncio==0.21.1 \
    pytest-cov==4.1.0 \
    alembic==1.12.0 \
    asyncpg==0.31.0 \
    sqlalchemy==2.0.23 \
    psycopg2-binary==2.9.9 \
    python-dotenv==1.0.1 \
    pydantic==2.10.4 \
    httpx==0.25.0 \
    click==8.1.7 \
    rich==13.7.0 \
    black==23.11.0 \
    ruff==0.1.7 \
    mypy==1.7.1

# Workspace setup
WORKDIR /workspace

# Copy requirements (if changing during build)
COPY requirements/ ./requirements/

# Install project dependencies
RUN pip install -r requirements/base.txt 2>/dev/null || echo "⚠️ base.txt not fully installed"

# Copy initialization script
COPY .devcontainer/init.sh /workspace/.devcontainer/init.sh
RUN chmod +x /workspace/.devcontainer/init.sh

# Environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    COLUMN=200

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)" || exit 1

# Default command
CMD ["/bin/bash"]
