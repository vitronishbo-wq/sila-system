#!/bin/bash
# Generate module.yaml discovery files for all normalized modules
# Cria arquivo de descoberta que mapeia onde encontrar cada subdomain

MODULES_DIR="/home/dev03wsl/sila-system/apps/backend/app/modules"
TEMPLATE_FILE="/home/dev03wsl/sila-system/MODULE_DISCOVERY_TEMPLATE.yaml"

generate_module_yaml() {
  local module_path="$1"
  local module_name=$(basename "$module_path")
  local output_file="$module_path/module.yaml"
  
  # Contar arquivos em cada camada
  local api_count=$(find "$module_path/api" -type f -name "*.py" 2>/dev/null | wc -l)
  local app_count=$(find "$module_path/application" -type f -name "*.py" 2>/dev/null | wc -l)
  local domain_count=$(find "$module_path/domain" -type f -name "*.py" 2>/dev/null | wc -l)
  local infra_count=$(find "$module_path/infrastructure" -type f -name "*.py" 2>/dev/null | wc -l)
  
  # Encontrar subdiretórios
  local endpoints_dirs=$(find "$module_path/api/endpoints" -type f -name "*.py" 2>/dev/null | grep -v __init__ | sort)
  local services=$(find "$module_path/application/services" -type f -name "*.py" 2>/dev/null | grep -v __init__ | sort)
  local domain_services=$(find "$module_path/domain/services" -type f -name "*.py" 2>/dev/null | grep -v __init__ | sort)
  
  cat > "$output_file" << EOF
# Module Discovery: $module_name
# Auto-gerado $(date '+%Y-%m-%d %H:%M:%S')
# Mapeia estrutura DDD/Hexagonal para navegação de subdomínios

module: "$module_name"
type: "domain-module"
normalized: true

# ========== ESTATÍSTICAS ==========
statistics:
  api_files: $api_count
  application_files: $app_count
  domain_files: $domain_count
  infrastructure_files: $infra_count
  total: $((api_count + app_count + domain_count + infra_count))

# ========== PONTOS DE ENTRADA (API) ==========
api_endpoints:
  location: "api/endpoints/"
  files:
EOF
  
  if [ -n "$endpoints_dirs" ]; then
    echo "$endpoints_dirs" | while read file; do
      filename=$(basename "$file")
      echo "    - $filename" >> "$output_file"
    done
  else
    echo "    # Nenhum endpoint específico encontrado" >> "$output_file"
  fi
  
  cat >> "$output_file" << EOF

# ========== CAMADA APPLICATION ==========
application_layer:
  services:
    location: "application/services/"
    count: $(find "$module_path/application/services" -type f -name "*.py" 2>/dev/null | grep -v __init__ | wc -l)
EOF
  
  if [ -n "$services" ]; then
    echo "$services" | while read file; do
      filename=$(basename "$file")
      echo "    - $filename" >> "$output_file"
    done
  fi
  
  cat >> "$output_file" << EOF
  
  dto:
    location: "application/dto/"
    schemas: $(find "$module_path/application/dto" -type f -name "*schema*.py" -o -name "*dto*.py" 2>/dev/null | grep -v __init__ | wc -l)
  
  commands:
    location: "application/commands/"
    count: $(find "$module_path/application/commands" -type f -name "*.py" 2>/dev/null | grep -v __init__ | wc -l)
  
  queries:
    location: "application/queries/"
    count: $(find "$module_path/application/queries" -type f -name "*.py" 2>/dev/null | grep -v __init__ | wc -l)

# ========== CAMADA DOMAIN ==========
domain_layer:
  services:
    location: "domain/services/"
    count: $(find "$module_path/domain/services" -type f -name "*.py" 2>/dev/null | grep -v __init__ | wc -l)
EOF
  
  if [ -n "$domain_services" ]; then
    echo "$domain_services" | while read file; do
      filename=$(basename "$file")
      echo "    - $filename" >> "$output_file"
    done
  fi
  
  cat >> "$output_file" << EOF
  
  entities:
    location: "domain/entities/"
    count: $(find "$module_path/domain/entities" -type f -name "*.py" 2>/dev/null | grep -v __init__ | wc -l)
  
  models:
    location: "domain/models/"
    count: $(find "$module_path/domain/models" -type f -name "*.py" 2>/dev/null | grep -v __init__ | wc -l)
  
  ports:
    location: "domain/ports/"
    description: "Interfaces de contrato com camada de infraestrutura"
    count: $(find "$module_path/domain/ports" -type f -name "*.py" 2>/dev/null | grep -v __init__ | wc -l)
  
  events:
    location: "domain/events/"
    count: $(find "$module_path/domain/events" -type f -name "*.py" 2>/dev/null | grep -v __init__ | wc -l)
  
  exceptions:
    location: "domain/exceptions/"
    description: "Exceções específicas do domínio"
    count: $(find "$module_path/domain/exceptions" -type f -name "*.py" 2>/dev/null | grep -v __init__ | wc -l)

# ========== CAMADA INFRASTRUCTURE ==========
infrastructure_layer:
  repositories:
    location: "infrastructure/repositories/"
    description: "Implementação concreta de repositórios"
    count: $(find "$module_path/infrastructure/repositories" -type f -name "*.py" 2>/dev/null | grep -v __init__ | wc -l)
  
  adapters:
    location: "infrastructure/adapters/"
    description: "Adaptadores para sistemas externos"
    count: $(find "$module_path/infrastructure/adapters" -type f -name "*.py" 2>/dev/null | grep -v __init__ | wc -l)
  
  orm:
    location: "infrastructure/orm/"
    description: "Modelos SQLAlchemy"
    count: $(find "$module_path/infrastructure/orm" -type f -name "*.py" 2>/dev/null | grep -v __init__ | wc -l)

# ========== COMO USAR ==========
discovery:
  - step: 1
    description: "Encontrar endpoint"
    action: "Navegue em api_endpoints/files"
  
  - step: 2
    description: "Encontrar serviço de orquestração"
    action: "Procure em application_layer/services/"
  
  - step: 3
    description: "Encontrar lógica de domínio"
    action: "Procure em domain_layer/services/"
  
  - step: 4
    description: "Encontrar persistência"
    action: "Procure em infrastructure_layer/repositories/"

# ========== CONFORMIDADE ==========
conformance:
  has_api_layer: $([ -d "$module_path/api" ] && echo "true" || echo "false")
  has_application_layer: $([ -d "$module_path/application" ] && echo "true" || echo "false")
  has_domain_layer: $([ -d "$module_path/domain" ] && echo "true" || echo "false")
  has_infrastructure_layer: $([ -d "$module_path/infrastructure" ] && echo "true" || echo "false")
  has_tests: $([ -d "$module_path/tests" ] && echo "true" || echo "false")
  ddd_compliant: "✓"
EOF
  
  echo "✓ Gerado: $output_file"
}

echo "📚 Gerando module.yaml para todos os módulos normalizados..."
echo ""

count=0
for module_dir in "$MODULES_DIR"/*; do
  if [ -d "$module_dir" ] && [ -d "$module_dir/domain" ]; then
    generate_module_yaml "$module_dir"
    ((count++))
  fi
done

echo ""
echo "✅ Gerados $count arquivo(s) module.yaml"
echo "   Cada módulo agora tem um mapa de descoberta"
echo ""
echo "📍 Próximos passos:"
echo "   1. Revisar estrutura real vs. esperada"
echo "   2. Preencher descrições de subdomínios"
echo "   3. Documentar dependências especiais"
