# AI Lecture Assistant - Prod Startup
Write-Host "🛡️ Starting AI Lecture Assistant (Production)..." -ForegroundColor Cyan

# 1. Verify environment
if (-not (Test-Path .env)) {
    Write-Host "❌ ERROR: .env file is required for production!" -ForegroundColor Red
    exit 1
}

# 2. Create required directories
$dirs = "storage/meetings", "storage/logs", "storage/temp", "storage/cache", "storage/uploads"
foreach ($dir in $dirs) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Force -Path $dir | Out-Null
    }
}

# 3. Run migrations
if (Test-Path "backend/app/migrations") {
    Write-Host "Applying production migrations..."
    alembic upgrade head
}

# 4. Start Backend
Write-Host "Launching production server..."
uvicorn backend.app.main:app `
    --host 0.0.0.0 `
    --port 8000 `
    --workers 4 `
    --log-level info `
    --proxy-headers `
    --timeout-keep-alive 65
