#!/bin/bash

# ============================================================================
# SILA SYSTEM - INSTALADOR DE EXTENSÕES VS CODE
# ============================================================================
# Script para instalar extensões essenciais do VS Code para desenvolvimento
# do SILA System com stack moderna (Python 3.12+, React 18+, TypeScript 5+)
# ============================================================================

set -euo pipefail

# ============================================================================
# IMPORTAR BIBLIOTECAS COMUNS
# ============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/../lib/colors.sh"
source "$SCRIPT_DIR/../lib/logging.sh"

# ============================================================================
# CONFIGURAÇÕES
# ============================================================================

LOG_FILE="$SCRIPT_DIR/logs/vsc_extensions_$(date +'%Y%m%d_%H%M%S').log"
EXTENSIONS_FILE="$SCRIPT_DIR/.vscode/extensions.json"

# ============================================================================
# EXTENSÕES ESSENCIAIS PARA SILA SYSTEM
# ============================================================================

# Extensões Python (Backend)
PYTHON_EXTENSIONS=(
    "ms-python.python"                    # Python
    "ms-python.pylint"                    # Pylint
    "ms-python.black-formatter"           # Black Formatter
    "ms-python.isort"                     # isort
    "ms-python.flake8"                    # Flake8
    "ms-python.mypy-type-checker"         # MyPy
    "ms-toolsai.jupyter"                  # Jupyter
    "ms-toolsai.vscode-jupyter-cell-tags" # Jupyter Cell Tags
    "ms-toolsai.vscode-jupyter-slideshow" # Jupyter Slideshow
)

# Extensões TypeScript/JavaScript (Frontend)
TYPESCRIPT_EXTENSIONS=(
    "ms-vscode.vscode-typescript-next"    # TypeScript
    "bradlc.vscode-tailwindcss"           # Tailwind CSS
    "esbenp.prettier-vscode"              # Prettier
    "ms-vscode.vscode-eslint"             # ESLint
    "formulahendry.auto-rename-tag"       # Auto Rename Tag
    "christian-kohler.path-intellisense"  # Path Intellisense
    "ms-vscode.vscode-json"               # JSON
)

# Extensões React/Next.js
REACT_EXTENSIONS=(
    "ms-vscode.vscode-react-native"       # React Native Tools
    "ms-vscode.vscode-react-snippets"     # React Snippets
    "formulahendry.auto-close-tag"        # Auto Close Tag
    "ms-vscode.vscode-css-peek"           # CSS Peek
    "zignd.html-css-class-completion"     # HTML CSS Support
)

# Extensões Docker/DevOps
DEVOPS_EXTENSIONS=(
    "ms-azuretools.vscode-docker"         # Docker
    "ms-kubernetes-tools.vscode-kubernetes-tools" # Kubernetes
    "redhat.vscode-yaml"                  # YAML
    "ms-vscode-remote.remote-containers"  # Dev Containers
    "ms-vscode-remote.remote-ssh"         # Remote SSH
)

# Extensões Git/Versionamento
GIT_EXTENSIONS=(
    "eamodio.gitlens"                     # GitLens
    "mhutchie.git-graph"                  # Git Graph
    "donjayamanne.githistory"             # Git History
    "github.vscode-pull-request-github"   # GitHub Pull Requests
)

# Extensões de Produtividade
PRODUCTIVITY_EXTENSIONS=(
    "ms-vscode.vscode-thunder-client"     # Thunder Client (API Testing)
    "ms-vscode.vscode-restclient"         # REST Client
    "humao.rest-client"                   # REST Client (alternativo)
    "ms-vscode.vscode-markdown"           # Markdown
    "yzhang.markdown-all-in-one"          # Markdown All in One
    "ms-vscode.vscode-json"               # JSON
    "redhat.vscode-xml"                   # XML
)

# Extensões de Banco de Dados
DATABASE_EXTENSIONS=(
    "ms-mssql.mssql"                      # SQL Server
    "ms-ossdata.vscode-postgresql"        # PostgreSQL
    "ms-mssql.sql-database-projects-vscode" # SQL Database Projects
)

