$ErrorActionPreference = "Stop"

$SCRIPT_DIR = Split-Path -Parent $MyInvocation.MyCommand.Path
$ROOT_DIR   = Resolve-Path (Join-Path $SCRIPT_DIR "..\..")

$logRoot   = Join-Path $ROOT_DIR "logs\tests"
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$LOG_DIR   = Join-Path $logRoot $timestamp

New-Item -ItemType Directory -Path $LOG_DIR -Force | Out-Null

function Run-Test($script, $name) {
    Write-Host "[INFO] Executando $name..." -ForegroundColor Cyan
    $logFile = Join-Path $LOG_DIR "$name.log"

    if (-not (Test-Path $script)) {
        Write-Host "[WARN] Script de teste não encontrado: $script" -ForegroundColor Yellow
        return
    }

    try {
        & $script *>&1 | Tee-Object -FilePath $logFile
        Write-Host "[INFO] ✅ $name OK (log: $logFile)" -ForegroundColor Green
    } catch {
        Write-Host "[ERROR] ❌ $name falhou. Veja o log: $logFile" -ForegroundColor Red
    }
}

Run-Test (Join-Path $SCRIPT_DIR "smoke-test.ps1")         "smoke-test"
Run-Test (Join-Path $SCRIPT_DIR "test_start_backend.ps1") "backend-test"

Write-Host "✅ Testes concluídos. Logs em: $LOG_DIR" -ForegroundColor Green
