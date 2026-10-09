# AI Lecture Assistant

# AI Rules

> Version: 1.0.0
>
> Status: Critical
>
> Audience: AI Coding Agents
>
> Priority: Highest
>
> This document defines the mandatory engineering rules that every AI agent must follow while contributing to this repository.

---

# Purpose

This document ensures that all AI-generated code remains:

- Consistent
- Modular
- Maintainable
- Scalable
- Testable
- Well documented

Every AI agent must read this file before modifying the repository.

---

# Golden Rule

> Never optimize for writing code quickly.
>
> Optimize for writing code that will still be understandable and maintainable two years from now.

---

# Core Principles

Every implementation must follow:

- Single Responsibility Principle
- Separation of Concerns
- DRY (Don't Repeat Yourself)
- KISS (Keep It Simple)
- SOLID Principles
- Explicit over Implicit
- Readability over Cleverness

---

# Before Writing Code

Always understand:

- The current architecture
- The affected module
- Existing implementations
- Dependencies
- Future roadmap

Never start coding without understanding the surrounding system.

---

# Before Creating a New File

Ask:

- Does a similar file already exist?
- Can existing functionality be extended?
- Does the new file belong in this folder?
- Is a new abstraction actually needed?

Avoid unnecessary files.

---

# Before Creating a New Class

Verify:

- A class is actually needed.
- One responsibility only.
- No duplicate behavior.
- Interface is clear.

---

# Before Creating a Function

Function should:

- Perform one task
- Be easy to test
- Have descriptive naming
- Avoid hidden side effects

Target length

20–40 lines

Split larger functions.

---

# Folder Rules

API

Only endpoints.

Services

Business logic only.

Repositories

Database access only.

Models

ORM models only.

Schemas

Validation only.

Agents

Autonomous modules only.

Utils

Generic reusable helpers only.

Never violate folder ownership.

---

# API Rules

- Thin route handlers.
- Validate every request.
- Return consistent JSON.
- Never access the database directly.
- Call services only.

---

# Service Rules

Services may:

- Call repositories
- Call AI agents
- Publish events
- Coordinate workflows

Services should not:

- Know HTTP
- Know UI
- Return HTML

---

# Repository Rules

Repositories only:

- Read
- Insert
- Update
- Delete

No business logic.

No AI logic.

---

# Database Rules

- SQLAlchemy ORM
- Migrations required
- Foreign keys where applicable
- UUID primary keys
- Timestamp fields
- Never store secrets

---

# AI Rules

Every AI request must go through:

LLM Router

Never call providers directly.

Never hardcode providers.

Never hardcode model names.

---

# Whisper Rules

Use faster-whisper.

Support configurable models.

Support CPU.

GPU optional.

---

# Prompt Rules

Prompts belong inside:

```
prompts/
```

Never embed large prompts inside Python files.

Prompts should be reusable.

---

# Event Rules

Prefer events over direct dependencies.

Example

Meeting Joined

↓

Audio Started

↓

Transcript Ready

↓

Notes Generated

Avoid tightly coupled modules.

---

# Logging Rules

Every important operation must log:

- Module
- Action
- Timestamp
- Duration
- Status
- Errors

Logs should help diagnose failures.

---

# Error Handling Rules

Never swallow exceptions.

Never ignore failures.

Provide meaningful messages.

Retry when appropriate.

Preserve data.

Fail gracefully.

---

# Configuration Rules

Everything configurable.

Never hardcode:

- API keys
- Model names
- File paths
- Ports
- Timeouts

Use configuration.

---

# Storage Rules

Store:

Raw Audio

Transcript

Notes

Summary

Quiz

Flashcards

PDF

Every lecture has its own folder.

Never overwrite raw files.

---

# Naming Rules

Classes

PascalCase

Functions

snake_case

Variables

snake_case

Constants

UPPER_CASE

Files

snake_case.py

Folders

lowercase

---

# Documentation Rules

Whenever architecture changes:

Update

04_SYSTEM_ARCHITECTURE.md

Whenever new agents are added:

Update

05_AI_AGENT_ARCHITECTURE.md

Whenever APIs change:

Update

09_API_SPECIFICATION.md

Whenever configuration changes:

Update

11_CONFIGURATION.md

Documentation is mandatory.

---

# Testing Rules

Every new feature should include:

- Unit Tests
- Integration Tests (when applicable)

Every bug fix should include:

- Regression Test

Never merge untested code.

---

# Performance Rules

Avoid:

Repeated database queries

Repeated AI requests

Repeated file reads

Prefer:

Caching

Batch processing

Streaming

where appropriate.

---

# Security Rules

Never expose:

API Keys

Secrets

Credentials

Tokens

Validate every external input.

Sanitize file names.

Protect sensitive information.

---

# Code Review Checklist

Before considering work complete, verify:

- Architecture respected
- Correct folder
- No duplicate logic
- Small functions
- Type hints
- Validation
- Logging
- Tests
- Documentation
- Clean naming

If any answer is "No", revise the implementation.

---

# Pull Request Checklist

Every contribution should include:

- Updated documentation
- Passing tests
- Clean formatting
- No dead code
- No debug prints
- No TODOs without issue references

---

# Anti-Patterns

Never:

- Write 500-line classes
- Write massive functions
- Hardcode configuration
- Mix UI with business logic
- Mix AI with storage
- Duplicate prompts
- Ignore exceptions
- Skip validation
- Break module ownership

---

# AI Self-Review

Before finishing any task, ask:

1. Is this modular?

2. Is this testable?

3. Is this configurable?

4. Is this documented?

5. Is this reusable?

6. Is this maintainable?

7. Is this scalable?

8. Does it follow the architecture?

If any answer is "No", improve the implementation before submitting.

---

# Final Rule

Do not write code simply because it works.

Write code that another developer—or another AI—can understand, modify, test, and extend with confidence.

The long-term health of the project is more important than short-term speed.
