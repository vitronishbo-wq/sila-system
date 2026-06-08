# ==============================================================================
# SILA System - Enterprise Management & Architecture Governance
# ==============================================================================
SHELL := /usr/bin/env bash
.DEFAULT_GOAL := help

# Paths e Estrutura
ROOT_DIR        := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))
BACKEND_DIR     := apps/backend
MODULES_ROOT    := $(BACKEND_DIR)/app/modules
REPORTS_DIR     := reports
DOCS_DIR        := docs
SCRIPTS_DIR     := scripts
MODULO          ?= apps/backend/app/processes/nascimento_bi_nif_ss

# Scripts de Guardrail
CHECK_MACRO     := $(SCRIPTS_DIR)/guardrails/check_macro_boundaries_final.py
CHECK_DEPS      := $(SCRIPTS_DIR)/guardrails/check_domain_dependencies.py
CHECK_CYCLES    := $(SCRIPTS_DIR)/guardrails/check_cycles.py
ARCH_COMPILER   := $(SCRIPTS_DIR)/arch_compiler.py
GEN_GRAPH       := $(SCRIPTS_DIR)/module_dependency_analysis.py
ARCH_SYNC       := $(SCRIPTS_DIR)/architecture/universalize_modules.sh
NORM_V2         := $(SCRIPTS_DIR)/architecture/normalize_modules_v2.sh
POLICY_YAML     := $(DOCS_DIR)/architecture/domain_dependency_policy.yaml
ARCH_AUDIT_DIR  := $(SCRIPTS_DIR)/architecture/audit
ARCH_FIX_SCRIPT := $(SCRIPTS_DIR)/architecture/fix/replace_core_imports.sh
DEV_ENV_LOADER  := $(SCRIPTS_DIR)/dev/load_runtime_env.sh
RUN_LOCAL_SH    := $(SCRIPTS_DIR)/dev/run_local.sh

# Binários
PYTHON          := python3
BACKEND_PYTHON  := $(BACKEND_DIR)/.venv/bin/python

.PHONY: help setup audit-domains audit-macro generate-graph compile-manifests check-cycles validate-policy audit-full sovereign-ritual architecture-report context-map scaffold-module architecture-sync arch-audit arch-fix daily-audit clean-audit consolidate-audit seed-test-db fix-npm-workspaces cleanup-root cleanup-root-preview cleanup-root-auto clean devcontainer-build devcontainer-up devcontainer-down infra-up infra-down env-print run-local pipeline test lint lint-fix format registry-check registry-cache-clear db-migrate db-rollback db-backup db-restore db-reset db-reset-full codex-agent

