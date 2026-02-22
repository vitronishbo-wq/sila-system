# ================================
# SILA-System — Makefile principal
# ================================
# Este Makefile fornece comandos padronizados para executar testes,
# limpar relatórios, e rodar o ambiente de testes via Docker.

# Diretórios
PYTHON       ?= python3
SCRIPTS_DIR  := scripts
REPORTS_DIR  := reports
DOCKER_TEST  := docker-compose.test.yml
COMPOSE_FILE_MAIN := infrastructure/docker/docker-compose.yml
COMPOSE_FILE_DEV  := infrastructure/docker/docker-compose.dev.yml
DC := docker compose -f $(COMPOSE_FILE_MAIN)
DC_DEV := docker compose -f $(COMPOSE_FILE_MAIN) -f $(COMPOSE_FILE_DEV)

# Variáveis de ambiente (podem ser sobrescritas via CLI)
DATABASE_URL ?= postgresql://postgres:Truman1*Marcelo1*@localhost:5433/test_sila
SMTP_HOST    ?= localhost
SMTP_PORT    ?= 1025

# ===============================
# Targets principais de automação
# ===============================

.PHONY: help test test-verbose test-fast test-nocov test-docker test-clean reports-clean coverage open-report \
        up up-dev down down-v build rebuild logs ps restart up-backend up-frontend up-metrics up-cache \
        migrate migrate-rev db-shell backend-shell \
        start stop status deploy-quick env-prepare db-init nginx-monitor monitor-sila structure-guard \
        refactor-paths-dry refactor-paths-apply monitor-audit \
        validate validate-structure validate-deps validate-docker audit ci deps \
        setup-precommit setup-precommit-all precommit-update precommit-run precommit-report \
        validate-local check-yaml check-python fix-python check-syntax fix-syntax clean-cache precommit-clean

help:
	@echo ""
	@echo "📘 Comandos disponíveis:"
	@echo "  make test           → Executa todos os testes com coverage"
	@echo "  make test-verbose   → Executa testes em modo verboso"
	@echo "  make test-fast      → Executa testes com fail-fast"
	@echo "  make test-nocov     → Executa testes sem coverage"
	@echo "  make test-docker    → Executa suíte de testes dentro de containers"
	@echo "  make test-clean     → Limpa relatórios e resultados antigos"
	@echo "  make open-report    → Abre o relatório HTML de coverage"
	@echo ""
	@echo "🛠️  Orquestração e ambiente:"
	@echo "  make start          → Inicia o stack SILA via scripts/orchestration/start_sila.sh"
	@echo "  make stop           → Interrompe o stack SILA via scripts/orchestration/sila_stop.sh"
	@echo "  make status         → Mostra o estado do stack SILA"
	@echo "  make deploy-quick   → Deploy rápido usando scripts/orchestration/quick_deploy.sh"
	@echo "  make env-prepare    → Prepara ambiente local (.env, dependências básicas)"
	@echo "  make db-init        → Inicializa base de dados local"
	@echo "  make nginx-monitor  → Monitora Nginx via scripts/orchestration/nginx_monitor.sh"
	@echo "  make monitor-sila   → Monitorização leve do sistema SILA"
	@echo "  make monitor-audit  → Gera snapshot de monitorização + árvores de diretórios"
	@echo ""
	@echo "🛡️  Governança estrutural:"
	@echo "  make structure-guard     → Roda validações de paths/imports/.env"
	@echo "  make refactor-paths-dry  → Simula refactor de paths (sem escrever em disco)"
	@echo "  make refactor-paths-apply→ Aplica refactor de paths definido em migration/refactor_paths_v1.json"
	@echo ""
	@echo "✅ Pipeline de validação:"
	@echo "  make validate            → Validação completa (estrutura + deps + docker)"
	@echo "  make validate-structure  → Valida estrutura do projeto"
	@echo "  make validate-deps       → Valida requirements.txt"
	@echo "  make validate-docker     → Valida configuração Docker"
	@echo "  make audit               → Auditoria completa de dependências"
	@echo "  make ci                  → Pipeline completo para CI/CD"
	@echo "  make validate-local      → Pipeline de validação local (replica CI)"
	@echo ""
	@echo "🔧 Pre-commit hooks avançado:"
	@echo "  make setup-precommit     → Configura pre-commit hooks"
	@echo "  make setup-precommit-all → Configura e executa em todos os arquivos"
	@echo "  make precommit-update    → Atualiza versões dos hooks"
	@echo "  make precommit-run       → Executa todos os hooks manualmente"
	@echo "  make precommit-report    → Gera relatório consolidado"
	@echo "  make check-yaml          → Verifica sintaxe YAML dos arquivos"
	@echo "  make check-python        → Verifica sintaxe Python dos arquivos"
	@echo "  make fix-python          → Corrige automaticamente erros Python"
	@echo "  make check-syntax        → Verifica sintaxe de todos os arquivos"
	@echo "  make fix-syntax          → Corrige automaticamente erros de sintaxe"
	@echo "  make clean-cache         → Limpa diretórios de cache problemáticos"
	@echo "  make precommit-clean     → Limpa cache + executa pre-commit"
	@echo ""