# Extensões de Monitoramento/Logs
MONITORING_EXTENSIONS=(
    "ms-vscode.vscode-log-viewer"         # Log Viewer
    "ms-vscode.vscode-json"               # JSON Viewer
    "redhat.vscode-yaml"                  # YAML Support
)

# ============================================================================
# FUNÇÕES DE INSTALAÇÃO
# ============================================================================

check_vscode_installed() {
    if ! command -v code &> /dev/null; then
        error "VS Code não está instalado ou não está no PATH"
        log "Instale o VS Code: https://code.visualstudio.com/"
        return 1
    fi

    local version=$(code --version | head -n1)
    success "VS Code encontrado: $version"
    return 0
}

install_extensions() {
    local category="$1"
    local extensions=("${@:2}")

    log "Instalando extensões de $category..."

    for extension in "${extensions[@]}"; do
        log "Instalando: $extension"
        if code --install-extension "$extension" --force 2>&1 | tee -a "$LOG_FILE"; then
            success "✅ $extension instalada"
        else
            warning "⚠️ Falha ao instalar $extension"
        fi
    done
}

create_extensions_json() {
    log "Criando arquivo de extensões recomendadas..."

    mkdir -p "$(dirname "$EXTENSIONS_FILE")"

    cat > "$EXTENSIONS_FILE" << 'EOF'
{
    "recommendations": [
        // Python Backend
        "ms-python.python",
        "ms-python.pylint",
        "ms-python.black-formatter",
        "ms-python.isort",
        "ms-python.flake8",
        "ms-python.mypy-type-checker",
        "ms-toolsai.jupyter",

        // TypeScript/JavaScript Frontend
        "ms-vscode.vscode-typescript-next",
        "bradlc.vscode-tailwindcss",
        "esbenp.prettier-vscode",
        "ms-vscode.vscode-eslint",
        "formulahendry.auto-rename-tag",
        "christian-kohler.path-intellisense",

        // React/Next.js
        "ms-vscode.vscode-react-native",
        "ms-vscode.vscode-react-snippets",
        "formulahendry.auto-close-tag",
        "ms-vscode.vscode-css-peek",

        // Docker/DevOps
        "ms-azuretools.vscode-docker",
        "ms-kubernetes-tools.vscode-kubernetes-tools",
        "redhat.vscode-yaml",
        "ms-vscode-remote.remote-containers",

        // Git/Versionamento
        "eamodio.gitlens",
        "mhutchie.git-graph",
        "donjayamanne.githistory",
        "github.vscode-pull-request-github",

        // Produtividade
        "ms-vscode.vscode-thunder-client",
        "ms-vscode.vscode-restclient",
        "yzhang.markdown-all-in-one",

        // Banco de Dados
        "ms-mssql.mssql",
        "ms-ossdata.vscode-postgresql",

        // Monitoramento
        "ms-vscode.vscode-log-viewer"
    ]
}
EOF

    success "Arquivo de extensões criado: $EXTENSIONS_FILE"
}