help:
	@echo "🚀 SILA System - Gestão de Arquitetura + Dev Autonomy"
	@echo ""
	@echo "=== DevContainer & Pipeline (NOVO) ==="
	@echo "  make dev-setup        -> Build container + start stack + migrate DB"
	@echo "  make dev-clean        -> Stop container + clean artifacts"
	@echo "  make devcontainer-up  -> Start docker-compose stack"
	@echo "  make devcontainer-down -> Stop docker-compose stack"
	@echo "  make infra-up         -> Start local PostgreSQL + Redis only"
	@echo "  make infra-down       -> Stop local PostgreSQL + Redis only"
	@echo "  make env-print        -> Show resolved host/container runtime env"
	@echo "  make run-local        -> Start infra + migrate + backend + frontend"
	@echo "  make pipeline         -> registry-check → lint-fix → lint → migrate → test → audit"
	@echo ""
	@echo "=== Self-Healing Pipeline (100% Autonomy) ==="
	@echo "  make post-mutation-pipeline -> ruff fix + black + pytest (auto-run after changes)"
	@echo "  make migration-guardrail    -> alembic upgrade head (with validation + guard-rails)"
	@echo "  make watch-mode             -> Auto-run tests on .py changes (requires watchdog)"
	@echo ""
	@echo "=== Database Operations ==="
	@echo "  make db-migrate       -> Run Alembic migrations (upgrade head)"
	@echo "  make db-rollback      -> Rollback last migration"
	@echo "  make db-reset         -> Full reset (downgrade base → upgrade head)"
	@echo "  make db-backup        -> Cria snapshot SQL completo em backups/"
	@echo "  make db-restore file=backups/arquivo.sql -> Restaura um dump SQL"
	@echo "  make db-reset-full    -> Recria o volume do Postgres e restaura backups/latest.sql"
	@echo ""
	@echo "=== Testing & Quality ==="
	@echo "  make test             -> Run pytest with coverage"
	@echo "  make lint-fix         -> Ruff fix + format"
	@echo "  make lint             -> Ruff check + format --check"
	@echo "  make format           -> Ruff formatter"
	@echo "  make registry-check   -> Smoke check ALL_MODELS registry"
	@echo "  make registry-cache-clear -> Clear registry discovery cache"
	@echo ""
	@echo "=== Codex Agent (Full Autonomy) ==="
	@echo "  make codex-agent      -> Start Codex in (approval_policy=never) mode"
	@echo ""
	@echo "=== Architecture Audit ==="
	@echo "  make audit-domains    -> Executa auditoria completa (Scan + Comparação)"
	@echo "  make audit-macro      -> Valida fronteiras de macro-domínios (Física)"
	@echo "  make generate-graph   -> Escaneia o código e gera o grafo observado"
	@echo "  make compile-manifests -> Compila contratos module.yaml em grafo de manifestos"
	@echo "  make check-cycles     -> Bloqueia dependências circulares conforme política YAML"
	@echo "  make validate-policy  -> Valida grafo observado contra arquitetura + política YAML"
	@echo "  make audit-full       -> generate-graph → compile-manifests → audit-macro → check-cycles → validate-policy"
	@echo "  make sovereign-ritual -> architecture-report → run_all_guardrails → check_domain_dependencies"
	@echo ""
	@echo "=== Documentation ==="
	@echo "  make context-map       -> Gera docs/architecture/context_map.md via grafo observado"
	@echo "  make scaffold-module   -> Executa scaffold interativo de módulo + auto-registro no grafo"
	@echo "  make architecture-sync -> Universaliza estrutura dos macro-domínios + compila manifests"
	@echo "  make arch-audit       -> Auditoria arquitetural E2E em lote (compliance/ciclos/colisões)"
	@echo "  make arch-fix         -> Normalização universal + auto-fix imports + arch-audit"
	@echo "  make daily-audit      -> 🕐 Ritual Diário: 5 validadores + relatório consolidado"
	@echo ""
	@echo "=== Cleanup ==="
	@echo "  make cleanup-root-preview -> Lista o que será removido (preview)"
	@echo "  make cleanup-root-force   -> Executa a limpeza pesada (CUIDADO)"
	@echo "  make check-leaks          -> Procura lógica sensível antes da purga"
	@echo "  make clean            -> Remove caches e relatórios temporários"
	@echo ""
	@echo "=== Setup ==="
	@echo "  make setup            -> Prepara o ambiente e dependências"
	@echo "  make fix-npm-workspaces -> Repara colisões de workspaces e reinstala npm"
	@echo ""

# --- 1. Fluxo de Auditoria (A Ordem Perfeita) ---

# Gera o JSON de dependências reais lendo o código fonte
generate-graph:
	@mkdir -p $(REPORTS_DIR)
	@echo "🔍 [Scanner] Analisando dependências no código fonte..."
	@$(PYTHON) $(GEN_GRAPH) \
		--modules-root $(MODULES_ROOT) \
		--output-md $(REPORTS_DIR)/module_dependencies.md \
		--output-json $(REPORTS_DIR)/module_dependency_graph.json

