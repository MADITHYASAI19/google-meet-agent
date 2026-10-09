# AI Lecture Assistant

# AI Context

> Version: 1.0.0
>
> Status: Critical
>
> This document is intended for AI coding agents.
>
> Read this file completely before generating, modifying, or reviewing code.

---

# Mission

Your goal is to help build the AI Lecture Assistant.

The objective is to build a production-quality, modular, maintainable, AI-powered lecture assistant that joins online meetings, captures audio, generates transcripts, detects attendance, produces structured study material, and stores everything locally.

You are expected to write clean, maintainable, and well-structured code.

---

# Project Goal

The application should be able to:

- Join Google Meet automatically.
- Capture meeting audio.
- Transcribe speech using faster-whisper.
- Detect attendance from spoken names.
- Generate structured lecture notes.
- Generate summaries.
- Generate quizzes.
- Generate flashcards.
- Export professional PDFs.
- Store all lecture artifacts locally.
- Support multiple AI providers.

---

# Project Philosophy

The project values:

- Simplicity
- Reliability
- Modularity
- Readability
- Extensibility
- Local-first execution

Avoid unnecessary complexity.

If two solutions satisfy the requirements, prefer the simpler one.

---

# Architecture Overview

Architecture Style

Modular Monolith

Backend

FastAPI

Frontend

Next.js

Speech Recognition

faster-whisper

Database

SQLite

ORM

SQLAlchemy

Browser Automation

Playwright

AI

LLM Router

Storage

Local filesystem

---

# Core Modules

The system consists of the following major modules.

- Meeting
- Audio
- Whisper
- Attendance
- Storage
- Search
- LLM Router
- Notes
- Summary
- Quiz
- Flashcards
- PDF
- Notification

Each module owns exactly one responsibility.

---

# AI Agent Responsibilities

Meeting Agent

Responsible only for joining and managing meetings.

Audio Agent

Responsible only for recording audio.

Whisper Agent

Responsible only for speech recognition.

Attendance Agent

Responsible only for attendance detection.

LLM Router

Responsible only for AI provider routing.

Notes Agent

Responsible only for classroom notes.

Summary Agent

Responsible only for lecture summaries.

Quiz Agent

Responsible only for quizzes.

Flashcard Agent

Responsible only for flashcards.

Storage Agent

Responsible only for persistence.

---

# What AI Must Never Do

Never merge unrelated responsibilities.

Never place database queries inside API routes.

Never place business logic inside API routes.

Never hardcode API keys.

Never hardcode file paths.

Never introduce global mutable state.

Never create circular dependencies.

Never duplicate existing functionality.

Never skip validation.

Never silently ignore exceptions.

---

# Coding Style

Use

- Type hints
- Docstrings
- Small functions
- Descriptive names
- Dependency injection where appropriate

Avoid

- Long functions
- Deep nesting
- Duplicate logic
- Unused code
- Hidden side effects

---

# Folder Responsibilities

api/

Only endpoints.

services/

Business logic.

repositories/

Database access.

models/

Database models.

schemas/

Validation.

agents/

AI agents.

utils/

Generic helpers.

No folder should violate its responsibility.

---

# Design Principles

- Single Responsibility Principle
- Dependency Inversion
- Separation of Concerns
- Loose Coupling
- High Cohesion
- Interface-driven design

---

# Event-Driven Communication

Modules should communicate using events where possible.

Example

Meeting Joined

↓

Audio Started

↓

Transcript Ready

↓

Notes Generated

Avoid direct coupling between modules.

---

# Error Handling

Every recoverable error should:

- Be logged.
- Return a meaningful message.
- Preserve existing data.
- Allow retries where appropriate.

Never terminate the entire application because one module fails.

---

# Logging Rules

Every important action should log:

- Timestamp
- Module
- Event
- Duration
- Status
- Error (if any)

Logs should help diagnose failures.

---

# Database Rules

Use SQLAlchemy.

Never write raw SQL unless necessary.

Always use migrations.

Never expose ORM models directly through APIs.

Store metadata in the database.

Store large files on disk.

---

# AI Provider Rules

All AI requests must pass through the LLM Router.

No module should directly call OpenAI, Grok, Gemini, or any future provider.

Responses must be normalized before returning to agents.

---

# Whisper Rules

Use faster-whisper.

Support configurable models.

Support CPU execution by default.

Do not assume GPU availability.

---

# File Storage Rules

Store every lecture in its own directory.

Example

storage/

meeting_uuid/

    audio.wav

    transcript.json

    notes.md

    summary.md

    lecture.pdf

Never overwrite raw audio or transcripts.

---

# API Rules

REST API

Versioned

Consistent JSON responses

Proper HTTP status codes

Validation using Pydantic

No business logic inside route handlers.

---

# Frontend Rules

Use reusable components.

Avoid duplicated UI.

Use API services.

Avoid direct fetch calls throughout components.

Centralize API access.

---

# Performance Goals

Meeting Join

<15 seconds

Whisper Delay

<5 seconds

Attendance Detection

<2 seconds

Dashboard Load

<2 seconds

Summary Generation

<20 seconds

---

# Security Rules

Never expose secrets.

Never log API keys.

Validate all user input.

Sanitize filenames.

Use environment variables for credentials.

---

# Documentation Rules

When changing architecture:

Update

04_SYSTEM_ARCHITECTURE.md

When adding agents:

Update

05_AI_AGENT_ARCHITECTURE.md

When adding APIs:

Update

09_API_SPECIFICATION.md

When adding configuration:

Update

11_CONFIGURATION.md

Documentation is part of the implementation.

---

# Current Project Status

Completed

- Architecture Design
- Agent Design
- Data Flow
- Database Design
- API Design
- Folder Structure
- Configuration Design

Next Priority

- Backend Foundation
- Meeting Agent
- Audio Pipeline
- Whisper Integration

---

# Future Roadmap

- RAG
- Vector Database
- Local LLM
- Plugin System
- Multi-user Support
- Analytics
- Calendar Integration

Design current code to support these features without requiring major refactoring.

---

# AI Decision Checklist

Before generating code, ask:

- Does this belong in the correct module?
- Am I duplicating functionality?
- Is the code testable?
- Is the code modular?
- Is it configurable?
- Is it documented?
- Is it scalable?
- Does it follow project architecture?

If any answer is "No", redesign before coding.

---

# Final Instruction

You are contributing to a long-term software project, not solving an isolated coding problem.

Prioritize maintainability, clarity, modularity, and correctness over speed.

Every implementation should make the project easier to extend in the future.
