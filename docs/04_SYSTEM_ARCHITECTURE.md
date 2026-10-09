# AI Lecture Assistant

# System Architecture

> Version: 1.0.0
>
> Status: Active
>
> Last Updated: YYYY-MM-DD
>
> Related Documents:
>
> - 00_PROJECT_MASTER_PLAN.md
> - 01_PROJECT_OVERVIEW.md
> - 02_PRODUCT_VISION.md

---

# Purpose

This document defines the high-level architecture of the AI Lecture Assistant.

It explains:

- Overall system architecture
- Major components
- Module interactions
- Data flow
- Architectural principles
- Technology decisions

This document should answer one question:

> "How is the entire system designed?"

---

# Architecture Style

The project follows a **Modular Monolith Architecture**.

## Why Modular Monolith?

The application is designed for a single user and runs locally.

Microservices would introduce unnecessary complexity.

Benefits:

- Easier development
- Easier debugging
- Faster iteration
- Lower resource usage
- Simpler deployment

Every module remains logically independent while running inside one application.

---

# High-Level Architecture

```
                    AI Lecture Assistant

                           │
                           ▼

                    Next.js Frontend

                           │

                    REST API (FastAPI)

                           │

────────────────────────────────────────────────────

Backend

    │

    ├── Meeting Module

    ├── Audio Module

    ├── Whisper Module

    ├── Attendance Module

    ├── LLM Router

    ├── Notes Module

    ├── Storage Module

    ├── PDF Module

    ├── Search Module

    └── Configuration Module

────────────────────────────────────────────────────

Infrastructure

    │

    ├── SQLite

    ├── Local Storage

    ├── AI APIs

    └── Whisper Model
```

---

# Architectural Principles

The architecture follows these principles.

## 1. Single Responsibility

Every module has exactly one responsibility.

Example:

Meeting Module

Only joins and manages meetings.

Storage Module

Only stores data.

---

## 2. Loose Coupling

Modules should communicate through interfaces.

Example

Meeting Module

↓

Audio Module

↓

Whisper Module

No module should directly modify another module's internal logic.

---

## 3. High Cohesion

Related functionality belongs together.

Example

Attendance detection should not exist inside the Notes Module.

---

## 4. Separation of Concerns

UI

Business Logic

Storage

AI Processing

Configuration

must remain independent.

---

## 5. Local First

The application should work locally.

Cloud services should remain optional.

---

# Major Components

## Frontend

Responsibilities

- Dashboard
- Meeting Controls
- History
- Search
- Settings

Technology

- Next.js
- React
- TypeScript

---

## Backend

Responsibilities

- API
- Business Logic
- AI Orchestration
- Storage
- Authentication (Future)

Technology

- FastAPI

---

## Meeting Module

Responsibilities

- Join Google Meet
- Leave Meeting
- Browser Automation
- Meeting Lifecycle

Input

Google Meet URL

Output

Meeting Session

---

## Audio Module

Responsibilities

- Capture Audio
- Buffer Audio
- Save Audio

Input

Meeting Session

Output

Audio Stream

---

## Whisper Module

Responsibilities

- Speech Recognition
- Timestamp Generation
- Transcript Creation

Input

Audio Stream

Output

Transcript

---

## Attendance Module

Responsibilities

- Detect User Name
- Record Attendance
- Notify User

Input

Transcript

Output

Attendance Event

---

## LLM Router

Responsibilities

- Select AI Model
- Route Requests
- Handle Failover
- Manage Providers

Input

Transcript

Output

LLM Response

---

## Notes Module

Responsibilities

- Generate Notes
- Generate Summary
- Generate Quiz
- Generate Flashcards

Input

Transcript

Output

Learning Material

---

## Storage Module

Responsibilities

- Save Files
- Save Database
- Manage History

---

## Search Module

Responsibilities

- Search Notes
- Search Transcript
- Search Meetings

---

## PDF Module

Responsibilities

- Generate PDF
- Export Notes

---

# Layered Architecture

```
Presentation Layer

↓

API Layer

↓

Business Logic Layer

↓

AI Layer

↓

Persistence Layer

↓

Infrastructure Layer
```

---

# Component Relationships

```
Frontend

↓

Backend API

↓

Meeting Module

↓

Audio Module

↓

Whisper

↓

Transcript

↓

Attendance

↓

LLM Router

↓

Notes

↓

Storage

↓

Search
```

---

# Technology Stack

| Layer | Technology |
| --------- | ------------ |
| Frontend | Next.js |
| Backend | FastAPI |
| Browser Automation | Playwright |
| Speech Recognition | faster-whisper |
| AI Providers | OpenAI, Grok, Gemini |
| Database | SQLite |
| ORM | SQLAlchemy |
| PDF | ReportLab |
| Language | Python 3.12 |

---

# Data Storage

The system stores:

- Meeting Metadata
- Audio Files
- Transcript
- Notes
- Summary
- PDF
- Quiz
- Flashcards
- Attendance Events

Storage remains local by default.

---

# Error Handling Philosophy

Every module should fail independently.

Example

If AI generation fails:

Meeting recording should continue.

If PDF generation fails:

Notes should still be saved.

If one LLM provider fails:

Router should automatically switch providers if configured.

---

# Security Principles

API Keys

- Never hardcoded
- Loaded from environment variables

User Data

- Stored locally
- Never uploaded without permission

Logs

- Must never expose API keys

---

# Scalability

Current Target

- Single User

Future

- Multiple Users
- Cloud Deployment
- Shared Knowledge Base

The architecture should allow future expansion without major redesign.

---

# Performance Goals

Meeting Join

< 15 seconds

Attendance Detection

< 2 seconds

Transcript Delay

< 5 seconds

Search

< 1 second

Summary Generation

< 20 seconds

---

# Design Decisions

Why FastAPI?

- Async support
- Excellent performance
- Strong typing
- Easy API documentation

Why Next.js?

- Modern React framework
- Fast development
- Excellent ecosystem

Why SQLite?

- Lightweight
- No setup
- Perfect for single-user applications

Why Playwright?

- Reliable browser automation
- Cross-browser support
- Stable API

Why faster-whisper?

- Fast inference
- Local execution
- High transcription quality

---

# Architecture Constraints

The following constraints must always be respected.

- One backend application.
- No microservices.
- No shared mutable state between modules.
- No direct database access from the frontend.
- Every module communicates through service interfaces.
- Configuration only through environment variables.

---

# Future Architecture

Future versions may introduce:

- Plugin System
- Local LLM Support
- Vector Database
- RAG Engine
- Multi-platform Meeting Support
- Cloud Synchronization

The current architecture should allow these features without major restructuring.

---

# Related Documents

Next Document

05_AI_AGENT_ARCHITECTURE.md

This document explains every AI agent in detail.

---

# Summary

The AI Lecture Assistant follows a modular monolith architecture that emphasizes simplicity, maintainability, extensibility, and local-first execution.

Every major capability is isolated into independent modules, allowing the project to evolve into a larger AI learning platform while remaining easy to develop and maintain.
