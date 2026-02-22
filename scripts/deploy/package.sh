#!/bin/bash
################################################################################
# 📦 SILA System - Package Builder
# Empacota migração completa com instruções simples
# Resultado: Um arquivo .tar.gz com tudo pronto
#
# Uso:
#   ./package.sh                  # Empacotar tudo
#   ./package.sh --extract        # Extrair em outro projeto
#   ./package.sh --instructions   # Apenas gerar instruções
################################################################################

set -euo pipefail

# ============================================================================
# CONFIGURAÇÃO
# ============================================================================

PACKAGE_NAME="sila-migration-package-$(date +%Y%m%d_%H%M%S)"
PACKAGE_FILE="${PACKAGE_NAME}.tar.gz"
EXTRACT_DIR="sila-migration-extracted-$(date +%Y%m%d_%H%M%S)"

# ============================================================================
# CORES
# ============================================================================

GREEN='\033[0;32m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
RESET='\033[0m'

# ============================================================================
# HELPERS
# ============================================================================

print_header() {
    echo -e "\n${BOLD}${CYAN}════════════════════════════════════════════${RESET}"
    echo -e "${BOLD}${CYAN}$1${RESET}"
    echo -e "${BOLD}${CYAN}════════════════════════════════════════════${RESET}\n"
}

print_success() {
    echo -e "${GREEN}✓${RESET} $1"
}

print_info() {
    echo -e "${BLUE}ℹ${RESET} $1"
}

# ============================================================================
# GERAR ARQUIVO DE INSTRUÇÕES
# ============================================================================

create_instructions() {
    local output_file="$1"

    cat > "$output_file" << 'INSTRUCTIONS'
# 🚀 SILA Migration Package - Quick Start

## Conteúdo do Pacote

```
├── scripts/
│   ├── onboarding.sh              # Orquestra tudo (EXECUTE ISTO!)
│   ├── migration_analyzer.py      # Análise
│   ├── module_classifier.py       # Classificação
│   ├── update_imports.py          # Mudança
│   ├── validate_migration.py      # Validação
│   ├── monitor-migration.sh       # Monitoramento
│   └── structure-guard.sh         # Proteção
├── docs/
│   ├── GUIA_PARA_LEIGOS.md        # Leia isto primeiro! 👈
│   ├── README_MIGRATION.md         # Visão geral
│   ├── ETAPA_5_SUMMARY.md         # Resumo
│   ├── NAVIGATION_INDEX.md        # Índice
│   └── MIGRATION_EXECUTIVE_PLAN.md# Plano
├── setup.sh                       # Setup automático
└── LEIA-ME-PRIMEIRO.txt           # Este arquivo

Total: 12 arquivos, tudo pronto para uso!
```

## ⚡ Instalação Rápida (2 minutos)

### Passo 1: Extrair pacote
```bash
tar xzf sila-migration-package-*.tar.gz
cd sila-migration-extracted-*
```

### Passo 2: Fazer setup
```bash
bash setup.sh
```

### Passo 3: Começar migração
```bash
# Opção 1: Menu interativo (recomendado)
bash scripts/onboarding.sh --interactive

# Opção 2: Fase específica
bash scripts/onboarding.sh --phase 1 --dry-run
bash scripts/onboarding.sh --phase 1
```

## 📖 Leitura Recomendada

1. **GUIA_PARA_LEIGOS.md** (15 min)
   - Tudo em português simples
   - Sem jargão técnico

2. **README_MIGRATION.md** (10 min)
   - Visão geral executiva

3. **ETAPA_5_SUMMARY.md** (10 min)
   - Resumo visual

## 🎯 Roteiro Sugerido

```
SEG: Análise
  bash scripts/onboarding.sh --phase analyze_only

TER: Fase 1 (monitoring) - DRY-RUN
  bash scripts/onboarding.sh --phase 1 --dry-run
  # Ler relatório

QUA: Fase 1 (monitoring) - REAL
  bash scripts/onboarding.sh --phase 1
  # Validar, fazer PR

QUI: Fase 2 (common)
  bash scripts/onboarding.sh --phase 2

SEX: Fase 3 (auth)
  bash scripts/onboarding.sh --phase 3

SEG-TER: Testes + Documentação
  bash scripts/monitor-migration.sh --report
  bash scripts/structure-guard.sh --report
```

## 🆘 Ajuda

| Situação | Comando |
|----------|---------|
| Primeira vez | `cat GUIA_PARA_LEIGOS.md` |
| Entender contexto | `cat README_MIGRATION.md` |
| Ver índice | `cat NAVIGATION_INDEX.md` |
| Menu | `bash scripts/onboarding.sh --interactive` |
| Validar | `bash scripts/monitor-migration.sh --check` |
| Estrutura | `bash scripts/structure-guard.sh --check` |

## ⏱️ Tempos

```
Análise:        2 minutos
Classificação:  1 minuto
Fase 1:        45 minutos
Fase 2:        30 minutos
Fase 3:        90 minutos
Testes:        15 minutos
TOTAL:         ~3 horas
```

## 🔒 Segurança

✅ Backup automático antes de modificar
✅ DRY-RUN antes de mudanças reais
✅ Validação após cada etapa
✅ Rollback < 5 minutos se necessário
✅ Relatórios completos gerados

## 📞 Contato

Se tiver dúvidas:
1. Leia GUIA_PARA_LEIGOS.md
2. Consulte README_MIGRATION.md
3. Execute com --help: `bash scripts/onboarding.sh --help`
4. Pergunte ao Tech Lead

---

**Bem-vindo! Você está 2 cliques de uma migração segura e completa.** 🚀

INSTRUCTIONS
}