compile-manifests:
	@mkdir -p $(REPORTS_DIR)
	@echo "📦 [Compiler] Compilando contratos module.yaml..."
	@$(PYTHON) $(ARCH_COMPILER) --output $(REPORTS_DIR)/module_manifest_graph.json

# Valida as fronteiras lógicas dos 7 Macro-domínios
audit-macro:
	@echo "🛡️ [Guardrail] Validando fronteiras de Macro-domínios..."
	@$(PYTHON) $(CHECK_MACRO) --fail-on-violation

# Alvo principal: Faz o scan primeiro, depois compara com a arquitetura declarada
audit-domains: generate-graph compile-manifests audit-macro
	@$(MAKE) architecture-report
	@echo "📊 [Guardrail] Cruzando Código Real vs. Grafo de Arquitetura..."
	@$(PYTHON) $(CHECK_DEPS) \
		--observed-json $(REPORTS_DIR)/module_dependency_graph.json \
		--declared-graph $(DOCS_DIR)/AI_ARCHITECTURE_GRAPH.yaml \
		--policy-yaml $(POLICY_YAML) \
		--report-output $(REPORTS_DIR)/domain_dependency_guardrail_report.md \
		--repo-root .

check-cycles:
	@echo "🔁 [Guardrail] Verificando ciclos de dependência..."
	@$(PYTHON) $(CHECK_CYCLES) \
		--observed-json $(REPORTS_DIR)/module_dependency_graph.json \
		--policy-yaml $(POLICY_YAML)

validate-policy:
	@echo "📜 [Guardrail] Validando política arquitetural..."
	@$(PYTHON) $(CHECK_DEPS) \
		--observed-json $(REPORTS_DIR)/module_dependency_graph.json \
		--declared-graph $(DOCS_DIR)/AI_ARCHITECTURE_GRAPH.yaml \
		--policy-yaml $(POLICY_YAML) \
		--report-output $(REPORTS_DIR)/domain_dependency_guardrail_report.md \
		--repo-root .

audit-full: generate-graph compile-manifests audit-macro check-cycles validate-policy
	@echo "✅ Auditoria full concluída."

sovereign-ritual: architecture-report
	@echo "🕰️  [Ritual] Executando protocolo soberano..."
	@bash scripts/guardrails/run_all_guardrails.sh
	@$(PYTHON) $(CHECK_DEPS) --repo-root . --policy-yaml $(POLICY_YAML)
	@echo "✅ Ritual soberano concluído."

# Gera o relatório MD final de saúde do sistema
architecture-report:
	@echo "📝 [Report] Gerando inventário e saúde dos domínios..."
	@$(PYTHON) $(SCRIPTS_DIR)/migration_domain_inventory.py --output $(REPORTS_DIR)/migration_domain_inventory.md
	@$(PYTHON) $(SCRIPTS_DIR)/ai/generate_architecture_graph.py
	@echo "✅ Auditoria concluída. Relatório em: $(REPORTS_DIR)/"

context-map:
	@echo "🗺️  [Docs] Gerando context map..."
	@$(PYTHON) $(SCRIPTS_DIR)/architecture/generate_context_map.py \
		--graph-json $(REPORTS_DIR)/module_dependency_graph.json \
		--output $(DOCS_DIR)/architecture/context_map.md

# ==============================================================================
# SILA SYSTEM - AUTOMATED INDEXING RITUAL
# ==============================================================================
.PHONY: update-indexes

update-indexes:
	@echo "[SILA] A iniciar atualização cirúrgica dos índices..."
	@python3 scripts/generate_indexes.py $(MODULO)
	@echo "[SILA] Índices tree.md e tree.modules.txt sincronizados com sucesso."

scaffold-module:
	@$(PYTHON) $(SCRIPTS_DIR)/create_domain_module.py

architecture-sync:
	@echo "🧩 [Sync] Universalizando estrutura dos módulos..."
	@bash $(ARCH_SYNC)
	@$(MAKE) compile-manifests

