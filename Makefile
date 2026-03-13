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

# Binários
PYTHON          := python3
BACKEND_PYTHON  := $(BACKEND_DIR)/.venv/bin/python

.PHONY: help setup audit-domains audit-macro generate-graph compile-manifests check-cycles validate-policy audit-full sovereign-ritual architecture-report context-map scaffold-module architecture-sync arch-audit arch-fix daily-audit clean-audit consolidate-audit seed-test-db fix-npm-workspaces clean

help:
	@echo "🚀 SILA System - Gestão de Arquitetura"
	@echo ""
	@echo "Alvos de Auditoria:"
	@echo "  make audit-domains    -> Executa auditoria completa (Scan + Comparação)"
	@echo "  make audit-macro      -> Valida fronteiras de macro-domínios (Física)"
	@echo "  make generate-graph   -> Escaneia o código e gera o grafo observado"
	@echo "  make compile-manifests -> Compila contratos module.yaml em grafo de manifestos"
	@echo "  make check-cycles     -> Bloqueia dependências circulares conforme política YAML"
	@echo "  make validate-policy  -> Valida grafo observado contra arquitetura + política YAML"
	@echo "  make audit-full       -> generate-graph -> compile-manifests -> audit-macro -> check-cycles -> validate-policy"
	@echo "  make sovereign-ritual -> architecture-report -> run_all_guardrails -> check_domain_dependencies"
	@echo ""
	@echo "Alvos de Documentação Viva:"
	@echo "  make context-map       -> Gera docs/architecture/context_map.md via grafo observado"
	@echo "  make scaffold-module   -> Executa scaffold interativo de módulo + auto-registro no grafo"
	@echo "  make architecture-sync -> Universaliza estrutura dos macro-domínios + compila manifests"
	@echo "  make arch-audit       -> Auditoria arquitetural E2E em lote (compliance/ciclos/colisões)"
	@echo "  make arch-fix         -> Normalização universal + auto-fix imports + arch-audit"
	@echo "  make daily-audit      -> 🕐 Ritual Diário: 5 validadores + relatório consolidado"
	@echo "  make clean-audit      -> 🧹 Limpa artefatos do ritual diário"
	@echo "  make consolidate-audit -> Consolidação avançada de artefatos em MD + JSON"
	@echo "  make seed-test-db     -> 🌱 Seed mínimo para testes de integração (RUN_DB_INTEGRATION=1)"
	@echo ""
	@echo "Alvos de Setup:"
	@echo "  make setup            -> Prepara o ambiente e dependências"
	@echo "  make fix-npm-workspaces -> Repara colisões de workspaces e reinstala npm"
	@echo "  make clean            -> Remove caches e relatórios temporários"

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
	@echo "📊 [Guardrail] Cruzando Código Real vs. Grafo de Arquitetura..."
	@$(PYTHON) $(CHECK_DEPS) \
		--observed-json $(REPORTS_DIR)/module_dependency_graph.json \
		--declared-graph $(DOCS_DIR)/AI_ARCHITECTURE_GRAPH.yaml \
		--policy-yaml $(POLICY_YAML) \
		--report-output $(REPORTS_DIR)/domain_dependency_guardrail_report.md \
		--repo-root .
	@$(MAKE) architecture-report

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
	@echo "✅ Auditoria concluída. Relatório em: $(REPORTS_DIR)/"

context-map:
	@echo "🗺️  [Docs] Gerando context map..."
	@$(PYTHON) $(SCRIPTS_DIR)/architecture/generate_context_map.py \
		--graph-json $(REPORTS_DIR)/module_dependency_graph.json \
		--output $(DOCS_DIR)/architecture/context_map.md

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
