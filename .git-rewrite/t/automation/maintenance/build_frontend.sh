#!/bin/bash
# Script para gerenciar a fase de build do frontend.
# Uso: ./scripts/build_frontend.sh [dev|prod]

set -euo pipefail

FRONTEND_DIR="frontend"
ENV="${1:-dev}"

# --- Funções de Logging ---

log() {
    local level=$1
    local message=$2
    printf "[%s] [%s] %s\n" "$(date +'%Y-%m-%d %H:%M:%S')" "$level" "$message"
}

if [[ ! -d "$FRONTEND_DIR" ]]; then
    log ERROR "Diretório do frontend '$FRONTEND_DIR' não encontrado. Abortando build."
    exit 1
fi

log INFO "Iniciando preparação do frontend para ambiente: $ENV"

# 1. Entrar na pasta do frontend
cd "$FRONTEND_DIR"

# 2. Instalar dependências (se necessário ou forçado)
log INFO "Garantindo dependências Node/NPM..."
if [[ ! -d "node_modules" ]]; then
    log INFO "node_modules não encontrado. Executando npm install..."
    npm install
else
    # Opção avançada: Descomente abaixo para forçar a instalação em DEV
    # log INFO "Rodando npm install para garantir a consistência."
    # npm install
    log INFO "node_modules já existe. Pulando 'npm install'."
fi

# 3. Executar o comando de build
if [[ "$ENV" = "dev" ]] || [[ "$ENV" = "development" ]]; then
    # No modo DEV, normalmente, apenas garantimos a instalação.
    # O container Docker Compose rodará o servidor de desenvolvimento (e.g., 'npm run dev').
    log INFO "Modo DEV. Apenas garantindo dependências. O servidor será iniciado no container."
elif [[ "$ENV" = "prod" ]] || [[ "$ENV" = "production" ]]; then
    log INFO "Modo PROD. Executando build de produção..."
    # 'npm run build' criará os arquivos estáticos na pasta 'dist'
    npm run build
    log SUCCESS "Build de produção concluído. Artefatos na pasta 'dist'."
else
    log ERROR "Ambiente '$ENV' desconhecido. Use 'dev' ou 'prod'."
    cd ..
    exit 1
fi

# 4. Voltar para a pasta raiz
cd ..
log SUCCESS "Preparação do frontend concluída."
