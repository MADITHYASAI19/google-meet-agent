# AI Lecture Assistant - Dev Startup
Write-Host "🚀 Starting AI Lecture Assistant (Development)..." -ForegroundColor Cyan

# 1. Verify environment
if (-not (Test-Path .env)) {
    Write-Host "❌ .env file not found. Copying from .env.example..." -ForegroundColor Yellow
    Copy-Item .env.example .env
    Write-Host "⚠️  Please update .env with your actual keys!" -ForegroundColor Yellow
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
    Write-Host "Running migrations..."
    alembic upgrade head
}

# 4. Start Backend
Write-Host "Starting backend..."
uvicorn backend.app.main:app --reload --port 8000
