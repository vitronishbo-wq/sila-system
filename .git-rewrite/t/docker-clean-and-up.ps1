# docker-clean-and-up.ps1 — Windows PowerShell

Write-Host "🧹 LIMPEZA AUTOMÁTICA E INICIALIZAÇÃO DO DOCKER" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host ""

# 1. Parar containers
Write-Host "[1/4] Parando containers..." -ForegroundColor Yellow
wsl -e docker ps -a --format "{{.Names}}" | ForEach-Object {
    if ($_ -match "sila-|postgres|redis") {
        wsl -e docker stop $_ 2>$null
        wsl -e docker rm -f $_ 2>$null
    }
}
Write-Host "✅ Containers parados e removidos" -ForegroundColor Green

# 2. Limpar sistema
Write-Host "[2/4] Limpando sistema Docker..." -ForegroundColor Yellow
wsl -e docker system prune -f --volumes 2>$null
Write-Host "✅ Sistema limpo" -ForegroundColor Green

# 3. Iniciar
Write-Host "[3/4] Iniciando containers..." -ForegroundColor Yellow
wsl -e bash -c "cd /home/truman/dev/sila-system && docker compose up -d"
Write-Host "✅ Containers iniciados" -ForegroundColor Green

# 4. Status
Write-Host "[4/4] Verificando status..." -ForegroundColor Yellow
wsl -e bash -c "cd /home/truman/dev/sila-system && docker compose ps"

Write-Host ""
Write-Host "=================================================="  -ForegroundColor Green
Write-Host "✅ DOCKER PRONTO!" -ForegroundColor Green
Write-Host "=================================================="  -ForegroundColor Green
Write-Host ""
Write-Host "🌐 Acesso:" -ForegroundColor Green
Write-Host "  Frontend: http://localhost"
Write-Host "  Backend:  http://localhost:8000"
Write-Host "  Database: localhost:5432"
Write-Host "  Redis:    localhost:6379"