# ============================================================================
# CRIAR SETUP SCRIPT
# ============================================================================

create_setup() {
    local output_file="$1"

    cat > "$output_file" << 'SETUP'
#!/bin/bash
# Setup automático para migration package

set -euo pipefail

echo "🚀 Configurando pacote de migração..."

# Copiar scripts para raiz do projeto
if [ -d "scripts" ]; then
    cp scripts/*.py ./ 2>/dev/null || true
    cp scripts/*.sh ./ 2>/dev/null || true
    chmod +x *.sh *.py 2>/dev/null || true
    echo "✓ Scripts copiados"
fi

# Copiar docs
if [ -d "docs" ]; then
    cp docs/*.md ./ 2>/dev/null || true
    echo "✓ Documentação copiada"
fi

echo ""
echo "✅ Setup concluído!"
echo ""
echo "Próximo passo:"
echo "  bash onboarding.sh --interactive"
SETUP

    chmod +x "$output_file"
}

# ============================================================================
# EMPACOTAR
# ============================================================================

package() {
    print_header "📦 Criando Pacote de Migração"

    # Criar diretório temporário
    local temp_dir=$(mktemp -d)
    trap "rm -rf $temp_dir" EXIT

    mkdir -p "$temp_dir/scripts"
    mkdir -p "$temp_dir/docs"

    print_info "Copiando scripts..."
    cp onboarding.sh "$temp_dir/scripts/" 2>/dev/null || true
    cp migration_analyzer.py "$temp_dir/scripts/" 2>/dev/null || true
    cp module_classifier.py "$temp_dir/scripts/" 2>/dev/null || true
    cp update_imports.py "$temp_dir/scripts/" 2>/dev/null || true
    cp validate_migration.py "$temp_dir/scripts/" 2>/dev/null || true
    cp monitor-migration.sh "$temp_dir/scripts/" 2>/dev/null || true
    cp structure-guard.sh "$temp_dir/scripts/" 2>/dev/null || true

    print_info "Copiando documentação..."
    cp GUIA_PARA_LEIGOS.md "$temp_dir/docs/" 2>/dev/null || true
    cp README_MIGRATION.md "$temp_dir/docs/" 2>/dev/null || true
    cp ETAPA_5_SUMMARY.md "$temp_dir/docs/" 2>/dev/null || true
    cp NAVIGATION_INDEX.md "$temp_dir/docs/" 2>/dev/null || true
    cp MIGRATION_EXECUTIVE_PLAN.md "$temp_dir/docs/" 2>/dev/null || true
    cp MIGRATION_EXECUTION_GUIDE.md "$temp_dir/docs/" 2>/dev/null || true

    print_info "Gerando instruções..."
    create_instructions "$temp_dir/LEIA-ME-PRIMEIRO.txt"

    print_info "Gerando setup script..."
    create_setup "$temp_dir/setup.sh"

    print_info "Compactando pacote..."
    tar czf "$PACKAGE_FILE" -C "$(dirname $temp_dir)" "$(basename $temp_dir)"

    print_success "Pacote criado: $PACKAGE_FILE"

    # Informações
    echo ""
    print_info "Tamanho: $(du -h $PACKAGE_FILE | cut -f1)"
    print_info "Arquivos: $(tar tzf $PACKAGE_FILE | wc -l) items"

    echo ""
    echo "Próximos passos:"
    echo "  1. Transportar arquivo: $PACKAGE_FILE"
    echo "  2. Extrair: tar xzf $PACKAGE_FILE"
    echo "  3. Ler: cat LEIA-ME-PRIMEIRO.txt"
    echo "  4. Setup: bash setup.sh"
    echo "  5. Começar: bash onboarding.sh --interactive"
}

# ============================================================================
# EXTRAIR
# ============================================================================

extract() {
    print_header "📦 Extraindo Pacote"

    if [ $# -lt 1 ]; then
        echo "Arquivo não especificado!"
        echo "Uso: $0 --extract <arquivo.tar.gz>"
        exit 1
    fi

    local package_file="$1"

    if [ ! -f "$package_file" ]; then
        echo "Arquivo não encontrado: $package_file"
        exit 1
    fi

    print_info "Extraindo $package_file..."
    tar xzf "$package_file"

    local extracted=$(ls -d sila-migration-extracted-* 2>/dev/null | head -1)

    print_success "Pacote extraído em: $extracted"

    echo ""
    echo "Próximos passos:"
    echo "  cd $extracted"
    echo "  cat LEIA-ME-PRIMEIRO.txt"
    echo "  bash setup.sh"
}

# ============================================================================
# MAIN
# ============================================================================

main() {
    case "${1:-package}" in
        package)
            package
            ;;
        extract)
            extract "${2:-}"
            ;;
        instructions)
            create_instructions "/tmp/instructions.txt"
            cat "/tmp/instructions.txt"
            ;;
        --help)
            echo "Uso: $0 [comando]"
            echo "  package        Empacotar migração (padrão)"
            echo "  extract FILE   Extrair pacote"
            echo "  instructions   Mostrar instruções"
            ;;
        *)
            package
            ;;
    esac
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
