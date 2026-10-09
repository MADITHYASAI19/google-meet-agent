# AI Lecture Assistant

# Configuration Guide

> Version: 1.0.0
>
> Status: Active
>
> Priority: High
>
> Related Documents
>
> - 04_SYSTEM_ARCHITECTURE.md
> - 05_AI_AGENT_ARCHITECTURE.md
> - 06_LLM_ROUTER.md

---

# Purpose

This document defines all runtime configuration used by the AI Lecture Assistant.

Every configurable value should originate from configuration rather than source code.

Configuration must be easy to modify without changing application logic.

---

# Configuration Hierarchy

Configuration is loaded in the following order.

```
Environment Variables

↓

.env

↓

config/default.yaml

↓

Runtime Overrides

↓

Application
```

Higher priority sources override lower priority ones.

---

# Configuration Categories

The application configuration is divided into the following categories.

- Application
- Server
- Database
- Storage
- Logging
- AI
- Whisper
- Meeting
- Frontend
- Feature Flags
- Security

---

# Environment Variables

The project uses a `.env` file for local development.

Example

```
APP_NAME=AI Lecture Assistant
APP_ENV=development
APP_DEBUG=true
APP_VERSION=1.0.0
```

---

# Server Configuration

```
HOST=127.0.0.1
PORT=8000
API_PREFIX=/api/v1
```

---

# Database Configuration

SQLite (MVP)

```
DATABASE_URL=sqlite:///storage/database.db
```

Future PostgreSQL

```
DATABASE_URL=postgresql://user:password@localhost/lecture_db
```

---

# Storage Configuration

```
STORAGE_PATH=storage/

MEETING_PATH=storage/meetings/

TRANSCRIPT_PATH=storage/transcripts/

NOTES_PATH=storage/notes/

PDF_PATH=storage/pdf/

TEMP_PATH=storage/temp/
```

---

# Logging Configuration

```
LOG_LEVEL=INFO

LOG_PATH=logs/

ENABLE_FILE_LOGGING=true

ENABLE_CONSOLE_LOGGING=true
```

Log Levels

- DEBUG
- INFO
- WARNING
- ERROR
- CRITICAL

---

# Whisper Configuration

```
WHISPER_MODEL=medium

WHISPER_DEVICE=cpu

WHISPER_COMPUTE_TYPE=int8

WHISPER_LANGUAGE=auto

WHISPER_BEAM_SIZE=5
```

Supported Models

- tiny
- base
- small
- medium
- large

---

# AI Configuration

Default Provider

```
DEFAULT_PROVIDER=grok
```

Default Model

```
DEFAULT_MODEL=grok-4-fast
```

Fallback Providers

```
FALLBACK_PROVIDERS=openai,gemini
```

Maximum Retries

```
MAX_AI_RETRIES=3
```

Timeout

```
AI_TIMEOUT=30
```

---

# API Keys

```
OPENAI_API_KEY=

GROK_API_KEY=

GEMINI_API_KEY=
```

Rules

- Never commit API keys.
- Never hardcode API keys.
- Read keys only from the environment.

---

# Meeting Configuration

```
AUTO_JOIN=false

AUTO_LEAVE=false

ENABLE_MIC=false

ENABLE_CAMERA=false

RECORD_AUDIO=true
```

---

# Attendance Configuration

```
ENABLE_ATTENDANCE=true

ATTENDANCE_CONFIDENCE=0.80

ATTENDANCE_TIMEOUT=5
```

---

# Notes Configuration

```
GENERATE_NOTES=true

GENERATE_SUMMARY=true

GENERATE_FLASHCARDS=true

GENERATE_QUIZ=true
```

---

# PDF Configuration

```
AUTO_EXPORT_PDF=true

PDF_THEME=default

PDF_PAGE_SIZE=A4
```

---

# Search Configuration

```
ENABLE_SEARCH=true

SEARCH_CACHE=true

MAX_SEARCH_RESULTS=100
```

---

# Feature Flags

```
ENABLE_RAG=false

ENABLE_VECTOR_SEARCH=false

ENABLE_SLIDE_OCR=false

ENABLE_CALENDAR=false

ENABLE_MULTI_USER=false
```

Feature flags allow unfinished functionality to remain disabled.

---

# Security Configuration

```
ENABLE_CORS=true

ENABLE_RATE_LIMIT=false

ENABLE_AUTH=false
```

Future

```
ENABLE_JWT=true

ENABLE_GOOGLE_LOGIN=true
```

---

# Performance Configuration

```
MAX_CONCURRENT_MEETINGS=1

MAX_CONCURRENT_AI_REQUESTS=3

MAX_UPLOAD_SIZE_MB=500
```

---

# Cache Configuration

Future

```
ENABLE_CACHE=true

CACHE_TTL=300
```

---

# Frontend Configuration

```
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1

NEXT_PUBLIC_APP_NAME=AI Lecture Assistant
```

---

# Configuration Validation

Every configuration value must be validated during application startup.

Examples

Database URL

✓ Valid

Port

Must be between 1 and 65535.

API Keys

Cannot be empty if the corresponding provider is enabled.

Storage Paths

Directories should exist or be created automatically.

---

# Configuration Loading

Application Startup

↓

Load `.env`

↓

Load YAML Configuration

↓

Validate Values

↓

Initialize Components

↓

Start Application

If validation fails, the application should stop with a clear error message.

---

# Runtime Configuration

Some settings can be changed without restarting the application.

Examples

- Theme
- Default AI Provider
- PDF Theme
- Search Options

Other settings require a restart.

Examples

- Database
- Whisper Model
- Server Port

---

# Configuration File Structure

```
config/

├── default.yaml

├── development.yaml

├── production.yaml

├── logging.yaml

└── prompts.yaml
```

Future environments can override only the values that differ.

---

# Best Practices

- Keep secrets outside the repository.
- Validate configuration before startup.
- Use meaningful defaults.
- Document every new configuration option.
- Avoid duplicate configuration values.
- Separate development and production settings.
- Keep configuration human-readable.

---

# Design Rules

1. No hardcoded secrets.
2. Environment variables override defaults.
3. Validate every configuration.
4. Fail fast on invalid settings.
5. Keep configuration modular.
6. Support future environments.
7. Use descriptive variable names.
8. Separate secrets from application settings.
9. Configuration changes should be logged.
10. Every configuration option must be documented.

---

# Summary

The AI Lecture Assistant uses a centralized configuration system to manage application behavior, AI providers, storage, logging, and future features.

A well-defined configuration layer keeps the application flexible, secure, and easy to maintain while allowing different environments to share the same codebase.
