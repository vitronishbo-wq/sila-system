#!/bin/bash

# =================================================================
# SILA NGINX DIAGNOSTIC REPORT - Relatório Detalhado de Diagnóstico
# Gera relatório completo sobre o estado do sistema Nginx
# =================================================================

# ============================================================================
# IMPORTAR BIBLIOTECAS COMUNS
# ============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/../lib/colors.sh"
source "$SCRIPT_DIR/../lib/logging.sh"

# ============================================================================
# CONFIGURAÇÃO
# ============================================================================

PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
REPORT_FILE="$PROJECT_ROOT/docs/reports/nginx_diagnostic_$(date +'%Y%m%d_%H%M%S').html"
LOG_FILE="$PROJECT_ROOT/logs/nginx_diagnostic_$(date +'%Y%m%d_%H%M%S').log"

# ============================================================================
# FUNÇÕES DE DIAGNÓSTICO
# ============================================================================

generate_html_report() {
    local status=$1

    cat > "$REPORT_FILE" << EOF
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Relatório de Diagnóstico - SILA Nginx</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
            text-align: center;
        }
        .status-card {
            background: white;
            padding: 20px;
            margin: 20px 0;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .status-healthy { border-left: 5px solid #4CAF50; }
        .status-warning { border-left: 5px solid #FF9800; }
        .status-error { border-left: 5px solid #F44336; }
        .section-title {
            color: #333;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }
        .info-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }
        .info-item {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            border: 1px solid #e9ecef;
        }
        .info-label {
            font-weight: bold;
            color: #495057;
            margin-bottom: 5px;
        }
        .info-value {
            color: #212529;
            font-family: monospace;
        }
        .recommendations {
            background: #e3f2fd;
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
        }
        .footer {
            text-align: center;
            margin-top: 40px;
            color: #6c757d;
            font-size: 0.9em;
        }
        .code {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            font-family: 'Courier New', monospace;
            overflow-x: auto;
            margin: 10px 0;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🛠️ Relatório de Diagnóstico - SILA Nginx</h1>
        <p>Gerado em: $(date)</p>
        <p><strong>Status Geral:</strong>
EOF

    if [[ "$status" == "healthy" ]]; then
        echo '            <span style="color: #4CAF50; font-size: 1.2em;">✅ Sistema Saudável</span>' >> "$REPORT_FILE"
    elif [[ "$status" == "warning" ]]; then
        echo '            <span style="color: #FF9800; font-size: 1.2em;">⚠️  Atenção Necessária</span>' >> "$REPORT_FILE"
    else
        echo '            <span style="color: #F44336; font-size: 1.2em;">❌ Problemas Detectados</span>' >> "$REPORT_FILE"
    fi

    cat >> "$REPORT_FILE" << EOF
        </p>
    </div>

    <div class="status-card status-$status">
        <h2 class="section-title">📊 Resumo Executivo</h2>
        <div class="info-grid">
EOF

    # Container Status
    if docker ps --filter "name=sila-demo-prod" --filter "status=running" | grep -q "sila-demo-prod"; then
        echo '            <div class="info-item">' >> "$REPORT_FILE"
        echo '                <div class="info-label">Status do Container</div>' >> "$REPORT_FILE"
        echo '                <div class="info-value" style="color: #4CAF50;">✅ Rodando</div>' >> "$REPORT_FILE"
        echo '            </div>' >> "$REPORT_FILE"
    else
        echo '            <div class="info-item">' >> "$REPORT_FILE"
        echo '                <div class="info-label">Status do Container</div>' >> "$REPORT_FILE"
        echo '                <div class="info-value" style="color: #F44336;">❌ Parado/Não encontrado</div>' >> "$REPORT_FILE"
        echo '            </div>' >> "$REPORT_FILE"
    fi

    # Image Status
    if docker images | grep -q "sila-nginx:optimized"; then
        echo '            <div class="info-item">' >> "$REPORT_FILE"
        echo '                <div class="info-label">Imagem Nginx</div>' >> "$REPORT_FILE"
        echo '                <div class="info-value" style="color: #4CAF50;">✅ Disponível</div>' >> "$REPORT_FILE"
        echo '            </div>' >> "$REPORT_FILE"
    else
        echo '            <div class="info-item">' >> "$REPORT_FILE"
        echo '                <div class="info-label">Imagem Nginx</div>' >> "$REPORT_FILE"
        echo '                <div class="info-value" style="color: #FF9800;">⚠️  Não encontrada</div>' >> "$REPORT_FILE"
        echo '            </div>' >> "$REPORT_FILE"
    fi

    # Frontend Build
    if [[ -d "frontend/webapp/dist" ]] && [[ -f "frontend/webapp/dist/index.html" ]]; then
        echo '            <div class="info-item">' >> "$REPORT_FILE"
        echo '                <div class="info-label">Arquivos de Frontend</div>' >> "$REPORT_FILE"
        echo '                <div class="info-value" style="color: #4CAF50;">✅ Build encontrado</div>' >> "$REPORT_FILE"
        echo '            </div>' >> "$REPORT_FILE"
    else
        echo '            <div class="info-item">' >> "$REPORT_FILE"
        echo '                <div class="info-label">Arquivos de Frontend</div>' >> "$REPORT_FILE"
        echo '                <div class="info-value" style="color: #F44336;">❌ Build não encontrado</div>' >> "$REPORT_FILE"
        echo '            </div>' >> "$REPORT_FILE"
    fi

    # Nginx Response
    if curl -f -s "http://localhost:8080" > /dev/null 2>&1; then
        RESPONSE=$(curl -s "http://localhost:8080" | head -1)
        if echo "$RESPONSE" | grep -q "Welcome to nginx"; then
            echo '            <div class="info-item">' >> "$REPORT_FILE"
            echo '                <div class="info-label">Resposta do Nginx</div>' >> "$REPORT_FILE"
            echo '                <div class="info-value" style="color: #F44336;">❌ Página padrão</div>' >> "$REPORT_FILE"
            echo '            </div>' >> "$REPORT_FILE"
        else
            echo '            <div class="info-item">' >> "$REPORT_FILE"
            echo '                <div class="info-label">Resposta do Nginx</div>' >> "$REPORT_FILE"
            echo '                <div class="info-value" style="color: #4CAF50;">✅ Aplicação servindo</div>' >> "$REPORT_FILE"
            echo '            </div>' >> "$REPORT_FILE"
        fi
    else
        echo '            <div class="info-item">' >> "$REPORT_FILE"
        echo '                <div class="info-label">Resposta do Nginx</div>' >> "$REPORT_FILE"
        echo '                <div class="info-value" style="color: #F44336;">❌ Não responde</div>' >> "$REPORT_FILE"
        echo '            </div>' >> "$REPORT_FILE"
    fi

    cat >> "$REPORT_FILE" << EOF
        </div>
    </div>

    <div class="status-card status-$status">
        <h2 class="section-title">🔧 Detalhes Técnicos</h2>

        <h3>📁 Estrutura de Arquivos</h3>
        <div class="code">
EOF

    # File structure
    find frontend/dist -name "*.conf" -o -name "*.sh" -o -name "Dockerfile" | head -10 >> "$REPORT_FILE" 2>/dev/null || echo "Arquivos não encontrados" >> "$REPORT_FILE"

    cat >> "$REPORT_FILE" << EOF
        </div>

        <h3>🐳 Containers Ativos</h3>
        <div class="code">
EOF

    docker ps --filter "name=sila" --format "table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}" >> "$REPORT_FILE" 2>/dev/null || echo "Nenhum container encontrado" >> "$REPORT_FILE"

    cat >> "$REPORT_FILE" << EOF
        </div>

        <h3>🏗️ Imagens Disponíveis</h3>
        <div class="code">
EOF

    docker images | grep nginx >> "$REPORT_FILE" 2>/dev/null || echo "Nenhuma imagem nginx encontrada" >> "$REPORT_FILE"

    cat >> "$REPORT_FILE" << EOF
        </div>
    </div>

    <div class="recommendations">
        <h2 class="section-title">💡 Recomendações</h2>
        <ul>
EOF

    # Recommendations based on status
    if [[ "$status" != "healthy" ]]; then
        echo '            <li>Execute o script de automação: <code>./nginx_automation.sh</code></li>' >> "$REPORT_FILE"
        echo '            <li>Verifique se o build do frontend foi executado</li>' >> "$REPORT_FILE"
        echo '            <li>Confirme se a imagem Nginx foi construída corretamente</li>' >> "$REPORT_FILE"
        echo '            <li>Verifique a configuração do docker-compose.dev.yml</li>' >> "$REPORT_FILE"
    else
        echo '            <li>Sistema funcionando corretamente ✅</li>' >> "$REPORT_FILE"
        echo '            <li>Monitore regularmente com: <code>./nginx_monitor.sh</code></li>' >> "$REPORT_FILE"
    fi

    cat >> "$REPORT_FILE" << EOF
        </ul>
    </div>

    <div class="footer">
        <p>Relatório gerado automaticamente pelo Sistema de Automação SILA Nginx</p>
        <p>Para suporte, consulte os logs em: logs/</p>
    </div>
</body>
</html>
EOF

    success "Relatório HTML gerado: $REPORT_FILE"
}

# ============================================================================
# EXECUÇÃO PRINCIPAL
# ============================================================================

main() {
    log "=== GERANDO RELATÓRIO DE DIAGNÓSTICO ==="

    mkdir -p "$(dirname "$REPORT_FILE")"
    mkdir -p "$(dirname "$LOG_FILE")"

    local overall_status="healthy"

    # Verificar componentes críticos
    if ! docker ps --filter "name=sila-demo-prod" --filter "status=running" | grep -q "sila-demo-prod"; then
        overall_status="error"
    fi

    if ! curl -f -s "http://localhost:8080" > /dev/null 2>&1; then
        overall_status="error"
    fi

    RESPONSE=$(curl -s "http://localhost:8080" 2>/dev/null)
    if [[ -n "$RESPONSE" ]] && echo "$RESPONSE" | grep -q "Welcome to nginx"; then
        overall_status="warning"
    fi

    if [[ ! -d "frontend/webapp/dist" ]] || [[ ! -f "frontend/webapp/dist/index.html" ]]; then
        overall_status="warning"
    fi

    # Gerar relatório HTML
    generate_html_report "$overall_status"

    log "=== DIAGNÓSTICO CONCLUÍDO ==="
    info "Relatório disponível em: $REPORT_FILE"

    # Mostrar status no console
    case "$overall_status" in
        "healthy")
            success "Sistema funcionando perfeitamente!"
            ;;
        "warning")
            warn "Sistema com avisos - verifique as recomendações no relatório"
            ;;
        "error")
            error "Problemas críticos detectados - execute a automação imediatamente"
            ;;
    esac
}

main "$@"
