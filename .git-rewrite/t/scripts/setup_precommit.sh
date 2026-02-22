#!/usr/bin/env bash
set -euo pipefail

# 🔧 SILA Pre-commit Setup
# Instala e configura pre-commit hooks para o projeto SILA

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "${ROOT_DIR}"

GREEN="\033[32m"
CYAN="\033[36m"
RESET="\033[0m"

print() { echo -e "${CYAN}>>>${RESET} $1"; }
ok() { echo -e "   ${GREEN}✓${RESET} $1"; }

print "Configurando pre-commit para SILA System"

# Instalar pre-commit se não estiver instalado
if ! command -v pre-commit &> /dev/null; then
    print "Instalando pre-commit..."
    pip install pre-commit
    ok "Pre-commit instalado"
else
    ok "Pre-commit já instalado"
fi

# Instalar hooks
print "Instalando hooks do pre-commit..."
pre-commit install
ok "Hooks instalados"

# Executar uma primeira vez (opcional)
if [[ "${1:-}" == "--run-all" ]]; then
    print "Executando pre-commit em todos os arquivos..."
    pre-commit run --all-files || {
        echo "⚠️ Alguns hooks falharam - revise os arquivos e commit novamente"
        exit 1
    }
    ok "Pre-commit executado com sucesso"
fi

# Instalar hooks adicionais
print "Instalando hooks para push e post-commit..."
pre-commit install --hook-type pre-push
pre-commit install --hook-type post-commit

print "Pre-commit avançado configurado com sucesso!"
echo ""
echo "🔧 Hooks ativos por stage:"
echo "  pre-commit:"
echo "    ✓ Formatação (Black, isort, Prettier)"
echo "    ✓ Linting (Flake8 + Bugbear)"
echo "    ✓ Validação (YAML, JSON, secrets)"
echo "    ✓ Validação SILA (estrutura, deps, Docker)"
echo ""
echo "  pre-push:"
echo "    ✓ Validação SILA reforçada"
echo ""
echo "  post-commit:"
echo "    ✓ Geração de relatórios consolidados"
echo ""
echo "📊 Relatórios gerados em: reports/pre-commit/"
echo "📋 Configuração: .env.precommit"
echo ""
echo "Uso avançado:"
echo "  git commit                    # Executa hooks pre-commit + post-commit"
echo "  git push                      # Executa hooks pre-push"
echo "  pre-commit run --all-files    # Executa todos os hooks"
echo "  pre-commit run validate-deps  # Executa hook específico"
echo "  pre-commit autoupdate         # Atualiza versões dos hooks"
