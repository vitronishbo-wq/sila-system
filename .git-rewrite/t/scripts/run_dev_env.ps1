# Requires -Version 7
$ErrorActionPreference = "Stop"

$SCRIPT_DIR = Split-Path -Parent $MyInvocation.MyCommand.Path
$UTILS_DIR  = Join-Path $SCRIPT_DIR "utils"

function Write-Info  ($msg) { Write-Host "[INFO] $msg"  -ForegroundColor Cyan }
function Write-Warn  ($msg) { Write-Host "[WARN] $msg"  -ForegroundColor Yellow }
function Write-ErrMsg ($msg) { Write-Host "[ERROR] $msg" -ForegroundColor Red }

$devSetup   = Join-Path $UTILS_DIR "dev_setup.ps1"
$testRunner = Join-Path $UTILS_DIR "test_runner.ps1"

if (-not (Test-Path $UTILS_DIR)) {
    Write-ErrMsg "Diretório de utils não encontrado: $UTILS_DIR"
    exit 1
}

if (-not (Test-Path $devSetup)) {
    Write-ErrMsg "Script de setup não encontrado: $devSetup"
    exit 1
}

if (-not (Test-Path $testRunner)) {
    Write-Warn "Script de testes não encontrado: $testRunner"
}

Write-Info "Iniciando setup de ambiente (Windows)..."
& $devSetup

if (Test-Path $testRunner) {
    Write-Info "Executando testes..."
    & $testRunner
} else {
    Write-Warn "Pulo execução de testes (test_runner.ps1 não disponível)."
}

Write-Info "Fluxo run_dev_env.ps1 concluído com sucesso."
