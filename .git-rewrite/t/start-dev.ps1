#!/usr/bin/env pwsh
<#
.SYNOPSIS
Inicia Frontend (Vite) e Backend (FastAPI) em paralelo
#>

$rootPath = "\\wsl.localhost\Ubuntu\home\truman\dev\sila-system"
$frontendPath = "$rootPath\frontend"
$backendPath = "$rootPath\apps\backend"
$venvPath = "$rootPath\.venv"

Write-Host @"
╔════════════════════════════════════════════════╗
║   🚀 Iniciando SILA - Frontend + Backend       ║
╚════════════════════════════════════════════════╝
"@ -ForegroundColor Cyan

# ====== BACKEND ======
Write-Host "`n📦 Iniciando Backend..." -ForegroundColor Magenta
$backendJob = Start-Job -ScriptBlock {
    param($backendPath, $venvPath)
    
    Set-Location $backendPath
    & "$venvPath\Scripts\Activate.ps1"
    
    # Instalar deps
    pip install -q -r requirements.txt 2>$null
    
    # Iniciar servidor
    uvicorn main:app --reload --host 0.0.0.0 --port 8000
} -ArgumentList $backendPath, $venvPath -Name "backend"

Start-Sleep -Seconds 3
Write-Host "✅ Backend iniciado (Job: $($backendJob.Id))" -ForegroundColor Green

# ====== FRONTEND ======
Write-Host "`n🎨 Iniciando Frontend..." -ForegroundColor Magenta
$frontendJob = Start-Job -ScriptBlock {
    param($frontendPath)
    
    Set-Location $frontendPath
    npm run dev
} -ArgumentList $frontendPath -Name "frontend"

Start-Sleep -Seconds 3
Write-Host "✅ Frontend iniciado (Job: $($frontendJob.Id))" -ForegroundColor Green

# ====== STATUS ======
Write-Host @"
`n╔════════════════════════════════════════════════╗
║  🎯 Serviços em Execução                        ║
╠════════════════════════════════════════════════╣
║  Frontend:  http://localhost:5173              ║
║  Backend:   http://localhost:8000              ║
║  API Docs:  http://localhost:8000/docs         ║
╚════════════════════════════════════════════════╝

ℹ️  Para parar tudo: Pressione Ctrl+C ou execute:
    Stop-Job -Name backend,frontend
    Remove-Job -Name backend,frontend
"@ -ForegroundColor Green

# Aguardar jobs
$backendJob, $frontendJob | Wait-Job
