# ==================================================
# Script PowerShell para gerar requirements.lock
# ==================================================

$ErrorActionPreference = "Stop"

Write-Host "🔒 Gerando requirements.lock..." -ForegroundColor Cyan

# Diretório do projeto
$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot

# Criar um ambiente virtual temporário
Write-Host "📦 Criando ambiente virtual temporário..." -ForegroundColor Yellow
python -m venv .venv_lock_temp

# Ativar o ambiente virtual
Write-Host "⚡ Ativando ambiente virtual..." -ForegroundColor Yellow
& .\.venv_lock_temp\Scripts\Activate.ps1

# Atualizar pip
Write-Host "⬆️  Atualizando pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip setuptools wheel

# Instalar dependências do requirements.txt
Write-Host "📥 Instalando dependências..." -ForegroundColor Yellow
pip install -r requirements.txt

# Gerar requirements.lock
Write-Host "💾 Gerando requirements.lock..." -ForegroundColor Yellow
pip freeze > requirements.lock

# Desativar o ambiente virtual
deactivate

# Remover o ambiente virtual temporário
Write-Host "🧹 Limpando ambiente temporário..." -ForegroundColor Yellow
Remove-Item -Recurse -Force .venv_lock_temp

Write-Host "✅ requirements.lock gerado com sucesso!" -ForegroundColor Green
Write-Host "📍 Localização: $ProjectRoot\requirements.lock" -ForegroundColor Green

# Mostrar resumo
Write-Host ""
Write-Host "📊 Resumo:" -ForegroundColor Cyan
$lineCount = (Get-Content requirements.lock).Count
Write-Host "   $lineCount pacotes instalados" -ForegroundColor White
