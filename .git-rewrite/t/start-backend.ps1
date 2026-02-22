#!/usr/bin/env pwsh
<#
.SYNOPSIS
Inicia o backend SILA FastAPI
#>

$backendPath = "\\wsl.localhost\Ubuntu\home\truman\dev\sila-system\apps\backend"
$venvPath = "\\wsl.localhost\Ubuntu\home\truman\dev\sila-system\.venv"

Write-Host "🚀 Iniciando Backend SILA..." -ForegroundColor Cyan

# Verificar se venv existe
if (Test-Path $venvPath) {
    Write-Host "✅ Virtual Environment encontrado" -ForegroundColor Green
} else {
    Write-Host "⚠️  Virtual Environment não encontrado em: $venvPath" -ForegroundColor Yellow
    Write-Host "Execute: cd ~/dev/sila-system && python -m venv .venv" -ForegroundColor Yellow
    exit 1
}

# Ir para o diretório do backend
Set-Location $backendPath

# Ativar venv
$activateScript = "$venvPath\Scripts\Activate.ps1"
if (Test-Path $activateScript) {
    & $activateScript
} else {
    Write-Host "❌ Script de ativação não encontrado" -ForegroundColor Red
    exit 1
}

# Verificar requisitos
Write-Host "📦 Verificando dependências..." -ForegroundColor Cyan
pip install fastapi uvicorn sqlalchemy pydantic python-dotenv -q

# Iniciar servidor
Write-Host "🎉 Iniciando servidor FastAPI em http://localhost:8000" -ForegroundColor Green
uvicorn main:app --reload --host 0.0.0.0 --port 8000
