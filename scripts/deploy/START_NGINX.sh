#!/bin/bash

# ============================================================================
# NGINX AUTOMATION - Guia Rápido de Início
# ============================================================================
# Este script inicia o nginx_automation.sh com modo --auto (recomendado)
# ============================================================================

echo ""
echo "╔══════════════════════════════════════════════════════════════════════════════╗"
echo "║                                                                              ║"
echo "║           🚀 SILA NGINX AUTOMATION - GUIA DE INÍCIO RÁPIDO 🚀               ║"
echo "║                                                                              ║"
echo "║                   Configuração Automática em 3 Passos                       ║"
echo "║                                                                              ║"
echo "╚══════════════════════════════════════════════════════════════════════════════╝"
echo ""

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Cores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
BOLD='\033[1m'
NC='\033[0m'

echo -e "${BOLD}📋 VERIFICAÇÃO PRÉ-REQUISITOS${NC}"
echo ""

# Verificar Docker
if command -v docker &> /dev/null; then
    echo -e "${GREEN}✅${NC} Docker instalado"
else
    echo -e "${YELLOW}⚠️${NC}  Docker não encontrado. Instale em: https://www.docker.com/"
    exit 1
fi

# Verificar estrutura
if [[ -d "$SCRIPT_DIR/apps/backend" ]] && [[ -d "$SCRIPT_DIR/apps/frontend" ]]; then
    echo -e "${GREEN}✅${NC} Estrutura de apps detectada"
else
    echo -e "${YELLOW}⚠️${NC}  Estrutura esperada não encontrada"
fi

echo ""
echo -e "${BOLD}${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

echo -e "${BOLD}PASSO 1️⃣  - VERIFICAR SE TUDO ESTÁ OK${NC}"
echo -e "${BLUE}Comando:${NC}"
echo "  bash nginx_automation.sh --diagnose"
echo ""
echo "O que ele faz:"
echo "  • Verifica diretórios de backend e frontend"
echo "  • Valida Docker"
echo "  • Detecta serviços disponíveis"
echo ""

echo -e "${BOLD}PASSO 2️⃣  - CONFIGURAR AUTOMATICAMENTE${NC}"
echo -e "${BLUE}Comando:${NC}"
echo "  bash nginx_automation.sh --auto"
echo ""
echo "O que ele faz:"
echo "  • Detecta serviços da sua aplicação"
echo "  • Gera nginx.conf otimizado automaticamente"
echo "  • Valida a configuração"
echo "  • Inicia container Nginx"
echo "  • Testa funcionamento"
echo ""

echo -e "${BOLD}PASSO 3️⃣  - TESTAR NO NAVEGADOR${NC}"
echo -e "${BLUE}Acesse:${NC}"
echo "  http://localhost/"
echo ""
echo "Você deve ver seu frontend carregando normalmente!"
echo ""

echo -e "${BOLD}${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

echo -e "${BOLD}📚 QUER SABER MAIS?${NC}"
echo ""
echo "Executar agora:"
echo -e "  ${GREEN}bash nginx_automation.sh --auto${NC}"
echo ""
echo "Ver todos os comandos:"
echo -e "  bash nginx_automation.sh --help"
echo ""
echo "Consultar documentação completa:"
echo -e "  cat NGINX_AUTOMATION_GUIDE.md"
echo ""
echo "Ver referência rápida:"
echo -e "  cat NGINX_CHEATSHEET.md"
echo ""

echo -e "${BOLD}🔧 COMANDOS ÚTEIS${NC}"
echo ""
echo "Diagnóstico:              bash nginx_automation.sh --diagnose"
echo "Gerar config:             bash nginx_automation.sh --generate"
echo "Validar config:           bash nginx_automation.sh --validate-config"
echo "Ver serviços:             bash nginx_automation.sh --list-services"
echo "Status completo:          bash nginx_automation.sh --status-report"
echo "Parar nginx:              bash nginx_automation.sh --clean"
echo ""

echo -e "${BOLD}${YELLOW}💡 DICA: Use --auto para começar!${NC}"
echo ""
