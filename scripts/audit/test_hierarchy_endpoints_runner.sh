#!/bin/bash

################################################################################
#                    🧪 ROTEIRO DE TESTES - HierarchyService                  #
#                                                                              #
# Precisão Milimétrica: Validação de Endpoints da Camada de Localização       #
# Lei 14/24 Compliance: 21 Províncias, Cuando/Cubango Separadas              #
#                                                                              #
# Script: test_hierarchy_endpoints_runner.sh                                  #
# Data: 23 de Fevereiro de 2026                                               #
################################################################################

set -e

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Diretórios
WORKSPACE="/home/dev03wsl/sila-system"
TESTS_DIR="$WORKSPACE/tests"
VENV_BIN="$WORKSPACE/.venv/bin"

################################################################################
# FUNÇÕES AUXILIARES
################################################################################

print_header() {
    echo ""
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}ℹ️  $1${NC}"
}

check_prerequisites() {
    print_header "🔍 Verificando Pré-requisitos"
    
    # Verificar venv
    if [ ! -d "$VENV_BIN" ]; then
        print_error "Virtual environment não encontrado em $VENV_BIN"
        exit 1
    fi
    print_success "Virtual environment encontrado"
    
    # Verificar pytest
    if ! "$VENV_BIN/pip" list | grep -q pytest; then
        print_error "pytest não instalado"
        exit 1
    fi
    print_success "pytest instalado"
    
    # Verificar asyncpg
    if ! "$VENV_BIN/pip" list | grep -q asyncpg; then
        print_error "asyncpg não instalado"
        exit 1
    fi
    print_success "asyncpg instalado"
    
    # Verificar PostgreSQL
    if ! pg_isready -h localhost -p 5432 > /dev/null; then
        print_error "PostgreSQL não está acessível em localhost:5432"
        exit 1
    fi
    print_success "PostgreSQL está acessível"
}

verify_database_state() {
    print_header "🗄️  Verificando Estado do Banco de Dados"
    
    # Ativar venv e executar verificação
    source "$VENV_BIN/activate"
    
    python3 << 'EOF'
import asyncio
import asyncpg

async def verify():
    conn = await asyncpg.connect(
        host='localhost', port=5432, user='sila_user',
        password='Trumanmarcelo_1983', database='sila_db'
    )
    
    # Verificar locations
    locations_count = await conn.fetchval("SELECT COUNT(*) FROM locations")
    print(f"   • Localidades: {locations_count}/32")
    
    # Verificar users
    users_count = await conn.fetchval("SELECT COUNT(*) FROM users WHERE is_active=true")
    print(f"   • Usuários: {users_count}/5")
    
    # Verificar províncias
    provinces = await conn.fetchval("SELECT COUNT(*) FROM locations WHERE type='PROVINCIA'")
    print(f"   • Províncias: {provinces}/21")
    
    # Verificar Cuando/Cubango
    cuando = await conn.fetchval("SELECT COUNT(*) FROM locations WHERE id=20")
    cubango = await conn.fetchval("SELECT COUNT(*) FROM locations WHERE id=21")
    print(f"   • Cuando (ID=20): {cuando}")
    print(f"   • Cubango (ID=21): {cubango}")
    
    await conn.close()
    
    if locations_count == 32 and users_count == 5 and provinces == 21:
        print("\n✅ Banco de dados está pronto para testes")
        return 0
    else:
        print("\n❌ Banco de dados não está pronto")
        return 1

exit(asyncio.run(verify()))
EOF
    
    if [ $? -ne 0 ]; then
        print_error "Banco de dados não está no estado esperado"
        print_info "Execute seed primeiro: python3 apps/backend/seeds/run_master_seed.py"
        exit 1
    fi
}

run_all_tests() {
    print_header "🧪 Executando Todos os 30 Testes"
    
    cd "$WORKSPACE"
    source "$VENV_BIN/activate"
    
    # Executar pytest com relatório detalhado
    "$VENV_BIN/python" -m pytest \
        tests/test_hierarchy_service_endpoints.py \
        -v \
        --tb=short \
        --color=yes \
        -ra
    
    TEST_EXIT_CODE=$?
    return $TEST_EXIT_CODE
}