# -------------------------------
# Execução local via run_tests.py
# -------------------------------

test:
	@echo "🚀 Executando testes com cobertura..."
	$(PYTHON) $(SCRIPTS_DIR)/run_tests.py --clean

test-verbose:
	@echo "🧩 Executando testes em modo detalhado..."
	$(PYTHON) $(SCRIPTS_DIR)/run_tests.py --clean -v

test-fast:
	@echo "⚡ Executando testes com fail-fast..."
	$(PYTHON) $(SCRIPTS_DIR)/run_tests.py --clean -x

test-nocov:
	@echo "🧮 Executando testes sem cobertura..."
	$(PYTHON) $(SCRIPTS_DIR)/run_tests.py --clean --no-coverage

# ----------------------------
# Execução em ambiente Docker
# ----------------------------

test-docker:
	@echo "🐳 Executando testes via Docker Compose..."
	DATABASE_URL=$(DATABASE_URL) docker compose -f $(DOCKER_TEST) up --build --abort-on-container-exit
	docker compose -f $(DOCKER_TEST) down -v

# -------------------------
# Limpeza e pós-processamento
# -------------------------

test-clean reports-clean:
	@echo "🧹 Limpando relatórios de testes..."
	rm -rf $(REPORTS_DIR)/*
	@mkdir -p $(REPORTS_DIR)/coverage/html

coverage:
	@echo "📊 Gerando badge e cobertura..."
	@if [ -f "$(REPORTS_DIR)/coverage/coverage.json" ]; then \
		$(PYTHON) $(SCRIPTS_DIR)/run_tests.py --no-parallel --no-coverage; \
	else \
		echo "⚠️  Nenhum arquivo de cobertura encontrado. Execute 'make test' primeiro."; \
	fi

open-report:
	@echo "🌐 Abrindo relatório HTML de cobertura..."
	@if [ -d "$(REPORTS_DIR)/coverage/html" ]; then \
		xdg-open $(REPORTS_DIR)/coverage/html/index.html >/dev/null 2>&1 || \
		open $(REPORTS_DIR)/coverage/html/index.html || \
		echo "📁 Relatório em: $(REPORTS_DIR)/coverage/html/index.html"; \
	else \
		echo "⚠️  Nenhum relatório HTML encontrado. Execute 'make test' primeiro."; \
	fi

# -------------------------
# Admin bootstrap targets
# -------------------------
create-admin:
	./scripts/auto_create_admin.sh

create-admin-force:
	# Allow passing FORCE_DELETE_EMAILS via: make create-admin-force FORCE_DELETE_EMAILS="a@x,b@x"
	FORCE_DELETE_EMAILS="$(FORCE_DELETE_EMAILS)" ./scripts/auto_create_admin.sh --force

revert-admin:
	./scripts/auto_create_admin.sh --revert

# -------------------------
# Docker Compose helpers
# -------------------------
up:
	$(DC) up -d

up-dev:
	$(DC_DEV) up -d

down:
	$(DC) down

down-v:
	$(DC) down -v

build:
	$(DC) build

rebuild:
	$(DC) build --no-cache

logs:
	$(DC) logs -f $(S)

ps:
	$(DC) ps

restart:
	$(DC) restart $(S)

up-backend:
	$(DC) --profile backend up -d backend db

up-frontend:
	$(DC) --profile frontend up -d frontend

up-metrics:
	$(DC) --profile metrics up -d metrics

up-cache:
	$(DC) --profile cache up -d redis

migrate:
	$(DC) exec backend sh -lc "alembic upgrade head"

migrate-rev:
	$(DC) exec backend sh -lc "alembic revision --autogenerate -m \"$(MSG)\""

db-shell:
	$(DC) exec db sh -lc "psql -U postgres -d sila_db"

backend-shell:
	$(DC) exec backend sh -lc "bash"

# -------------------------
# Orquestração e bootstrap
# -------------------------

start:
	@echo "🚀 Iniciando SILA via scripts/orchestration/start_sila.sh..."
	bash scripts/orchestration/start_sila.sh

stop:
	@echo "🛑 Parando SILA via scripts/orchestration/sila_stop.sh..."
	bash scripts/orchestration/sila_stop.sh

status:
	@echo "📊 Status do SILA via scripts/orchestration/status_sila.sh..."
	bash scripts/orchestration/status_sila.sh

deploy-quick:
	@echo "⚡ Deploy rápido SILA via scripts/orchestration/quick_deploy.sh..."
	bash scripts/orchestration/quick_deploy.sh

env-prepare:
	@echo "🔧 Preparando ambiente local via scripts/bootstrap/prepare_environment.sh..."
	bash scripts/bootstrap/prepare_environment.sh

db-init:
	@echo "🗄️  Inicializando base de dados local via scripts/bootstrap/init_database.sh..."
	bash scripts/bootstrap/init_database.sh

nginx-monitor:
	@echo "🌐 Monitorando Nginx via scripts/orchestration/nginx_monitor.sh..."
	bash scripts/orchestration/nginx_monitor.sh

monitor-sila:
	@echo "📡 Monitorizando SILA via scripts/orchestration/monitor_sila.sh..."
	bash scripts/orchestration/monitor_sila.sh

monitor-audit:
	@echo "📡 Geração de snapshot de monitorização e árvore de diretórios..."
	bash scripts/orchestration/monitor_sila.sh --export-json --export-md || true
	bash automation/utils/generate_project_tree.sh 4 || true

# =============================
# SILA — Validation Pipeline
# =============================

REQ_VALIDATOR := automation/validation/dependency_validator.py
STRUCTURE_GUARD := automation/validation/structure_guard.sh
DEPENDENCY_AUDIT := scripts/audit_dependencies.sh

# ---- Validation Targets ----

validate: validate-structure validate-deps validate-docker
	@echo "✔ VALIDAÇÃO COMPLETA (SILA SYSTEM OK)"

validate-structure:
	@$(STRUCTURE_GUARD)

validate-deps:
	@$(PYTHON) $(REQ_VALIDATOR)

validate-docker:
	@devops/validate.sh

audit:
	@$(DEPENDENCY_AUDIT)

ci:
	@echo "🔁 Executando CI localmente: validações + audit + pre-commit"
	@make precommit-run || true
	@make validate
	@make audit
	@make validate-local
	@if command -v act >/dev/null 2>&1; then \
		echo "⚙️  Running `act` to simulate GitHub Actions (build-and-test job)."; \
		act -j build-and-test || true; \
	fi

validate-local:
	@echo "🔍 Executando pipeline de validação local..."
	@make check-syntax
	@make validate-docker
	@make validate-structure
	@make validate-deps
	@make precommit-run
	@echo "✅ Pipeline local concluída"

validate-docker:
	@echo "🐳 Validando Docker Compose..."
	@bash devops/validate.sh

validate-structure:
	@echo "🏗️ Validando estrutura do projeto..."
	@bash automation/validation/structure_guard.sh

validate-deps:
	@echo "📦 Validando dependências Python..."
	@mkdir -p reports/ci
	@$(PYTHON) automation/validation/dependency_validator.py --report reports/ci/deps_validation.json

# Conveniência
deps:
	pip install -r requirements.txt

setup-precommit:
	@echo "🔧 Configurando pre-commit hooks..."
	bash scripts/setup_precommit.sh

setup-precommit-all:
	@echo "🔧 Configurando pre-commit e executando em todos os arquivos..."
	bash scripts/setup_precommit.sh --run-all

precommit-update:
	@echo "🔄 Atualizando hooks do pre-commit..."
	pre-commit autoupdate

precommit-run:
	@echo "🏃 Executando todos os hooks do pre-commit..."
	pre-commit run --all-files

precommit-report:
	@echo "📊 Gerando relatório de pre-commit..."
	python3 automation/validation/generate_precommit_report.py

check-yaml:
	@echo "🔍 Verificando sintaxe YAML..."
	python3 scripts/check_yaml_syntax.py

check-python:
	@echo "🐍 Verificando sintaxe Python..."
	python3 scripts/check_python_syntax.py

fix-python:
	@echo "🔧 Corrigindo sintaxe Python automaticamente..."
	python3 scripts/check_python_syntax.py --fix

check-syntax:
	@echo "🔍 Verificando sintaxe de todos os arquivos..."
	@make check-python
	@make check-yaml

fix-syntax:
	@echo "🔧 Corrigindo sintaxe automaticamente..."
	@make fix-python
	@make check-yaml

clean-cache:
	@echo "🧹 Limpando diretórios de cache..."
	python3 scripts/clean_cache_dirs.py

precommit-clean:
	@echo "🔧 Limpando cache e executando pre-commit..."
	@make clean-cache
	@make precommit-run

# -------------------------
# Governança estrutural
# -------------------------

structure-guard:
	@echo "🛡️  Executando Structure Guard..."
	bash automation/validation/structure_guard.sh

refactor-paths-dry:
	@echo "🔁 Simulando refactor de paths (dry-run)..."
	$(PYTHON) tools/refactor/update_paths.py --dry-run

refactor-paths-apply:
	@echo "🔁 Aplicando refactor de paths (com escrita em disco)..."
	$(PYTHON) tools/refactor/update_paths.py --apply
