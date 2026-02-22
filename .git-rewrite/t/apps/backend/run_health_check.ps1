# SILA Complete Health Verification Pipeline
# Usage: .\run_health_check.ps1

Write-Host "🩺 Starting SILA Complete Health Verification..." -ForegroundColor Green
Write-Host "=" * 70

# Step 1: Service Discovery
Write-Host "`n📋 Step 1: Service Discovery" -ForegroundColor Yellow
python scripts/generate_services_map.py

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Service discovery failed" -ForegroundColor Red
    exit 1
}

# Step 2: Ensure server is running
Write-Host "`n🌐 Step 2: Server Health Check" -ForegroundColor Yellow

$serverReady = $false
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/docs" -TimeoutSec 3 -ErrorAction SilentlyContinue
    if ($response.StatusCode -eq 200) {
        $serverReady = $true
        Write-Host "✅ Server is running" -ForegroundColor Green
    }
} catch {
    Write-Host "⚠️  Server not running, starting Uvicorn..." -ForegroundColor Yellow
    Start-Process -NoNewWindow -FilePath "python" -ArgumentList "-m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

    # Wait for server
    Write-Host "⏳ Waiting for server initialization..." -ForegroundColor Yellow
    for ($i = 0; $i -lt 20; $i++) {
        try {
            $response = Invoke-WebRequest -Uri "http://localhost:8000/docs" -TimeoutSec 2 -ErrorAction SilentlyContinue
            if ($response.StatusCode -eq 200) {
                $serverReady = $true
                Write-Host "✅ Server started successfully" -ForegroundColor Green
                break
            }
        } catch {}
        Start-Sleep -Seconds 1
    }
}

if (-not $serverReady) {
    Write-Host "❌ Server failed to start within expected time" -ForegroundColor Red
    exit 1
}

# Step 3: Comprehensive Testing
Write-Host "`n🧪 Step 3: Comprehensive Service Testing" -ForegroundColor Yellow
python scripts/test_all_services.py

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Service testing failed" -ForegroundColor Red
    exit 1
}

# Step 4: Health Dashboard Generation
Write-Host "`n📊 Step 4: Health Dashboard Generation" -ForegroundColor Yellow
python scripts/module_health_dashboard.py

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Dashboard generation failed" -ForegroundColor Red
    exit 1
}

Write-Host "`n" + "=" * 70
Write-Host "✅ HEALTH VERIFICATION COMPLETE!" -ForegroundColor Green
Write-Host "📄 Open 'module_health_dashboard.html' for complete status" -ForegroundColor Cyan
Write-Host "📋 Open 'services_test_report.json' for detailed results" -ForegroundColor Cyan
Write-Host "📖 Open 'modules_services.json' for service catalog" -ForegroundColor Cyan
