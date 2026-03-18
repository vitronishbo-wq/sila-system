#!/bin/bash
# Module Deficit Evaluation - Full Report with Deep Analysis
# Avalia infrastructure_sector e módulos core com análise de subdomínios

MODULES_DIR="/home/dev03wsl/sila-system/apps/backend/app/modules"

# Função para análise profunda de um módulo
analyze_module_deep() {
  local module_name="$1"
  local module_path="$MODULES_DIR/$module_name"
  
  if [ ! -d "$module_path" ]; then
    return 1
  fi
  
  # 1. Estrutura base (5 camadas DDD)
  local has_api=$([ -d "$module_path/api" ] && echo "yes" || echo "no")
  local has_app=$([ -d "$module_path/application" ] && echo "yes" || echo "no")
  local has_domain=$([ -d "$module_path/domain" ] && echo "yes" || echo "no")
  local has_infra=$([ -d "$module_path/infrastructure" ] && echo "yes" || echo "no")
  local has_tests=$([ -d "$module_path/tests" ] && echo "yes" || echo "no")
  
  # 2. Componentes de camada (lote: especificidade)
  local api_endpoints=$(find "$module_path/api/endpoints" -type f -name "*.py" 2>/dev/null | grep -v __init__ | wc -l)
  local api_schemas=$(find "$module_path/api/schemas" -type f -name "*.py" 2>/dev/null | grep -v __init__ | wc -l)
  
  local app_services=$(find "$module_path/application/services" -type f -name "*.py" 2>/dev/null | grep -v __init__ | wc -l)
  local app_dto=$(find "$module_path/application/dto" -type f -name "*.py" 2>/dev/null | grep -v __init__ | wc -l)
  local app_commands=$(find "$module_path/application/commands" -type f -name "*.py" 2>/dev/null | grep -v __init__ | wc -l)
  local app_queries=$(find "$module_path/application/queries" -type f -name "*.py" 2>/dev/null | grep -v __init__ | wc -l)
  
  local domain_entities=$(find "$module_path/domain/entities" -type f -name "*.py" 2>/dev/null | grep -v __init__ | wc -l)
  local domain_models=$(find "$module_path/domain/models" -type f -name "*.py" 2>/dev/null | grep -v __init__ | wc -l)
  local domain_services=$(find "$module_path/domain/services" -type f -name "*.py" 2>/dev/null | grep -v __init__ | wc -l)
  local domain_ports=$(find "$module_path/domain/ports" -type f -name "*.py" 2>/dev/null | grep -v __init__ | wc -l)
  local domain_events=$(find "$module_path/domain/events" -type f -name "*.py" 2>/dev/null | grep -v __init__ | wc -l)
  
  local infra_repos=$(find "$module_path/infrastructure/repositories" -type f -name "*.py" 2>/dev/null | grep -v __init__ | wc -l)
  local infra_adapters=$(find "$module_path/infrastructure/adapters" -type f -name "*.py" 2>/dev/null | grep -v __init__ | wc -l)
  local infra_orm=$(find "$module_path/infrastructure/orm" -type f -name "*.py" 2>/dev/null | grep -v __init__ | wc -l)
  
  # 3. Verificar subdomínios internos (estrutura de múltiplos bounded contexts)
  local subdomains=$(find "$module_path" -maxdepth 1 -type d \( -name "api" -o -name "application" -o -name "domain" -o -name "infrastructure" -o -name "tests" -o -name ".git" -o -name "__pycache__" \) -prune -o -type d -print | grep -v "^\.$" | wc -l)
  subdomains=$((subdomains - 2)) # Remove . e ..
  
  # Conformidade percentual
  local conformity_score=0
  [ "$has_api" = "yes" ] && conformity_score=$((conformity_score + 20))
  [ "$has_app" = "yes" ] && conformity_score=$((conformity_score + 20))
  [ "$has_domain" = "yes" ] && conformity_score=$((conformity_score + 20))
  [ "$has_infra" = "yes" ] && conformity_score=$((conformity_score + 20))
  [ "$has_tests" = "yes" ] && conformity_score=$((conformity_score + 20))
  
  # Output estruturado
  cat << EOF
╔════════════════════════════════════════════════════════════════════════════════╗
║ MODULE: $module_name
╚════════════════════════════════════════════════════════════════════════════════╝

📋 ESTRUTURA DDD (5 Camadas Obrigatórias)
  ✓ API Layer ............................ $has_api
  ✓ Application Layer ................... $has_app
  ✓ Domain Layer ........................ $has_domain
  ✓ Infrastructure Layer ............... $has_infra
  ✓ Tests Layer ......................... $has_tests
  
  ➜ Conformidade Estrutural: $conformity_score%

📊 ANÁLISE POR CAMADA

  API Layer ($api_endpoints endpoints, $api_schemas schemas):
    • Endpoints: $api_endpoints arquivos em api/endpoints/
    • Schemas: $api_schemas arquivos em api/schemas/

  Application Layer (CQRS):
    • Services: $app_services arquivos
    • DTOs: $app_dto arquivos
    • Commands: $app_commands arquivos
    • Queries: $app_queries arquivos

  Domain Layer (Lógica Pura):
    • Entities: $domain_entities agregados
    • Models: $domain_models objetos de valor
    • Services: $domain_services serviços de domínio
    • Ports: $domain_ports interfaces de contrato
    • Events: $domain_events eventos de domínio

  Infrastructure Layer (Adapters):
    • Repositories: $infra_repos implementações concretas
    • Adapters: $infra_adapters integrações externas
    • ORM Models: $infra_orm modelos SQLAlchemy

📌 CARACTERIZAÇÃO
EOF

  # Verificar padrões especiais
  if [ "$subdomains" -gt 0 ]; then
    echo "  ⚡ MULTI-BOUNDED CONTEXT: $subdomains subdomínios internos detectados"
    echo "     (Este é um módulo agregador com múltiplos contextos limitados)"
  fi
  
  # Verificar padrões de implementação
  if [ "$domain_ports" -gt 0 ]; then
    echo "  ✅ Padrão PORTS & ADAPTERS implementado ($domain_ports portas)"
  else
    echo "  ⚠️  Sem portas de domínio (acoplamento com infrastructure possível)"
  fi
  
  if [ "$app_commands" -gt 0 ] || [ "$app_queries" -gt 0 ]; then
    echo "  ✅ Padrão CQRS implementado (Commands: $app_commands, Queries: $app_queries)"
  else
    echo "  ⚠️  Sem Command/Query handlers (considere implementar CQRS)"
  fi
  
  if [ "$domain_events" -gt 0 ]; then
    echo "  ✅ Domain Events implementado ($domain_events eventos)"
  fi
  
  # Deficits
  echo ""
  echo "🔴 DEFICITS IDENTIFICADOS"
  if [ "$has_tests" = "no" ]; then
    echo "  ❌ CRÍTICO: Nenhuma camada de testes"
  fi
  if [ "$domain_ports" = "0" ] && [ "$has_infra" = "yes" ]; then
    echo "  ⚠️  MODERADO: Sem Ports & Adapters (risco de acoplamento)"
  fi
  if [ "$app_commands" = "0" ] && [ "$app_queries" = "0" ]; then
    echo "  ⚠️  OPPORTUNITY: Sem CQRS (considere implementar para escalabilidade)"
  fi
  if [ "$domain_services" = "0" ] && [ "$domain_entities" -gt 0 ]; then
    echo "  ⚠️  OPPORTUNITY: Sem serviços de domínio (lógica pode estar em application)"
  fi
  
  echo ""
  echo "═════════════════════════════════════════════════════════════════════════════════"
  echo ""
}

# ==============================================================================
# EXECUÇÃO EM LOTE CONFORME REGRA INVIOLÁVEL #2
# ==============================================================================

echo "╔═════════════════════════════════════════════════════════════════════════════════╗"
echo "║     MODULE DEFICIT EVALUATION - DETAILED ANALYSIS                             ║"
echo "║                         $(date '+%Y-%m-%d %H:%M:%S')                                   ║"
echo "╚═════════════════════════════════════════════════════════════════════════════════╝"
echo ""

# LOTE 1: Infrastructure_sector (FOCO PRINCIPAL)
echo "🎯 LOTE 1: INFRASTRUCTURE_SECTOR (FOCO PRINCIPAL - MULTI-BOUNDED CONTEXT)"
analyze_module_deep "infrastructure_sector"

# LOTE 2: Core modules
echo "🎯 LOTE 2: MÓDULOS CORE"
for module in audit compliance governance identity; do
  analyze_module_deep "$module"
done

# LOTE 3: Integration modules
echo "🎯 LOTE 3: MÓDULOS DE INTEGRAÇÃO"
for module in payment procurement economy; do
  analyze_module_deep "$module"
done

echo "✅ Análise completa!"
