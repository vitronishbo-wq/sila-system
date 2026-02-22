# SILA System - Organized & Corrected Project Commands

**Generated**: November 18, 2025 **Status**: ✅ Validated & Organized **Mode**: IDE
Compatible (PowerShell/Bash)

---

## 📋 Table of Contents

1. [Environment Setup & Initialization](#1-environment-setup--initialization)
2. [Database & Migration Commands](#2-database--migration-commands)
3. [Development Stack Commands](#3-development-stack-commands)
4. [Testing & Validation](#4-testing--validation)
5. [Deployment & Production](#5-deployment--production)
6. [Maintenance & Cleanup](#6-maintenance--cleanup)
7. [Execution Flow & Sequence](#7-execution-flow--sequence)

---

## 1. Environment Setup & Initialization

### 1.1 Initial Project Setup (PowerShell)

```powershell
# Initialize project structure with validation
# Path: ./init_project.ps1
# Prerequisites: None
# Expected Output: Directory structure created, initial files generated

.\init_project.ps1

# Alternative with detailed output
.\init_project.ps1 -Verbose
```

**Corrections Applied:**

- ✅ Proper array handling in PowerShell
- ✅ Directory creation with `-Force` flag
- ✅ File encoding set to UTF8 explicitly
- ✅ Error handling with try-catch blocks

---

### 1.2 Environment Configuration (Bash/PowerShell)

```bash
# Option A: Bash - Complete environment variables
# Path: ./complete_env.sh
# Adds missing variables to .env, creates if missing
chmod +x ./complete_env.sh
./complete_env.sh complete

# Validate environment after completion
./complete_env.sh validate
```

```powershell
# Option B: PowerShell - Setup environment
# Path: ./setup_env.ps1
# Creates backend directory structure and configuration

.\setup_env.ps1
```

**Corrections Applied:**

- ✅ Script executable permissions set in Bash
- ✅ Proper error handling with `set -e`
- ✅ Color codes validated for terminal output
- ✅ UTF8 encoding enforced in PowerShell

---

### 1.3 Environment File Preparation

```bash
# Create initial .env file from template
cp .env.example .env

# Complete missing variables (production-ready)
./complete_env.sh complete

# Validate critical variables exist
./complete_env.sh validate
```

**Expected Variables Created:**

- Database: `POSTGRES_PASSWORD`, `POSTGRES_HOST`, `POSTGRES_DB`
- Redis: `REDIS_URL`, `REDIS_PASSWORD`
- MinIO: `MINIO_ENDPOINT`, `MINIO_ACCESS_KEY`
- Monitoring: `GRAFANA_PASSWORD`, `SENTRY_DSN`
- Feature Flags: `FEATURE_AUTO_HEALER`, `FEATURE_MONITORING`

---

## 2. Database & Migration Commands

### 2.1 Database Initialization

```python
# Python - Initialize database tables
# Path: ./init_db.py
# Prerequisites: Environment configured, Docker DB running

python init_db.py
```

**Expected Output:**

```
✅ Database tables created successfully
Tables initialized from SQLAlchemy models
```

---

### 2.2 SQL Database Setup

```bash
# Initialize with SQL script (if using custom initialization)
# Path: ./ensure_databases.sql
# Run from PostgreSQL container or psql client

psql -U postgres -d sila_dev -f ensure_databases.sql

# Or via Docker Compose
docker compose exec db psql -U postgres -d sila_dev -f /scripts/ensure_databases.sql
```

---

### 2.3 Admin User Setup

```bash
# Initialize admin account
# Path: ./setup_admin.sql

psql -U postgres -d sila_dev -f setup_admin.sql
```

---

## 3. Development Stack Commands

### 3.1 Start Development Environment (Bash)

```bash
# Smart development startup with auto-detection
# Path: ./start_sila.sh
# Detects environment and starts appropriate services

chmod +x start_sila.sh
./start_sila.sh dev

# Or production mode
./start_sila.sh prod

# With backup of configurations
./start_sila.sh dev --backup
```

**Expected Output:**

```
╔═══════════════════════════════════════════════════════════╗
║                    🚀 SILA SYSTEM 3.0                    ║
║              Docker Compose Unificado e Inteligente      ║
╚═══════════════════════════════════════════════════════════╝

✅ SILA SYSTEM INICIADO
📋 Informações do Sistema:
   Modo: development
   Timestamp: [timestamp]

🌐 URLs Disponíveis:
   Frontend (Dev): http://localhost:5173
   Frontend (Prod): http://localhost
   Backend API: http://localhost:8000
   API Docs: http://localhost:8000/docs
```

---

### 3.2 Start Development Environment (PowerShell)

```powershell
# Unified PowerShell development startup
# Path: ./dev-up.ps1
# Handles Docker Compose with hot-reload

.\dev-up.ps1 -Mode dev

# Production mode
.\dev-up.ps1 -Mode prod

# With audit checks
.\dev-up.ps1 -Mode dev
```

**Features:**

- ✅ Automatic Docker Compose detection
- ✅ npm audit for frontend dependencies
- ✅ pip-audit for Python dependencies
- ✅ Comprehensive logging with timestamps

---

### 3.3 Stop Development Environment

```powershell
# Path: ./down.ps1
# Stops all running containers

.\down.ps1 -Mode dev
# Or for production
.\down.ps1 -Mode prod
```

---

### 3.4 Docker Compose Operations (Make)

```bash
# Start development stack (via Make)
make up-dev

# Start production stack (via Make)
make up

# View running services
make ps

# Follow logs in real-time
make logs

# Restart services
make restart

# Stop all services
make down

# Stop and remove volumes
make down-v
```

---

## 4. Testing & Validation

### 4.1 Run All Tests (PowerShell)

```powershell
# Path: ./run-tests.ps1
# Executes backend test suite with UTF-8 support

.\run-tests.ps1

# Expected output shows test results and coverage
```

---

### 4.2 Run Tests via Make

```bash
# Execute all tests with coverage
make test

# Verbose test output
make test-verbose

# Fast fail mode (stops at first failure)
make test-fast

# Without coverage report
make test-nocov

# Docker-based tests
make test-docker

# Open coverage report
make open-report
```

---

### 4.3 Backend Testing (Direct)

```bash
# Using Python directly (if running locally)
python -m pytest backend/tests -v --cov=backend/app

# With specific test file
python -m pytest backend/tests/unit/test_models.py -v
```

---

### 4.4 Project Structure Validation

```bash
# Validate complete project structure
make validate

# Validate structure only
make validate-structure

# Validate dependencies
make validate-deps

# Validate Docker configuration
make validate-docker

# Run all CI checks locally
make validate-local
```

---

## 5. Deployment & Production

### 5.1 Quick Deployment

```bash
# Path: ./quick_deploy.sh
chmod +x quick_deploy.sh
./quick_deploy.sh

# Expected: Builds, tests, and deploys
```

---

### 5.2 Production Deploy via Make

```bash
# Quick production deployment
make deploy-quick

# Full deployment pipeline
make deploy
```

---

### 5.3 Database Migrations

```bash
# Using Alembic (if configured)
alembic upgrade head  # Apply all pending migrations
alembic upgrade +1    # Apply one migration
alembic downgrade -1  # Rollback one migration

# Via Make
make migrate          # Apply migrations
make migrate-rev      # Create new migration
```

---

## 6. Maintenance & Cleanup

### 6.1 Clean Temporary Files

```bash
# Path: ./cleanup_temp_files.sh
chmod +x cleanup_temp_files.sh
./cleanup_temp_files.sh

# This removes:
# - __pycache__ directories
# - .pytest_cache
# - *.log files
# - .env temporary files
```

---

### 6.2 Project Cleanup

```bash
# Comprehensive cleanup
chmod +x cleanup_project.sh
./cleanup_project.sh

# Includes: Backups cleanup, cache clearing, log rotation
```

---

### 6.3 Cache Management

```bash
# Clean Python cache
make clean-cache

# Pre-commit cleanup
make precommit-clean
```

---

### 6.4 Database Utilities

```bash
# Shell access to PostgreSQL container
make db-shell

# Backend application shell
make backend-shell

# Initialize databases
make db-init
```

---

## 7. Execution Flow & Sequence

### ✅ Recommended Execution Sequence for Fresh Project

```bash
# === STEP 1: Environment & Prerequisites (5-10 min) ===
# 1.1 Initialize project structure
.\init_project.ps1

# 1.2 Prepare environment file
cp .env.example .env
./complete_env.sh complete
./complete_env.sh validate

# === STEP 2: Infrastructure Setup (10-15 min) ===
# 2.1 Start Docker infrastructure
./start_sila.sh dev

# OR via Make
make up-dev

# 2.2 Initialize databases
python init_db.py

# 2.3 Setup admin account
psql -U postgres -d sila_dev -f setup_admin.sql

# === STEP 3: Validation (5 min) ===
# 3.1 Validate project structure
make validate-structure

# 3.2 Run quick test
make test-fast

# === STEP 4: Development Ready (ready for coding) ===
# 4.1 Monitor services
make ps

# 4.2 Check logs if issues
make logs

# 4.3 Access endpoints
# Frontend: http://localhost:5173 (dev) or http://localhost (prod)
# Backend: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

---

### ⚠️ Troubleshooting Sequence

```bash
# If services don't start properly:

# 1. Check container status
make ps
docker ps -a

# 2. View logs
make logs
make logs | grep -i error

# 3. Clean and restart
make down-v
make up-dev

# 4. Validate environment
./complete_env.sh validate

# 5. Check dependencies
make validate-deps

# 6. Run diagnostics (if available)
make structure-guard
```

---

## 📊 Command Statistics

| Category           | Count   | Status           |
| ------------------ | ------- | ---------------- |
| Bash Scripts       | 8+      | ✅ Validated     |
| PowerShell Scripts | 6+      | ✅ Validated     |
| Make Targets       | 40+     | ✅ Validated     |
| Python Scripts     | 5+      | ✅ Validated     |
| SQL Scripts        | 2+      | ✅ Validated     |
| **Total**          | **60+** | ✅ **Organized** |

---

## 🔧 Corrections Applied

### Syntax Errors Fixed

- ✅ Proper escape sequences in PowerShell
- ✅ Array handling in bash vs PowerShell
- ✅ UTF8 encoding enforced across all scripts
- ✅ Error handling consistency
- ✅ Log file path normalization

### Logic Improvements

- ✅ Dependency checks before execution
- ✅ Validation of required files and directories
- ✅ Proper error exit codes
- ✅ Comprehensive logging output
- ✅ Resource cleanup in finally blocks

### IDE Compatibility

- ✅ PowerShell: Set-ExecutionPolicy compatible
- ✅ Bash: POSIX-compliant where possible
- ✅ Make: Compatible with standard Make tools
- ✅ Python: Python 3.8+ compatible

---

## 📝 Notes for IDE Execution

### For VS Code Terminal:

```bash
# Make sure you're in the correct directory
cd \\wsl$\Ubuntu\home\truman\dev\sila-system

# Run commands directly
./start_sila.sh dev
make test
make logs
```

### For PowerShell (Windows):

```powershell
# Set execution policy if needed
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Navigate to project
cd "C:\path\to\sila-system"

# Run scripts
.\dev-up.ps1 -Mode dev
.\run-tests.ps1
```

---

## ✨ Command Execution Priority

**Tier 1 - Critical (Run First)**

1. `./init_project.ps1` - Project initialization
2. `./complete_env.sh validate` - Environment validation
3. `./start_sila.sh dev` or `.\dev-up.ps1` - Infrastructure startup

**Tier 2 - Standard (Run After Tier 1)**

1. `python init_db.py` - Database initialization
2. `make test` - Run tests
3. `make validate-structure` - Validate structure

**Tier 3 - Optional (Run as Needed)**

1. `make deploy-quick` - Deployment
2. `./cleanup_project.sh` - Cleanup
3. `make logs` - Monitoring

---

## 📞 Support & Debugging

If commands fail:

1. Check prerequisites (Docker, Python version, Node.js)
2. Validate environment variables: `./complete_env.sh validate`
3. Review logs in `./logs/` directory
4. Run `make validate-local` for comprehensive check
5. Consult script headers for detailed documentation

---

**Last Updated**: November 18, 2025 **Status**: Production Ready **Version**: 3.5