arch-audit:
	@mkdir -p $(REPORTS_DIR)
	@echo "🧪 [E2E] Executando full architecture audit..."
	@$(PYTHON) $(ARCH_AUDIT_DIR)/full_arch_audit.py \
		--modules-root $(MODULES_ROOT) \
		--report-output $(REPORTS_DIR)/architecture_audit.md \
		--json-output $(REPORTS_DIR)/architecture_audit.json
	@echo "🔁 [E2E] Escaneando circularidade..."
	@$(PYTHON) $(ARCH_AUDIT_DIR)/circular_dependency_scan.py \
		--modules-root $(MODULES_ROOT) \
		--output $(REPORTS_DIR)/circular_dependency_scan.md
	@echo "🧬 [E2E] Escaneando colisão de entidades..."
	@$(PYTHON) $(ARCH_AUDIT_DIR)/entity_collision_scan.py \
		--modules-root $(MODULES_ROOT) \
		--output $(REPORTS_DIR)/entity_collision_scan.md
	@echo "✅ E2E arch-audit concluído."

arch-fix:
	@echo "⚙️  [E2E] Normalização universal + auto-fix em lote..."
	@bash $(NORM_V2)
	@bash $(ARCH_FIX_SCRIPT)
	@$(MAKE) arch-audit

daily-audit:
	@echo "🕐 [Ritual] Executando auditoria diária..."
	@mkdir -p $(REPORTS_DIR)/daily_audit
	@$(MAKE) update-indexes
	@bash $(SCRIPTS_DIR)/daily_audit.sh
	@$(PYTHON) $(SCRIPTS_DIR)/consolidate_audit.py

