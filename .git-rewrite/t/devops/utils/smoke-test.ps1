# Smoke Test Script for SILA (Windows)
# Requires -Version 7
$ErrorActionPreference = "Stop"

Write-Host "=== SILA Smoke Test (Windows) ===" -ForegroundColor Cyan

function Check-Cmd($cmd, $friendly) {
    if (Get-Command $cmd -ErrorAction SilentlyContinue) {
        Write-Host "[OK] $friendly encontrado: $cmd" -ForegroundColor Green
        return $true
    } else {
        Write-Host "[WARN] $friendly não encontrado: $cmd" -ForegroundColor Yellow
        return $false
    }
}

# Verificações básicas
Check-Cmd git        "Git"
Check-Cmd python     "Python"
Check-Cmd node       "Node.js"
Check-Cmd pwsh       "PowerShell 7"

Write-Host "Smoke test concluído." -ForegroundColor Green
