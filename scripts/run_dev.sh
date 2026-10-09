#!/bin/bash
set -e

echo "🚀 Starting AI Lecture Assistant (Development)..."

# 1. Verify environment
if [ ! -f .env ]; then
    echo "❌ .env file not found. Copying from .env.example..."
    cp .env.example .env
    echo "⚠️  Please update .env with your actual keys!"
fi

# 2. Create required directories
mkdir -p storage/meetings storage/logs storage/temp storage/cache storage/uploads

# 3. Run migrations (assumes alembic is used)
if [ -d "backend/app/migrations" ]; then
    echo "Running migrations..."
    alembic upgrade head
fi

# 4. Start Backend
echo "Starting backend..."
uvicorn backend.app.main:app --reload --port 8000
