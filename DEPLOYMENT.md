# Deployment Guide

## Local Development
1. Install Python 3.12.
2. Run `scripts/run_dev.sh` (Linux/Mac) or `scripts/run_dev.ps1` (Windows).

## Docker Deployment (Recommended)
1. Ensure Docker and Docker Compose are installed.
2. Configure your `.env` file.
3. Run:
   ```bash
   docker-compose up --build -d
   ```

## Production VPS Deployment
1. Install Docker and Docker Compose.
2. Set up a reverse proxy (Nginx or Traefik) to handle SSL/TLS.
3. Deploy using the Docker Compose method.

## Database Migrations
The system uses Alembic for migrations. To run migrations manually:
```bash
alembic upgrade head
```

## Troubleshooting
- **Whisper Issues**: Ensure FFmpeg is installed on the host or inside the container.
- **Browser Issues**: Ensure the Chromium dependencies are installed (handled by Dockerfile).
- **Permissions**: Ensure the `storage/` directory is writable by the application user.
