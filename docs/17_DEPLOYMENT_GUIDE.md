# AI Lecture Assistant

# Deployment Guide

> Version: 1.0.0
>
> Status: Active
>
> Priority: High
>
> Audience
>
> - Developers
> - AI Coding Agents
>
> This document explains how to install, configure, run, update, and maintain the AI Lecture Assistant.

---

# Purpose

This document provides the official deployment process for the project.

It covers

- Local development
- Environment setup
- Database initialization
- Running the application
- Updating the application
- Backup
- Recovery
- Future production deployment

---

# Deployment Philosophy

Current Target

Single User

Local Machine

Future Target

Cloud Deployment

The project should always work locally without requiring Docker or cloud services.

---

# System Requirements

Operating System

- Windows 11
- Ubuntu 24.04+
- macOS (Future)

Python

```
3.12+
```

Node.js

```
20+
```

RAM

Minimum

```
8 GB
```

Recommended

```
16 GB
```

Disk Space

```
5 GB Free
```

Internet

Required only for AI providers.

---

# Required Software

Python

Node.js

Git

Google Chrome

Playwright Browsers

---

# Initial Setup

Clone Repository

```bash
git clone <repository-url>

cd AI-Lecture-Assistant
```

---

# Backend Setup

Create Virtual Environment

```bash
python -m venv .venv
```

Activate

Windows

```bash
.venv\Scripts\activate
```

Linux

```bash
source .venv/bin/activate
```

Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Frontend Setup

```bash
cd frontend

npm install
```

Return

```bash
cd ..
```

---

# Playwright Installation

Install Browser

```bash
playwright install
```

Verify

```bash
playwright --version
```

---

# Whisper Setup

Install

```bash
pip install faster-whisper
```

Verify

```bash
python

>>> from faster_whisper import WhisperModel
```

---

# Configuration

Copy

```
.env.example
```

↓

```
.env
```

Update

```
GROK_API_KEY

OPENAI_API_KEY

GEMINI_API_KEY
```

Never commit `.env`.

---

# Storage Initialization

Create

```
storage/

logs/

temp/
```

If missing, the application should create them automatically.

---

# Database Initialization

Run

```bash
alembic upgrade head
```

Verify

Database file exists

```
storage/database.db
```

---

# Starting Backend

```bash
uvicorn backend.app.main:app --reload
```

Expected

```
http://localhost:8000
```

---

# Starting Frontend

```bash
cd frontend

npm run dev
```

Expected

```
http://localhost:3000
```

---

# Health Check

Open

```
http://localhost:8000/api/v1/health
```

Expected

```json
{
    "status":"healthy"
}
```

---

# First Run Checklist

Verify

- Backend starts
- Frontend starts
- Database exists
- Storage folders created
- API responds
- Browser launches
- Configuration loads
- AI providers configured

---

# Running Tests

Backend

```bash
pytest
```

Coverage

```bash
pytest --cov
```

Frontend

```bash
npm test
```

---

# Updating Dependencies

Python

```bash
pip install -r requirements.txt --upgrade
```

Frontend

```bash
npm update
```

---

# Backup

Backup

```
storage/

database.db

.env

logs/
```

Recommended

Daily backup during development.

---

# Restore

Restore

```
database.db

storage/

.env
```

Restart application.

---

# Logs

Application logs

```
logs/app.log
```

Errors

```
logs/error.log
```

Debug

```
logs/debug.log
```

---

# Troubleshooting

## Backend fails to start

Check

- Python version
- Missing packages
- Configuration
- Port conflicts

---

## Frontend fails

Check

- Node version
- npm install
- API URL

---

## Whisper not working

Verify

- faster-whisper installed
- CPU supported
- Audio file valid

---

## Browser Automation fails

Verify

- Chrome installed
- Playwright installed
- Browser permissions
- Meet URL valid

---

## AI Provider Error

Check

- API Key
- Internet
- Provider Status
- Model Name

---

# Upgrade Process

Before upgrading

1. Backup database
2. Backup storage
3. Backup .env

Update

```bash
git pull
```

Run

```bash
pip install -r requirements.txt

npm install

alembic upgrade head
```

Restart application.

---

# Recovery

If the project becomes corrupted

1. Restore backup
2. Reinstall dependencies
3. Restore database
4. Restore storage
5. Restart application

No user data should be lost.

---

# Future Production Deployment

Planned

- Docker
- Reverse Proxy
- HTTPS
- PostgreSQL
- Cloud Storage
- CI/CD
- Monitoring

These are not required for the MVP.

---

# Deployment Rules

1. Never commit secrets.
2. Always use virtual environments.
3. Backup before upgrading.
4. Validate configuration before startup.
5. Run migrations before starting.
6. Verify health endpoint.
7. Test after deployment.
8. Keep logs enabled.
9. Use versioned releases.
10. Document deployment changes.

---

# Deployment Checklist

Before running

- Python installed
- Node installed
- Dependencies installed
- Browser installed
- Database initialized
- Environment configured
- Storage ready

After running

- Backend healthy
- Frontend healthy
- Database connected
- Browser automation working
- Whisper working
- AI providers responding

---

# Summary

The AI Lecture Assistant is designed to run locally with minimal setup.

Following this guide should allow a developer—or an AI coding agent—to install, configure, run, and recover the application in a consistent and repeatable manner.
