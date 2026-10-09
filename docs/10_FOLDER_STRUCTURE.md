# AI Lecture Assistant

# Folder Structure

> Version: 1.0.0
>
> Status: Active
>
> Priority: High
>
> Related Documents
>
> - 04_SYSTEM_ARCHITECTURE.md
> - 08_DATABASE_DESIGN.md
> - 09_API_SPECIFICATION.md

---

# Purpose

This document defines the official directory structure of the AI Lecture Assistant.

Every source file, configuration file, generated artifact, and document must follow this structure.

Developers and AI coding agents should never create new top-level folders without updating this document.

---

# Repository Structure

```
AI-Lecture-Assistant/

│
├── backend/
├── frontend/
├── docs/
├── storage/
├── prompts/
├── scripts/
├── tests/
├── tools/
├── assets/
├── logs/
├── .github/
│
├── .env
├── .env.example
├── .gitignore
├── README.md
├── LICENSE
└── requirements.txt
```

---

# Root Directory

The root directory should contain only project-level files.

Allowed Files

```
README.md

LICENSE

.gitignore

.env

.env.example

requirements.txt

docker-compose.yml (Future)

pyproject.toml

package.json (Frontend)

Makefile (Future)
```

No source code should exist directly inside the root.

---

# Backend

```
backend/

├── app/
├── tests/
├── migrations/
├── requirements.txt
└── README.md
```

Purpose

Contains all backend source code.

---

# Backend Structure

```
backend/app/

├── api/
├── agents/
├── services/
├── database/
├── models/
├── schemas/
├── repositories/
├── middleware/
├── core/
├── config/
├── events/
├── workers/
├── utils/
├── constants/
├── exceptions/
└── main.py
```

---

# api/

Contains REST API endpoints.

Example

```
meeting.py

notes.py

summary.py

search.py
```

Only route definitions belong here.

Business logic is prohibited.

---

# agents/

Contains AI and automation agents.

Example

```
meeting_agent.py

audio_agent.py

whisper_agent.py

notes_agent.py

attendance_agent.py
```

Each file should contain one primary agent.

---

# services/

Contains business logic.

Example

```
meeting_service.py

notes_service.py

pdf_service.py

storage_service.py
```

Routes call services.

Services call repositories.

---

# database/

Contains

```
database.py

session.py

base.py
```

Responsible for database initialization.

---

# models/

Contains SQLAlchemy models.

Example

```
meeting.py

transcript.py

notes.py
```

No business logic.

---

# schemas/

Contains request and response models.

Example

```
meeting_schema.py

notes_schema.py
```

Used by FastAPI validation.

---

# repositories/

Contains database queries.

Example

```
meeting_repository.py

notes_repository.py
```

Only persistence logic.

---

# middleware/

Contains

- Logging
- Authentication (Future)
- Request timing
- Exception middleware

---

# core/

Contains application startup logic.

Example

```
startup.py

shutdown.py

application.py
```

---

# config/

Contains configuration.

Example

```
settings.py

logging.py
```

No secrets stored here.

---

# events/

Contains event definitions.

Example

```
meeting_events.py

transcript_events.py
```

Supports future event-driven architecture.

---

# workers/

Contains background workers.

Future Examples

```
pdf_worker.py

embedding_worker.py
```

---

# utils/

Contains reusable helper functions.

Example

```
file_utils.py

time_utils.py

hash_utils.py
```

Should not contain business logic.

---

# constants/

Stores

- enums
- constants
- event names

---

# exceptions/

Contains custom exception classes.

Example

```
MeetingException

StorageException

WhisperException
```

---

# Frontend

```
frontend/

├── app/
├── components/
├── hooks/
├── services/
├── lib/
├── styles/
├── types/
├── public/
└── tests/
```

---

# Frontend app/

Contains pages.

Examples

Dashboard

Meeting

History

Settings

Search

---

# components/

Reusable UI components.

Examples

Sidebar

Navbar

MeetingCard

TranscriptViewer

NotesViewer

---

# hooks/

Custom React hooks.

Example

```
useMeeting()

useTranscript()
```

---

# services/

API communication.

Example

```
meeting_api.ts

notes_api.ts
```

---

# lib/

Utilities.

Example

```
api_client.ts

formatter.ts
```

---

# public/

Images

Icons

Fonts

Logos

---

# Docs

```
docs/
```

Contains all documentation.

Every architectural change must update the relevant document.

---

# Storage

```
storage/

├── meetings/
├── audio/
├── transcripts/
├── notes/
├── summaries/
├── quizzes/
├── flashcards/
├── pdf/
├── exports/
└── temp/
```

Purpose

Stores all generated artifacts.

---

# Meeting Storage

Every lecture receives its own folder.

Example

```
meetings/

meeting_uuid/

    metadata.json

    audio.wav

    transcript.json

    notes.md

    summary.md

    quiz.md

    flashcards.json

    lecture.pdf
```

---

# Prompts

```
prompts/

meeting/

notes/

summary/

quiz/

flashcards/
```

Stores all LLM prompt templates.

Prompts should never be hardcoded.

---

# Scripts

```
scripts/

install.py

setup.py

backup.py

cleanup.py
```

Utility scripts.

---

# Tests

```
tests/

unit/

integration/

e2e/

fixtures/

mocks/
```

Every new module should have tests.

---

# Tools

Contains developer tools.

Examples

```
benchmark.py

token_counter.py

model_test.py
```

---

# Assets

Stores

- Images
- Logos
- Icons
- Screenshots

No generated data.

---

# Logs

Stores

Application logs

Error logs

Audit logs

Performance logs

---

# .github

Contains

GitHub Actions

Issue Templates

Pull Request Templates

Contribution Guide

---

# Naming Conventions

Folders

lowercase

snake_case

Files

snake_case.py

Classes

PascalCase

Functions

snake_case

Variables

snake_case

Constants

UPPER_CASE

---

# Ownership Rules

Every folder has one responsibility.

Example

models/

↓

Database Models

Only.

No services.

No APIs.

No utilities.

---

# Folder Dependency Rules

Allowed

```
API

↓

Services

↓

Repositories

↓

Database
```

Not Allowed

```
API

↓

Database
```

Business logic must always go through services.

---

# Rules

1. No source code in root.

2. One responsibility per folder.

3. No circular dependencies.

4. Prompts outside source code.

5. Generated files never committed.

6. Documentation always in docs/.

7. Tests mirror source structure.

8. Configuration separated from code.

9. Utilities remain generic.

10. Keep the repository clean.

---

# Summary

The AI Lecture Assistant follows a structured repository layout that separates concerns between APIs, services, agents, persistence, frontend, prompts, documentation, and generated artifacts.

Maintaining this structure is essential for scalability, readability, AI-assisted development, and long-term maintainability.
