#!/bin/bash
set -e

echo "🛡️ Starting AI Lecture Assistant (Production)..."

# 1. Verify environment
if [ ! -f .env ]; then
    echo "❌ ERROR: .env file is required for production!"
    exit 1
fi

# 2. Create required directories
mkdir -p storage/meetings storage/logs storage/temp storage/cache storage/uploads

# 3. Run migrations
if [ -d "backend/app/migrations" ]; then
    echo "Applying production migrations..."
    alembic upgrade head
fi

# 4. Start Backend with production worker config
echo "Launching production server..."
exec uvicorn backend.app.main:app \
    --host 0.0.0.0 \
    --port 8000 \
    --workers 4 \
    --log-level info \
    --proxy-headers \
    --timeout-keep-alive 65