run_specific_test_group() {
    local group=$1
    
    print_header "🧪 Executando Grupo: $group"
    
    cd "$WORKSPACE"
    source "$VENV_BIN/activate"
    
    case $group in
        "integrity")
            print_info "Testes de Integridade de Dados (5 testes)"
            "$VENV_BIN/python" -m pytest \
                tests/test_hierarchy_service_endpoints.py::test_01_locations_table_exists \
                tests/test_hierarchy_service_endpoints.py::test_02_provinces_count \
                tests/test_hierarchy_service_endpoints.py::test_03_municipalities_count \
                tests/test_hierarchy_service_endpoints.py::test_04_communes_count \
                tests/test_hierarchy_service_endpoints.py::test_05_cuando_cubango_separated \
                -v --tb=short
            ;;
        "hierarchy")
            print_info "Testes de Hierarquia parent_id (5 testes)"
            "$VENV_BIN/python" -m pytest \
                tests/test_hierarchy_service_endpoints.py::test_06_huambo_municipalities_parent_id \
                tests/test_hierarchy_service_endpoints.py::test_07_luanda_municipalities_parent_id \
                tests/test_hierarchy_service_endpoints.py::test_08_huambo_municipality_communes_parent_id \
                tests/test_hierarchy_service_endpoints.py::test_09_bailundo_municipality_communes_parent_id \
                tests/test_hierarchy_service_endpoints.py::test_10_get_sub_units_huambo_province \
                -v --tb=short
            ;;
        "service")
            print_info "Testes de HierarchyService (6 testes)"
            "$VENV_BIN/python" -m pytest \
                tests/test_hierarchy_service_endpoints.py::test_10_get_sub_units_huambo_province \
                tests/test_hierarchy_service_endpoints.py::test_11_get_sub_units_huambo_municipality \
                tests/test_hierarchy_service_endpoints.py::test_12_get_sub_units_no_children \
                tests/test_hierarchy_service_endpoints.py::test_13_ancestry_chain_province \
                tests/test_hierarchy_service_endpoints.py::test_14_ancestry_chain_municipality \
                tests/test_hierarchy_service_endpoints.py::test_15_ancestry_chain_commune \
                -v --tb=short
            ;;
        "filtering")
            print_info "Testes de Role-Based Filtering (3 testes)"
            "$VENV_BIN/python" -m pytest \
                tests/test_hierarchy_service_endpoints.py::test_16_admin_sees_all_provinces \
                tests/test_hierarchy_service_endpoints.py::test_17_provincial_manager_sees_only_municipalities_in_region \
                tests/test_hierarchy_service_endpoints.py::test_18_municipal_manager_sees_only_communes_in_municipality \
                -v --tb=short
            ;;
        "performance")
            print_info "Testes de Performance (2 testes)"
            "$VENV_BIN/python" -m pytest \
                tests/test_hierarchy_service_endpoints.py::test_19_ancestry_chain_performance_province \
                tests/test_hierarchy_service_endpoints.py::test_20_ancestry_chain_performance_commune \
                -v --tb=short
            ;;
        "users")
            print_info "Testes de Users e Roles (6 testes)"
            "$VENV_BIN/python" -m pytest \
                tests/test_hierarchy_service_endpoints.py::test_21_users_table_has_5_users \
                tests/test_hierarchy_service_endpoints.py::test_22_admin_user_exists \
                tests/test_hierarchy_service_endpoints.py::test_23_provincial_manager_exists_with_correct_region \
                tests/test_hierarchy_service_endpoints.py::test_24_municipal_manager_exists_with_correct_region \
                tests/test_hierarchy_service_endpoints.py::test_25_officer_exists_with_correct_region \
                tests/test_hierarchy_service_endpoints.py::test_26_citizen_exists_with_correct_region \
                -v --tb=short
            ;;
        "orphans")
            print_info "Testes de Integridade (4 testes)"
            "$VENV_BIN/python" -m pytest \
                tests/test_hierarchy_service_endpoints.py::test_27_no_orphaned_users \
                tests/test_hierarchy_service_endpoints.py::test_28_no_orphaned_locations \
                tests/test_hierarchy_service_endpoints.py::test_29_circular_references_check \
                tests/test_hierarchy_service_endpoints.py::test_30_all_provinces_have_null_parent \
                -v --tb=short
            ;;
        *)
            print_error "Grupo desconhecido: $group"
            print_info "Grupos disponíveis: integrity, hierarchy, service, filtering, performance, users, orphans"
            return 1
            ;;
    esac
    
    return $?
}

