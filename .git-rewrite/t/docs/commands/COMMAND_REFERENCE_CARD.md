# SILA System - Technical Command Reference Card

**Quick Access Guide** | Last Updated: November 18, 2025

---

## 🚀 One-Line Quick Start

```bash
# Development (choose one)
./start_sila.sh dev                    # Bash/Linux
.\dev-up.ps1 -Mode dev               # PowerShell/Windows
make up-dev                            # Make (cross-platform)
```

---

## 📦 Project Initialization Checklist

| Step  | Command                      | Expected Result             | Alternatives                  |
| ----- | ---------------------------- | --------------------------- | ----------------------------- |
| **1** | `.\init_project.ps1`         | Directory structure created | N/A                           |
| **2** | `cp .env.example .env`       | .env file created           | Manual creation               |
| **3** | `./complete_env.sh complete` | ENV vars populated          | `./complete_env.sh validate`  |
| **4** | `./start_sila.sh dev`        | Containers running          | `.\dev-up.ps1 -Mode dev`      |
| **5** | `python init_db.py`          | Database initialized        | SQL script via psql           |
| **6** | `make test-fast`             | Tests pass                  | `make test` for full coverage |

---

## 🔄 Common Workflows

### Development Cycle

```bash
# Terminal 1 - Start services
./start_sila.sh dev
# or
make up-dev

# Terminal 2 - Watch logs
make logs

# Terminal 3 - Run tests
make test-watch  # (if available)
# or run periodically
make test
```

### Test & Deploy

```bash
# Local validation
make validate-local

# Run tests
make test

# Quick deploy
make deploy-quick
# or
./quick_deploy.sh
```

### Cleanup & Reset

```bash
# Stop services
make down

# Clean everything
make down-v
./cleanup_project.sh

# Fresh start
make up-dev
```

---

## 🎯 Command Map by Use Case

### **Starting the Project**

```
Bash:        ./start_sila.sh dev
PowerShell:  .\dev-up.ps1 -Mode dev
Make:        make up-dev
```

### **Stopping the Project**

```
Make:        make down
PowerShell:  .\down.ps1 -Mode dev
Docker:      docker compose down
```

### **Testing**

```
All tests:           make test
Verbose:             make test-verbose
Fast fail:           make test-fast
Without coverage:    make test-nocov
Docker tests:        make test-docker
Coverage report:     make open-report
```

### **Database Operations**

```
Initialize:  python init_db.py
Setup admin: psql -U postgres -d sila_dev -f setup_admin.sql
Migrate:     make migrate
Rollback:    make migrate-rev
DB shell:    make db-shell
```

### **Validation & Quality**

```
Full validation:      make validate
Structure only:       make validate-structure
Dependencies:         make validate-deps
Docker config:        make validate-docker
Local CI pipeline:    make validate-local
Security audit:       make audit
```

### **Monitoring & Logs**

```
Container status:  make ps
Follow logs:       make logs
Nginx monitor:     make nginx-monitor
SILA monitor:      make monitor-sila
Audit snapshot:    make monitor-audit
```

### **Cleanup & Maintenance**

```
Temp files:        ./cleanup_temp_files.sh
Full project:      ./cleanup_project.sh
Cache:             make clean-cache
Pre-commit cache:  make precommit-clean
```

---

## ⚙️ Script Parameters & Options

### `start_sila.sh`

```bash
./start_sila.sh [MODE] [OPTIONS]

Modes:
  dev              Development mode (hot-reload)
  prod             Production mode (optimized)
  (empty)          Auto-detect

Options:
  --backup         Create backup before starting
  --help, -h       Show help
```

### `dev-up.ps1` / `down.ps1`

```powershell
.\dev-up.ps1 -Mode dev|prod
.\down.ps1 -Mode dev|prod

Parameters:
  -Mode dev        Development environment
  -Mode prod       Production environment
```

### `complete_env.sh`

```bash
./complete_env.sh [COMMAND]

Commands:
  complete         Complete .env with missing variables
  validate         Validate .env has required variables
  help             Show help message
```

### `test.ps1`

```powershell
.\test.ps1 [options]

Features:
  - UTF-8 encoding
  - Virtual environment activation
  - Error handling & logging
```

---

## 🔍 Validation Commands Quick Reference

```bash
# Check if project structure is valid
make structure-guard

# Validate all components
make validate

# Pre-commit hooks
make setup-precommit
make precommit-run
make precommit-report

# Linting & syntax
make check-python
make check-yaml
make check-syntax

# Auto-fixes
make fix-python
make fix-syntax
```