create_settings_json() {
    local settings_file="$SCRIPT_DIR/.vscode/settings.json"

    log "Criando configurações do VS Code..."

    cat > "$settings_file" << 'EOF'
{
    // Python
    "python.defaultInterpreterPath": "./backend/venv/bin/python",
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.linting.flake8Enabled": true,
    "python.formatting.provider": "black",
    "python.formatting.blackArgs": ["--line-length=88"],
    "python.sortImports.args": ["--profile", "black"],

    // TypeScript/JavaScript
    "typescript.preferences.importModuleSpecifier": "relative",
    "typescript.suggest.autoImports": true,
    "typescript.updateImportsOnFileMove.enabled": "always",
    "javascript.suggest.autoImports": true,
    "javascript.updateImportsOnFileMove.enabled": "always",

    // ESLint
    "eslint.validate": [
        "javascript",
        "javascriptreact",
        "typescript",
        "typescriptreact"
    ],
    "eslint.format.enable": true,

    // Prettier
    "editor.formatOnSave": true,
    "editor.defaultFormatter": "esbenp.prettier-vscode",
    "prettier.singleQuote": true,
    "prettier.trailingComma": "es5",
    "prettier.tabWidth": 2,

    // Tailwind CSS
    "tailwindCSS.includeLanguages": {
        "typescript": "typescript",
        "typescriptreact": "typescriptreact"
    },
    "tailwindCSS.experimental.classRegex": [
        ["cva\\(([^)]*)\\)", "[\"'`]([^\"'`]*).*?[\"'`]"],
        ["cx\\(([^)]*)\\)", "(?:'|\"|`)([^']*)(?:'|\"|`)"]
    ],

    // Git
    "git.enableSmartCommit": true,
    "git.confirmSync": false,
    "git.autofetch": true,

    // Docker
    "docker.showStartPage": false,

    // Files
    "files.exclude": {
        "**/node_modules": true,
        "**/__pycache__": true,
        "**/.pytest_cache": true,
        "**/venv": true,
        "**/.venv": true,
        "**/dist": true,
        "**/build": true
    },

    // Editor
    "editor.tabSize": 2,
    "editor.insertSpaces": true,
    "editor.rulers": [88, 120],
    "editor.wordWrap": "on",
    "editor.minimap.enabled": false,

    // Terminal
    "terminal.integrated.defaultProfile.linux": "bash",
    "terminal.integrated.cwd": "${workspaceFolder}",

    // SILA System specific
    "files.associations": {
        "*.env*": "dotenv",
        "docker-compose*.yml": "dockercompose",
        "Dockerfile*": "dockerfile"
    }
}
EOF

    success "Configurações do VS Code criadas: $settings_file"
}

# ============================================================================
# FUNÇÃO PRINCIPAL
# ============================================================================

main() {
    echo -e "${CYAN}╔═══════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║        SILA SYSTEM - VS CODE EXTENSIONS          ║${NC}"
    echo -e "${CYAN}║           Instalador Automático                  ║${NC}"
    echo -e "${CYAN}╚═══════════════════════════════════════════════════╝${NC}"
    echo ""

    # Criar diretório de logs
    mkdir -p "$(dirname "$LOG_FILE")"

    # Iniciar log
    echo "=== INSTALAÇÃO DE EXTENSÕES VS CODE - $(date) ===" > "$LOG_FILE"

    # Verificar VS Code
    if ! check_vscode_installed; then
        exit 1
    fi

    # Instalar extensões por categoria
    install_extensions "Python Backend" "${PYTHON_EXTENSIONS[@]}"
    install_extensions "TypeScript/JavaScript" "${TYPESCRIPT_EXTENSIONS[@]}"
    install_extensions "React/Next.js" "${REACT_EXTENSIONS[@]}"
    install_extensions "Docker/DevOps" "${DEVOPS_EXTENSIONS[@]}"
    install_extensions "Git/Versionamento" "${GIT_EXTENSIONS[@]}"
    install_extensions "Produtividade" "${PRODUCTIVITY_EXTENSIONS[@]}"
    install_extensions "Banco de Dados" "${DATABASE_EXTENSIONS[@]}"
    install_extensions "Monitoramento" "${MONITORING_EXTENSIONS[@]}"

    # Criar arquivos de configuração
    create_extensions_json
    create_settings_json

    # Resumo final
    echo ""
    echo -e "${GREEN}${BOLD}✅ INSTALAÇÃO CONCLUÍDA!${NC}"
    echo -e "${CYAN}═══════════════════════════════════════════════════${NC}"
    echo ""
    echo -e "${BLUE}📋 Próximos passos:${NC}"
    echo "   1. Reinicie o VS Code"
    echo "   2. As extensões serão carregadas automaticamente"
    echo "   3. Configure suas preferências pessoais se necessário"
    echo ""
    echo -e "${BLUE}📁 Arquivos criados:${NC}"
    echo "   - $EXTENSIONS_FILE"
    echo "   - $SCRIPT_DIR/.vscode/settings.json"
    echo "   - $LOG_FILE"
    echo ""
    echo -e "${BLUE}🔧 Comandos úteis:${NC}"
    echo "   - code --list-extensions (listar extensões instaladas)"
    echo "   - code --uninstall-extension <id> (desinstalar extensão)"
    echo ""
    echo -e "${GREEN}🎉 VS Code configurado para desenvolvimento SILA!${NC}"
}

# ============================================================================
# EXECUÇÃO
# ============================================================================

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
