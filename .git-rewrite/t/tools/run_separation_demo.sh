#!/bin/bash
# 🎬 Demo do Sistema de Separação Models/Schemas
# Execute: bash tools/run_separation_demo.sh

echo "🎬 SILA Separation System - Demo Interativo"
echo "=========================================="
echo ""

# Cores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Função para pausar
pause() {
    echo ""
    read -p "Pressione ENTER para continuar..."
    echo ""
}

# 1. Testar sistema
echo -e "${BLUE}📍 ETAPA 1: Testando o sistema${NC}"
echo "Executando: python3 tools/test_separation_system.py"
pause
python3 tools/test_separation_system.py
pause

# 2. Validar módulo location
echo -e "${BLUE}📍 ETAPA 2: Validando módulo location${NC}"
echo "Executando: python3 tools/validate_separation.py backend/modules/location"
pause
python3 tools/validate_separation.py backend/modules/location
pause

# 3. Auditar imports
echo -e "${BLUE}📍 ETAPA 3: Auditando imports${NC}"
echo "Executando: python3 tools/audit_imports.py --module location"
pause
python3 tools/audit_imports.py --module location
pause

# 4. Validar todos os módulos
echo -e "${BLUE}📍 ETAPA 4: Validando todos os módulos${NC}"
echo "Executando: python3 tools/validate_separation.py --all"
pause
python3 tools/validate_separation.py --all
pause

# 5. Simular migração em lote
echo -e "${BLUE}📍 ETAPA 5: Simulando migração em lote${NC}"
echo "Executando: python3 tools/migrate_all_modules.py --dry-run"
pause
python3 tools/migrate_all_modules.py --dry-run
pause

# Resumo
echo ""
echo "=========================================="
echo -e "${GREEN}✨ Demo concluído!${NC}"
echo "=========================================="
echo ""
echo "📚 Documentação disponível em:"
echo "   • tools/README_SEPARATION.md"
echo "   • tools/QUICKSTART_SEPARATION.md"
echo "   • tools/EXAMPLES_SEPARATION.md"
echo ""
echo "🚀 Para migrar um módulo:"
echo "   python3 tools/migrate_module.py backend/modules/<module_name>"
echo ""