---

## 📊 Environment Variables Summary

### Database

```
POSTGRES_USER        = postgres
POSTGRES_PASSWORD    = S1l4D3v2025!Str0ng
POSTGRES_HOST        = db
POSTGRES_PORT        = 5432
POSTGRES_DB          = sila_dev
```

### Redis & Caching

```
REDIS_URL            = redis://sila-redis:6379/0
REDIS_PASSWORD       = S1l4R3d1s2025!Str0ng
CELERY_BROKER_URL    = redis://sila-redis:6379/1
CACHE_TTL_SECONDS    = 3600
```

### MinIO (S3 Compatible)

```
MINIO_ENDPOINT       = sila-minio:9000
MINIO_ACCESS_KEY     = sila_minio_admin
MINIO_SECRET_KEY     = S1l4M1n102025!Str0ng
MINIO_ROOT_USER      = sila_minio_admin
MINIO_ROOT_PASSWORD  = S1l4M1n102025!Str0ng
```

### Monitoring

```
GRAFANA_PASSWORD     = S1l4Gr4f4n42025!Str0ng
SENTRY_DSN           = (leave empty if unused)
PROMETHEUS_GATEWAY   = sila-prometheus:9090
JAEGER_ENDPOINT      = http://sila-jaeger:14268
```

### Application

```
ENVIRONMENT          = development|production
DEBUG                = true|false
LOG_LEVEL            = DEBUG|INFO|WARNING
PYTHONUNBUFFERED     = 1
PYTHONDONTWRITEBYTECODE = 1
```

---

## 🐛 Troubleshooting Quick Commands

```bash
# Container won't start?
docker compose logs [service_name]

# Port already in use?
lsof -i :[PORT]  # Linux/Mac
netstat -ano | findstr :[PORT]  # Windows

# Database connection error?
make db-shell
# or
psql -h localhost -U postgres -d sila_dev

# Tests failing?
make test-verbose
make test-fast  # Show first failure

# Permission issues?
chmod +x *.sh
chmod +x scripts/**/*.sh

# Cache issues?
make clean-cache
make precommit-clean
```

---

## 📍 Key Directories

| Directory         | Purpose                     |
| ----------------- | --------------------------- |
| `/backend`        | Backend API service         |
| `/frontend`       | Frontend React application  |
| `/infrastructure` | Docker & deployment configs |
| `/scripts`        | Automation scripts          |
| `/tests`          | Test suites                 |
| `/docs`           | Documentation               |
| `/logs`           | Application logs            |
| `/.git`           | Version control             |

---

## 🎯 Port Mapping Reference

| Service       | Default Port | Docker Port | Alternative |
| ------------- | ------------ | ----------- | ----------- |
| Frontend Dev  | 5173         | 5173        | 3000        |
| Frontend Prod | 80           | 80          | 8080        |
| Backend API   | 8000         | 8000        | 5000        |
| Database      | 5434         | 5432        | 5433        |
| Redis         | 6379         | 6379        | 6380        |
| Metrics       | 9111         | 9111        | 9090        |
| MinIO         | 9000         | 9000        | 9001        |
| Grafana       | 3000         | 3000        | 3001        |

---

## ✅ Pre-execution Checklist

- [ ] Docker installed and running
- [ ] Docker Compose available
- [ ] Python 3.8+ installed (for local dev)
- [ ] Node.js installed (for frontend dev)
- [ ] Git configured
- [ ] `.env.example` exists
- [ ] At least 2GB free disk space
- [ ] Ports 80, 8000, 5173 available

---

## 🔐 Security Best Practices

- Never commit `.env` file to version control
- Rotate credentials in production regularly
- Use strong passwords (already set in templates)
- Enable SSL/TLS in production (see `.env.production`)
- Keep dependencies updated: `make audit`
- Run pre-commit hooks: `make precommit-run`

---

## 📞 Error Resolution Flow

```
Error Occurs
    ↓
Check logs: make logs
    ↓
Validate environment: ./complete_env.sh validate
    ↓
Check dependencies: make validate-deps
    ↓
Validate structure: make validate-structure
    ↓
Run diagnostics: make structure-guard
    ↓
If database issue: make db-shell
    ↓
If container issue: docker compose logs [service]
    ↓
If still stuck: Clean & restart
    make down-v
    make up-dev
```

---

**💡 Tip**: Bookmark this file for quick reference during development!

**Version**: 3.5 | **Status**: ✅ Production Ready