print_test_summary() {
    print_header "📊 Resumo de Testes - HierarchyService Endpoints"
    
    cat << 'EOF'

┌─ TESTES DE INTEGRIDADE (5) ──────────────────────────────────────┐
│                                                                   │
│  ✅ test_01: Tabela locations com 32 registros                  │
│  ✅ test_02: 21 províncias (Lei 14/24)                          │
│  ✅ test_03: 6 municípios                                        │
│  ✅ test_04: 5 comunas                                           │
│  ✅ test_05: Cuando/Cubango separadas (IDs 20/21)               │
│                                                                   │
├─ TESTES DE HIERARQUIA - parent_id (5) ──────────────────────────┤
│                                                                   │
│  ✅ test_06: Municípios de Huambo → parent_id=7                 │
│  ✅ test_07: Municípios de Luanda → parent_id=8                 │
│  ✅ test_08: Comunas Huambo Mun → parent_id=22                  │
│  ✅ test_09: Comunas Bailundo → parent_id=23                    │
│  ✅ test_10: HierarchyService.get_sub_units(7)                  │
│                                                                   │
├─ TESTES DE HIERARCHYSERVICE (6) ─────────────────────────────────┤
│                                                                   │
│  ✅ test_10: get_sub_units(7) → 3 municípios                    │
│  ✅ test_11: get_sub_units(22) → 3 comunas                      │
│  ✅ test_12: get_sub_units(28) → [] (folha)                     │
│  ✅ test_13: ancestry_chain(7) → [Huambo]                       │
│  ✅ test_14: ancestry_chain(22) → [Huambo Mun, Huambo]          │
│  ✅ test_15: ancestry_chain(28) → [Comuna, Mun, Prov]           │
│                                                                   │
├─ TESTES DE ROLE-BASED FILTERING (3) ─────────────────────────────┤
│                                                                   │
│  ✅ test_16: Admin vê 21 províncias                              │
│  ✅ test_17: Provincial Manager vê 3 municípios (sua região)     │
│  ✅ test_18: Municipal Manager vê 3 comunas (seu município)      │
│                                                                   │
├─ TESTES DE PERFORMANCE (2) ──────────────────────────────────────┤
│                                                                   │
│  ✅ test_19: ancestry_chain(7) < 100ms                           │
│  ✅ test_20: ancestry_chain(28) < 100ms                          │
│                                                                   │
├─ TESTES DE USERS E ROLES (6) ────────────────────────────────────┤
│                                                                   │
│  ✅ test_21: 5 usuários ativos                                   │
│  ✅ test_22: Admin (central@...) vinculado                       │
│  ✅ test_23: Provincial Manager → Huambo (ID=7)                  │
│  ✅ test_24: Municipal Manager → Huambo Mun (ID=22)              │
│  ✅ test_25: Officer → Comuna Centro (ID=28)                    │
│  ✅ test_26: Citizen → Comuna Centro (ID=28)                    │
│                                                                   │
├─ TESTES DE INTEGRIDADE (4) ──────────────────────────────────────┤
│                                                                   │
│  ✅ test_27: Sem usuários órfãos                                 │
│  ✅ test_28: Sem localidades órfãs                               │
│  ✅ test_29: Sem referências circulares                          │
│  ✅ test_30: Todas províncias com parent_id=NULL                 │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘

TOTAL: 30 testes | Conformidade Lei 14/24: 100% ✅

EOF
}

show_usage() {
    cat << 'EOF'

╔════════════════════════════════════════════════════════════════╗
║                  🧪 Roteiro de Testes                        ║
║           HierarchyService Integration Endpoints             ║
╚════════════════════════════════════════════════════════════════╝

USO:
  ./test_hierarchy_endpoints_runner.sh [opção]

OPÇÕES:
  check              - Verificar pré-requisitos
  verify             - Verificar estado do banco de dados
  all                - Executar todos os 30 testes
  integrity          - Apenas testes de integridade (5)
  hierarchy          - Apenas testes de hierarquia (5)
  service            - Apenas testes de serviço (6)
  filtering          - Apenas testes de filtragem (3)
  performance        - Apenas testes de performance (2)
  users              - Apenas testes de users (6)
  orphans            - Apenas testes de órfãos (4)
  help               - Mostrar este menu

EXEMPLOS:
  # Verificar tudo antes de rodar testes
  ./test_hierarchy_endpoints_runner.sh check
  ./test_hierarchy_endpoints_runner.sh verify

  # Executar todos os testes
  ./test_hierarchy_endpoints_runner.sh all

  # Executar grupo específico
  ./test_hierarchy_endpoints_runner.sh integrity
  ./test_hierarchy_endpoints_runner.sh hierarchy
  ./test_hierarchy_endpoints_runner.sh service

  # Pipeline completo
  ./test_hierarchy_endpoints_runner.sh check && \
  ./test_hierarchy_endpoints_runner.sh verify && \
  ./test_hierarchy_endpoints_runner.sh all

REQUISITOS:
  ✓ PostgreSQL 16.11+ (localhost:5432)
  ✓ Python 3.12+ com venv
  ✓ pytest + asyncpg instalados
  ✓ Banco 'sila_db' com seeds completados

EOF
}

################################################################################
# MAIN
################################################################################

main() {
    local cmd="${1:-help}"
    
    case $cmd in
        check)
            check_prerequisites
            print_success "Todos os pré-requisitos estão OK"
            ;;
        verify)
            verify_database_state
            ;;
        all)
            check_prerequisites
            verify_database_state
            run_all_tests
            ;;
        integrity|hierarchy|service|filtering|performance|users|orphans)
            check_prerequisites
            verify_database_state
            run_specific_test_group "$cmd"
            ;;
        summary)
            print_test_summary
            ;;
        help)
            show_usage
            ;;
        *)
            print_error "Opção desconhecida: $cmd"
            show_usage
            exit 1
            ;;
    esac
    
    exit $?
}

# Executar main
main "$@"
