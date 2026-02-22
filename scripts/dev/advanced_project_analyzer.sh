#!/bin/bash
# =============================================================================
# SILA Advanced Project Analyzer - Versão 4.0
# =============================================================================
# Moved to tools/analysis for better organization

set -euo pipefail

# Configurações
ANALYSIS_DIR="$PWD/.advanced_analysis"
REPORT_FILE="$ANALYSIS_DIR/project_report_$(date +%Y%m%d_%H%M%S).html"

# Pré-requisitos
check_requirements() {
    echo "🔍 Verificando pré-requisitos..."

    # Verificar se tree está instalado
    if ! command -v tree &> /dev/null; then
        echo "⚠️ Instalando tree para análise de diretórios..."
        sudo apt-get install -y tree
    fi

    # Verificar se pip está instalado
    if ! command -v pip &> /dev/null; then
        echo "⚠️ Instalando pip para análise Python..."
        sudo apt-get install -y python3-pip
    fi
}

# Análise aprofundada da estrutura
analyze_structure() {
    echo "📁 Analisando estrutura (5 níveis)..."
    mkdir -p "$ANALYSIS_DIR"
    tree -L 5 -I "node_modules|venv|.cache|.git" -H "$PWD" -T "SILA Project Structure" -o "$ANALYSIS_DIR/structure.html"
}

# Análise de dependências Python
analyze_python_deps() {
    echo "🐍 Analisando dependências Python..."

    # Encontrar todos os requirements.txt
    find . -name "requirements.txt" -exec echo "📦 {}:" \; -exec cat {} \; > "$ANALYSIS_DIR/python_deps.txt"

    # Verificar conflitos
    pip freeze > "$ANALYSIS_DIR/current_env.txt"
}

# Análise de endpoints API
analyze_api_endpoints() {
    echo "🛣️ Analisando endpoints API..."

    # Buscar padrões de rotas em arquivos Python
    grep -nRE "@router|@app.route|FastAPI" --include="*.py" backend/ > "$ANALYSIS_DIR/api_endpoints.txt" || true
}

# Gerar relatório HTML
generate_report() {
    echo "📊 Gerando relatório HTML..."

    cat > "$REPORT_FILE" <<HTML
<!DOCTYPE html>
<html>
<head>
    <title>SILA Project Analysis - $(date)</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .section { margin-bottom: 30px; border-bottom: 1px solid #eee; padding-bottom: 20px; }
        pre { background: #f5f5f5; padding: 10px; border-radius: 5px; overflow-x: auto; }
        .ok { color: green; }
        .warn { color: orange; }
        .error { color: red; }
    </style>
</head>
<body>
    <h1>SILA Project Analysis</h1>
    <p>Generated: $(date)</p>

    <div class="section">
        <h2>📁 Project Structure</h2>
        <iframe src="structure.html" width="100%" height="500px"></iframe>
    </div>

    <div class="section">
        <h2>🐍 Python Dependencies</h2>
        <pre>$(cat "$ANALYSIS_DIR/python_deps.txt" || echo "No Python dependencies found")</pre>
    </div>

    <div class="section">
        <h2>🛣️ API Endpoints</h2>
        <pre>$(cat "$ANALYSIS_DIR/api_endpoints.txt" || echo "No API endpoints found")</pre>
    </div>
</body>
</html>
HTML
}

# Main
main() {
    check_requirements
    analyze_structure
    analyze_python_deps
    analyze_api_endpoints
    generate_report

    echo "✅ Análise completa! Relatório gerado em:"
    echo "📄 file://$(realpath "$REPORT_FILE")"
}

main "$@"
