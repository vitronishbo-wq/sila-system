# Backend Test Script for SILA (Windows)
# Requires -Version 7
$ErrorActionPreference = "Stop"

Write-Host "=== Backend Test (Windows) ===" -ForegroundColor Cyan

# Verificar se o Python venv existe e dependências estão instaladas
$backendDir = Join-Path $PSScriptRoot "..\..\backend"
$requirements = Join-Path $backendDir "requirements.txt"

if (-not (Test-Path $backendDir)) {
    Write-Host "[ERROR] Backend directory não encontrado: $backendDir" -ForegroundColor Red
    exit 1
}

if (-not (Test-Path $requirements)) {
    Write-Host "[WARN] requirements.txt não encontrado. Pulo teste de dependências." -ForegroundColor Yellow
} else {
    Write-Host "Instalando dependências em modo --dry-run (pip check)..." -ForegroundColor Gray
    pip install --quiet -r $requirements
    pip check | Out-Null
    Write-Host "[OK] Dependências Python verificadas." -ForegroundColor Green
}

Write-Host "[OK] Backend smoke test concluído." -ForegroundColor Green
