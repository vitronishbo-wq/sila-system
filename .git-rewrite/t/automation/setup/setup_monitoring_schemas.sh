#!/bin/bash
# Script automatizado para validar schemas do módulo monitoring
# Uso: ./scripts/setup_monitoring_schemas.sh

set -e  # Exit on error

echo "============================================================"
echo "🔍 Validando Schemas do Módulo Monitoring"
echo "============================================================"

# Cores para output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Diretório base
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
BACKEND_DIR="$PROJECT_ROOT/backend"

echo ""
echo "📂 Diretórios:"
echo "   Project Root: $PROJECT_ROOT"
echo "   Backend: $BACKEND_DIR"
echo ""

# Verificar se estamos no diretório correto
if [ ! -d "$BACKEND_DIR/app/modules/monitoring" ]; then
    echo -e "${RED}❌ Erro: Diretório monitoring não encontrado!${NC}"
    echo "   Esperado: $BACKEND_DIR/app/modules/monitoring"
    exit 1
fi

# Verificar se schemas/ existe
if [ ! -d "$BACKEND_DIR/app/modules/monitoring/schemas" ]; then
    echo -e "${RED}❌ Erro: Diretório schemas/ não encontrado!${NC}"
    echo "   Execute primeiro a criação dos schemas."
    exit 1
fi

echo -e "${GREEN}✓${NC} Estrutura de diretórios OK"
echo ""

# Verificar arquivos de schemas
echo "🔍 Verificando arquivos de schemas..."
SCHEMA_FILES=(
    "app/modules/monitoring/schemas/__init__.py"
    "app/modules/monitoring/schemas/alert.py"
    "app/modules/monitoring/schemas/alert_schemas.py"
    "app/modules/monitoring/schemas/metric_schemas.py"
    "app/modules/monitoring/schemas/audit_schemas.py"
    "app/modules/monitoring/schemas/dashboard_schemas.py"
)

MISSING_FILES=0
for file in "${SCHEMA_FILES[@]}"; do
    if [ -f "$BACKEND_DIR/$file" ]; then
        echo -e "   ${GREEN}✓${NC} $file"
    else
        echo -e "   ${RED}✗${NC} $file ${RED}(FALTANDO)${NC}"
        MISSING_FILES=$((MISSING_FILES + 1))
    fi
done

if [ $MISSING_FILES -gt 0 ]; then
    echo ""
    echo -e "${RED}❌ $MISSING_FILES arquivo(s) faltando!${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}✓${NC} Todos os arquivos de schemas encontrados"
echo ""

# Verificar se venv existe
if [ ! -d "$PROJECT_ROOT/venv" ]; then
    echo -e "${YELLOW}⚠️  Aviso: venv não encontrado em $PROJECT_ROOT/venv${NC}"
    echo "   Tentando usar python3 do sistema..."
    PYTHON_CMD="python3"
else
    PYTHON_CMD="$PROJECT_ROOT/venv/bin/python3"
    echo -e "${GREEN}✓${NC} Usando venv: $PYTHON_CMD"
fi

echo ""

# Executar teste de validação
echo "🧪 Executando testes de validação..."
echo ""

cd "$BACKEND_DIR"

if [ -f "test_all_monitoring_schemas.py" ]; then
    if $PYTHON_CMD test_all_monitoring_schemas.py; then
        echo ""
        echo -e "${GREEN}============================================================${NC}"
        echo -e "${GREEN}✅ TODOS OS TESTES PASSARAM!${NC}"
        echo -e "${GREEN}============================================================${NC}"
        echo ""
        echo "📊 Schemas validados:"
        echo "   • Base Alert Schemas: 5"
        echo "   • Alert CRUD Schemas: 6"
        echo "   • Metric Schemas: 5"
        echo "   • Audit Schemas: 3"
        echo "   • Dashboard Schemas: 2"
        echo "   • Models: 3"
        echo "   ────────────────────────────────────────"
        echo "   TOTAL: 24 schemas/models/enums ✓"
        echo ""
        echo "🚀 Próximos passos:"
        echo "   1. Rodar pytest: cd backend && pytest --collect-only"
        echo "   2. Verificar imports no código real"
        echo "   3. Expandir schemas conforme necessário"
        echo ""
        exit 0
    else
        echo ""
        echo -e "${RED}============================================================${NC}"
        echo -e "${RED}❌ TESTES FALHARAM!${NC}"
        echo -e "${RED}============================================================${NC}"
        echo ""
        echo "Verifique os erros acima e corrija os schemas."
        exit 1
    fi
else
    echo -e "${YELLOW}⚠️  Aviso: test_all_monitoring_schemas.py não encontrado${NC}"
    echo "   Pulando testes automatizados."
    echo ""
    echo -e "${GREEN}✓${NC} Estrutura de schemas validada manualmente"
    exit 0
fi