clean-audit:
	@echo "🧹 [Ritual] Limpando artefatos de auditoria diária..."
	@rm -rf $(REPORTS_DIR)/daily_audit/*
	@rm -f $(REPORTS_DIR)/domain_dependency_guardrail_report.md
	@rm -f platform/storage/reports/domain_dependency_guardrail_report.md

consolidate-audit:
	@echo "📊 [Consolidação] Gerando relatório consolidado..."
	@$(PYTHON) $(SCRIPTS_DIR)/consolidate_audit.py
	@echo "✅ Relatório consolidado: $(REPORTS_DIR)/daily_audit.md"

seed-test-db:
	@echo "🌱 [Seed] Preparando dataset mínimo para testes de integração..."
	@RUN_DB_INTEGRATION=1 bash $(SCRIPTS_DIR)/seed_test_db.sh

# --- 2. Setup e Manutenção ---

setup:
	@echo "🔧 Preparando ambiente..."
	@mkdir -p $(REPORTS_DIR)
	@test -d $(BACKEND_DIR)/.venv || $(PYTHON) -m venv $(BACKEND_DIR)/.venv
	@$(BACKEND_DIR)/.venv/bin/pip install -q pyyaml pytest ruff
	@echo "✅ Setup concluído."

fix-npm-workspaces:
	@echo "🔧 Reparando estrutura de workspaces NPM..."
	@bash $(SCRIPTS_DIR)/fix_npm_workspaces.sh
	@echo "✅ NPM Workspaces reparados com sucesso."

clean:
	@echo "🧹 Limpando artefatos..."
	@rm -rf $(REPORTS_DIR)/*
	@find . -type d -name "__pycache__" -exec rm -rf {} +

# --- 3. Limpeza de Artefatos (Extensões vs. Scope) ---

cleanup-root-preview:
	@echo "--- Ficheiros Fantasmas Detectados ---"
	@find . -maxdepth 1 -type f -name "*.json" -not -name "package.json"
	@find . -maxdepth 1 -type f -name "*.csv"
	@echo "--- Directórios Fora de Escopo ---"
	@ls -d docs/architecture docs/archive docs/templates 2>/dev/null || echo "Limpo"

cleanup-root:
	@echo "🧹 Removendo artefatos phantom do diretório raiz..."
	@$(PYTHON) $(SCRIPTS_DIR)/cleanup_artifacts.py

cleanup-root-auto:
	@echo "🧹 Removendo automaticamente todos os artefatos phantom..."
	@$(PYTHON) $(SCRIPTS_DIR)/cleanup_artifacts.py --auto

cleanup-root-force:
	@echo "🚀 Iniciando purga atômica..."
	@rm -rf $(ROOT_DIR)/docs/architecture
	@rm -rf $(ROOT_DIR)/docs/archive
	@rm -rf $(ROOT_DIR)/docs/templates
	@rm -rf $(ROOT_DIR)/src
	@find . -maxdepth 1 -type f -name "DUPLICATION_*" -delete
	@find . -maxdepth 1 -type f -name "CONSOLIDATION_*" -delete
	@echo "✅ Autonomia restaurada. Terreno limpo."

check-leaks:
	@echo "🔍 Minerando lógica sensível antes da purga..."
	@grep -rliE "NIF|BI|provincia|municipio" $(DOCS_DIR) || echo "Nenhum dado sensível encontrado."

# ============================================================================
# DevContainer & CI/CD Pipeline (Codex Full Autonomy Mode)
# ============================================================================

devcontainer-build:
	@echo "🐳 Building DevContainer..."
	@docker compose -f .devcontainer/docker-compose.yml build --no-cache

devcontainer-up:
	@echo "🚀 Starting DevContainer stack..."
	@docker compose -f .devcontainer/docker-compose.yml up -d
	@echo "✅ Services running:"
	@echo "   - App container: sila-dev-agent"
	@echo "   - PostgreSQL: localhost:5432"
	@echo "   - Redis: localhost:6379"

devcontainer-down:
	@echo "⛔ Stopping DevContainer stack..."
	@docker compose -f .devcontainer/docker-compose.yml down

infra-up:
	@echo "🚀 Starting local infra (PostgreSQL + Redis)..."
	@docker compose -f .devcontainer/docker-compose.yml up -d db redis
	@echo "✅ Infra running on localhost:5432 and localhost:6379"

infra-down:
	@echo "⛔ Stopping local infra (PostgreSQL + Redis)..."
	@docker compose -f .devcontainer/docker-compose.yml stop db redis

env-print:
	@$(DEV_ENV_LOADER) "$${ENV_MODE:-auto}" --print

# === Database Operations ===

db-migrate:
	@echo "🔄 Running database migrations..."
	@bash -lc 'source "$(ROOT_DIR)/.venv/bin/activate" && eval "$$($(DEV_ENV_LOADER) "$${ENV_MODE:-auto}")" && cd $(BACKEND_DIR) && alembic upgrade head'
	@echo "✅ Migrations complete"

db-rollback:
	@echo "⏮️  Rolling back last migration..."
	@bash -lc 'source "$(ROOT_DIR)/.venv/bin/activate" && eval "$$($(DEV_ENV_LOADER) "$${ENV_MODE:-auto}")" && cd $(BACKEND_DIR) && alembic downgrade -1'
	@echo "✅ Rollback complete"

db-reset:
	@echo "🔄 Resetting database..."
	@bash -lc 'source "$(ROOT_DIR)/.venv/bin/activate" && eval "$$($(DEV_ENV_LOADER) "$${ENV_MODE:-auto}")" && cd $(BACKEND_DIR) && alembic downgrade base && alembic upgrade head'
	@echo "✅ Database reset complete"

db-backup:
	@bash $(SCRIPTS_DIR)/db_backup.sh

db-restore:
	@if [ -z "$(file)" ]; then \
		echo "❌ Uso: make db-restore file=backups/full_YYYYMMDD_HHMMSS.sql"; \
		exit 1; \
	fi
	@bash $(SCRIPTS_DIR)/db_restore.sh "$(file)"

db-reset-full:
	@if [ -n "$(file)" ]; then \
		bash $(SCRIPTS_DIR)/db_reset_full.sh "$(file)"; \
	else \
		bash $(SCRIPTS_DIR)/db_reset_full.sh; \
	fi

# === Testing & Quality ===

test:
	@echo "🧪 Running test suite..."
	@if python3 -c "import pytest_cov" >/dev/null 2>&1; then \
		pytest -v --cov=apps/backend/app --cov-report=html tests/; \
	else \
		echo "⚠️ pytest-cov não instalado; executando testes sem cobertura"; \
		pytest -v tests/; \
	fi
	@echo "✅ Tests complete"

lint:
	@echo "🔍 Running linters..."
	@ruff check . && ruff format --check .
	@echo "✅ Lint complete"

lint-fix:
	@echo "🧹 Auto-fixing lint..."
	@ruff check --fix --unsafe-fixes . && ruff format .
	@echo "✅ Lint fix complete"

format:
	@echo "🎨 Formatting code..."
	@ruff format .
	@echo "✅ Format complete"

registry-check:
	@echo "🧭 Running registry smoke check..."
	@cd $(BACKEND_DIR) && SILA_REGISTRY_SMOKE_CHECK=1 $(PYTHON) -c "from app.db.registry import smoke_check_all_models"
	@echo "✅ Registry check complete"

registry-cache-clear:
	@echo "🧹 Clearing registry cache..."
	@rm -f $(BACKEND_DIR)/app/db/registry/.cache/registry_modules.json
	@echo "✅ Registry cache cleared"

# === Post-Mutation Pipeline (Self-Healing Code Agent) ===

post-mutation-pipeline:
	@echo "🔄 Executing post-mutation pipeline..."
	@echo "   (ruff fix → black → pytest)"
	@bash $(SCRIPTS_DIR)/post-mutation-pipeline.sh

migration-guardrail:
	@echo "🔐 Executing migration guardrail..."
	@echo "   (alembic upgrade head with validation)"
	@bash $(SCRIPTS_DIR)/migration-guardrail.sh

# Watch mode (requires watchdog: pip install watchdog pyaml)
watch-mode:
	@echo "👁️  Starting watch mode (auto-run tests on Python changes)..."
	@watchmedo auto-restart --patterns="*.py" --recursive --ignore-patterns="__pycache__|.venv|dist|build" -- \
		python -m pytest tests/ -v --tb=short
	@echo "✅ Watch mode enabled"

# === Main Pipeline (Build → Migrate → Test) ===

pipeline:
	set -e
	$(MAKE) registry-check
	$(MAKE) lint-fix
	$(MAKE) lint
	$(MAKE) db-migrate
	$(MAKE) test
	$(MAKE) audit-full
	@echo ""
	@echo "🎉 PIPELINE COMPLETO!"
	@echo "✓ Code formatted & linted"
	@echo "✓ Database migrated"
	@echo "✓ Tests passed"
	@echo "✓ Architecture validated"
	@echo ""

# === Codex Agent (Full Autonomy Commands) ===

codex-agent:
	@echo "🤖 Starting Codex Agent in FULL AUTONOMY mode..."
	@echo "Commands:"
	@echo "  'implement JWT auth' -> Codex writes code, runs migrations, tests"
	@echo "  'add SPA service' -> Codex scaffolds, integrates, tests"
	@echo "  'refactor module X' -> Codex refactors, validates, commits"
	@echo ""
	@echo "Agent is now AUTONOMOUS - no approval needed"
	@echo ""

# === Development Shortcuts ===

dev-setup: devcontainer-build devcontainer-up db-migrate
	@echo "✅ Dev environment ready!"

dev-clean: devcontainer-down clean
	@echo "✅ Dev environment cleaned"

run-local:
	@ENV_MODE="$${ENV_MODE:-auto}" $(RUN_LOCAL_SH)

.PHONY: cleanup-root cleanup-root-preview cleanup-root-auto cleanup-root-force check-leaks
