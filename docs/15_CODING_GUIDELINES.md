# AI Lecture Assistant

# Coding Guidelines

> Version: 1.0.0
>
> Status: Active
>
> Priority: High
>
> Audience:
>
> - Developers
> - AI Coding Agents
>
> This document defines the official coding standards for the project.

---

# Purpose

The goal of these guidelines is to ensure that the codebase remains:

- Consistent
- Readable
- Testable
- Maintainable
- Scalable

Code should be written for humans first and computers second.

---

# General Principles

Follow these principles in every module.

- Readability over cleverness.
- Simplicity over unnecessary abstraction.
- Explicit over implicit behavior.
- Composition over inheritance where appropriate.
- Small modules.
- Small functions.
- Clear interfaces.

---

# Project Languages

Backend

Python 3.12+

Frontend

TypeScript

Database

SQLAlchemy ORM

Configuration

YAML

Documentation

Markdown

---

# Naming Conventions

## Files

```
meeting_agent.py

notes_service.py

meeting_repository.py
```

Use

snake_case

---

## Classes

```
MeetingAgent

StorageService

TranscriptRepository
```

Use

PascalCase

---

## Functions

```
join_meeting()

save_transcript()

generate_notes()
```

Use

snake_case

---

## Variables

```
meeting_id

transcript_path

audio_duration
```

Use

snake_case

---

## Constants

```
MAX_RETRIES

DEFAULT_PROVIDER

APP_VERSION
```

Use

UPPER_CASE

---

# Function Guidelines

A function should

- Do one thing.
- Be easy to understand.
- Be easy to test.

Preferred length

20–40 lines

Maximum

60 lines

If longer, split it.

---

# Class Guidelines

A class should own one responsibility.

Good

MeetingAgent

Bad

MeetingAudioTranscriptNotesManager

Keep classes focused.

---

# Comments

Write comments only when necessary.

Good

Explain "why".

Avoid

Explaining "what" obvious code is doing.

Example

Good

```
Retry because AI providers may return temporary rate-limit errors.
```

Bad

```
Increment i.
```

---

# Docstrings

Every public class and function should have a docstring.

Example

```python
def join_meeting(url: str) -> bool:
    """
    Join a Google Meet using the provided URL.

    Args:
        url: Google Meet link.

    Returns:
        True if the meeting was joined successfully.
    """
```

---

# Type Hints

Always use type hints.

Good

```python
def generate_notes(transcript: str) -> str:
```

Avoid

```python
def generate_notes(transcript):
```

---

# Imports

Standard Library

↓

Third-party Libraries

↓

Internal Modules

Example

```python
import os
from pathlib import Path

from fastapi import APIRouter

from app.services.notes_service import NotesService
```

---

# Error Handling

Always handle expected errors.

Never

```
except:
```

Use

```python
except FileNotFoundError:
```

Log the error.

Return meaningful information.

---

# Logging

Never use

```
print()
```

Use

Python logging.

Every log should include

- Module
- Event
- Status

Example

```
Meeting joined successfully.
```

---

# Configuration

Never hardcode

- API keys
- File paths
- Ports
- Models
- Timeouts

Everything comes from configuration.

---

# API Design

Routes

↓

Services

↓

Repositories

↓

Database

Never skip layers.

---

# Database

Use SQLAlchemy.

Avoid raw SQL unless necessary.

Always

- Use relationships
- Use constraints
- Use migrations

---

# AI Integration

Every AI request

↓

LLM Router

↓

Provider

Never call providers directly.

---

# Prompt Management

Store prompts in

```
prompts/
```

Never embed large prompts in code.

Prompts should be reusable.

---

# File Organization

Each file should focus on one responsibility.

Good

```
meeting_agent.py
```

Bad

```
meeting_audio_notes_utils.py
```

---

# Testing

Every feature should have

- Unit tests
- Integration tests (when needed)

Every bug fix

↓

Regression test

---

# Performance

Avoid

Repeated AI calls

Repeated file reads

Repeated database queries

Use caching when appropriate.

---

# Async Programming

Use async only where it provides real benefit.

Examples

- API requests
- Browser automation
- File streaming

Avoid unnecessary async complexity.

---

# Frontend Guidelines

Use

Reusable components.

Centralized API services.

Typed interfaces.

Avoid duplicated UI logic.

---

# Git Commit Style

Format

```
type(scope): message
```

Examples

```
feat(meeting): add Google Meet join support

fix(storage): resolve transcript save issue

docs(api): update endpoint documentation

test(notes): add summary generation tests
```

---

# Branch Naming

Examples

```
feature/meeting-agent

feature/whisper

bugfix/audio-sync

docs/api-update
```

---

# Code Review Checklist

Before merging, verify

- Builds successfully
- Tests pass
- Documentation updated
- No dead code
- No debug prints
- No TODO without issue reference
- Architecture respected
- Naming consistent

---

# AI Generated Code Checklist

Before accepting AI-generated code

- Correct module?
- Correct folder?
- Uses configuration?
- Uses logging?
- Uses type hints?
- Uses docstrings?
- Has tests?
- Avoids duplication?
- Follows architecture?

If any answer is "No", revise the implementation.

---

# Refactoring Rules

Refactor when

- Duplicate code exists.
- Function becomes too large.
- Class has multiple responsibilities.
- Logic becomes difficult to understand.

Avoid unnecessary refactoring.

---

# Security Guidelines

Never

- Expose secrets
- Trust user input
- Log API keys

Always

- Validate input
- Sanitize filenames
- Handle exceptions

---

# Documentation Guidelines

Whenever code changes

Verify whether any of these documents require updates

- System Architecture
- API Specification
- Database Design
- Configuration
- AI Context

Documentation should evolve with the code.

---

# Final Philosophy

Write code that another developer—or another AI—can understand within minutes.

Readable, modular, and well-tested code is more valuable than clever code.

Every contribution should improve the overall quality of the project.
