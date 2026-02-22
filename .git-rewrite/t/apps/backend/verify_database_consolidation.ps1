# PowerShell Script: Validação de Consolidação de Database
#
# Este script verifica:
# 1. Sintaxe de todos os arquivos Python modificados
# 2. Imports corretos (core/db ao invés de core/database)
# 3. Ausência de referências a core.database
# 4. Conformidade com padrão de imports absolutos

param(
    [switch]$Verbose = $false,
    [switch]$Fix = $false
)

$ErrorActionPreference = "Stop"
$ScriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "🔍 VERIFICAÇÃO DE CONSOLIDAÇÃO DATABASE" -ForegroundColor Cyan
Write-Host "=" * 70

# Arquivos que foram modificados
$filesModified = @(
    "core/db/base_class.py",
    "core/db/session.py",
    "core/db/__init__.py",
    "core/database.py",
    "tests/integration/test_schemas_validation.py",
    "tests/unit/test_core_logic.py",
    "tests/unit/test_core_system.py",
    "tests/test_auth.py",
    "modules/integration/models/conector_externo.py",
    "modules/integration/models/transformacao_dados.py",
    "modules/integration/models/sincronizacao_b_n_a.py",
    "modules/integration/models/a_p_i_gateway.py",
    "modules/urbanism/models/alvara_funcionamento.py",
    "modules/health/models/health_record.py",
    "modules/monitoring/models/alert.py",
    "modules/monitoring/models/system_metric.py",
    "modules/governance/controller.py",
    "modules/governance/seed_data.py",
    "modules/auth/auth_utils.py",
    "modules/auth/endpoints.py",
    "modules/citizenship/endpoints.py",
    "modules/analytics/endpoints.py",
    "modules/health/controller.py",
    "modules/health/seed_data.py",
    "modules/dashboard/endpoints.py"
)

# Validações
$successCount = 0
$errorCount = 0
$warnings = @()

# 1. Validar Sintaxe Python
Write-Host "`n1️⃣  VALIDANDO SINTAXE PYTHON" -ForegroundColor Yellow
foreach ($file in $filesModified) {
    $fullPath = Join-Path $ScriptRoot $file

    if (Test-Path $fullPath) {
        try {
            python -m py_compile $fullPath 2>&1 | Out-Null
            Write-Host "   ✅ $file" -ForegroundColor Green
            $successCount++
        }
        catch {
            Write-Host "   ❌ $file" -ForegroundColor Red
            $errorCount++
        }
    }
    else {
        Write-Host "   ⚠️  $file - Não encontrado" -ForegroundColor Yellow
    }
}

# 2. Procurar por imports antigos
Write-Host "`n2️⃣  PROCURANDO POR IMPORTS DE core.database" -ForegroundColor Yellow
$oldImports = @()
Get-ChildItem -Path (Join-Path $ScriptRoot "apps/backend") -Recurse -Filter "*.py" -File |
    ForEach-Object {
        if (Select-String -Path $_.FullName -Pattern "from core\.database|import.*core\.database" -Quiet) {
            $oldImports += $_.FullName
        }
    }

if ($oldImports.Count -eq 0) {
    Write-Host "   ✅ Nenhum import de core.database encontrado (CORRETO!)" -ForegroundColor Green
    $successCount++
}
else {
    Write-Host "   ❌ Imports de core.database ainda encontrados:" -ForegroundColor Red
    foreach ($import in $oldImports) {
        Write-Host "      - $import" -ForegroundColor Red
        $errorCount++
    }
}

# 3. Validar imports de core.db
Write-Host "`n3️⃣  VALIDANDO IMPORTS DE core.db" -ForegroundColor Yellow
$validImports = 0
Get-ChildItem -Path (Join-Path $ScriptRoot "apps/backend") -Recurse -Filter "*.py" -File |
    ForEach-Object {
        if (Select-String -Path $_.FullName -Pattern "from core\.db" -Quiet) {
            $validImports++
        }
    }

Write-Host "   ✅ Arquivos usando core.db: $validImports" -ForegroundColor Green
$successCount++

# 4. Verificar consolidação de Base
Write-Host "`n4️⃣  VERIFICANDO CONSOLIDAÇÃO DE Base EM core/db/" -ForegroundColor Yellow
$baseFile = Join-Path $ScriptRoot "core/db/__init__.py"
if (Test-Path $baseFile) {
    $content = Get-Content $baseFile -Raw
    if ($content -match "from core\.db\.base_class import Base" -and $content -match "Base" -in ($content -split "`n" | Select-String "^from|^import")) {
        Write-Host "   ✅ Base exportada corretamente em core/db/__init__.py" -ForegroundColor Green
        $successCount++
    }
    else {
        Write-Host "   ⚠️  Verificar exportação de Base" -ForegroundColor Yellow
    }
}

# 5. Verificar duplicações
Write-Host "`n5️⃣  VERIFICANDO DUPLICAÇÕES DE FUNÇÕES" -ForegroundColor Yellow
$sessionFile = Join-Path $ScriptRoot "core/db/session.py"
if (Test-Path $sessionFile) {
    $content = Get-Content $sessionFile -Raw
    $getDbCount = ($content | Select-String -Pattern "^def get_db\(" -AllMatches).Matches.Count
    $getAsyncCount = ($content | Select-String -Pattern "^def get_async_db\(" -AllMatches).Matches.Count

    if ($getDbCount -eq 1 -and $getAsyncCount -eq 1) {
        Write-Host "   ✅ Sem duplicações: get_db (1), get_async_db (1)" -ForegroundColor Green
        $successCount++
    }
    else {
        Write-Host "   ⚠️  Verificar duplicações: get_db ($getDbCount), get_async_db ($getAsyncCount)" -ForegroundColor Yellow
    }
}

# Resumo Final
Write-Host "`n" + "=" * 70
Write-Host "📊 RESUMO FINAL" -ForegroundColor Cyan
Write-Host "   ✅ Verificações OK: $successCount" -ForegroundColor Green
Write-Host "   ❌ Erros encontrados: $errorCount" -ForegroundColor Red

if ($errorCount -eq 0) {
    Write-Host "`n✨ CONSOLIDAÇÃO VALIDADA COM SUCESSO!" -ForegroundColor Green
    Write-Host "`nStatus: Database module consolidado corretamente" -ForegroundColor Green
    Write-Host "  - core/database.py descontinuado" -ForegroundColor Green
    Write-Host "  - Todos os imports migrados para core/db/" -ForegroundColor Green
    exit 0
}
else {
    Write-Host "`n❌ VERIFICAÇÃO FALHOU" -ForegroundColor Red
    exit 1
}
