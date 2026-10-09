# AI Lecture Assistant

# Project Master Plan

> **Version:** 1.0.0
>
> **Status:** Planning
>
> **Project Type:** Personal AI Productivity System
>
> **Development Style:** AI-Assisted Development
>
> **Primary Language:** Python
>
> **Backend:** FastAPI
>
> **Frontend:** Next.js
>
> **Architecture:** Modular Monolith
>
> **Deployment Target:** Local Machine (Windows)

---

# Document Purpose

This document is the **single source of truth** for the AI Lecture Assistant project.

Every developer, AI coding agent, contributor, or future maintainer **must read this document before making any changes to the codebase.**

This document explains:

- Why this project exists
- What problems it solves
- The long-term vision
- The development philosophy
- Architectural principles
- Scope of the MVP
- Future roadmap
- Repository organization
- Rules that every AI and developer must follow

If there is any conflict between code and documentation, this document has the highest priority until updated.

---

# Project Overview

AI Lecture Assistant is a **personal AI-powered meeting assistant** that automatically joins Google Meet lectures, captures audio, transcribes speech using Whisper, detects attendance calls, generates structured classroom notes using multiple LLMs, and builds a searchable personal knowledge base.

The project is designed primarily for **students** who attend online lectures and want accurate notes without manually writing everything.

Unlike traditional meeting assistants, this project focuses on **education**, not business meetings.

---

# Problem Statement

Students attending long online lectures often face several problems.

- Difficult to write notes while listening.
- Miss important concepts.
- Forget assignments.
- Forget important definitions.
- Difficult to revise before exams.
- Cannot search previous lectures efficiently.
- Attendance calls may be missed if attention is divided.

Current meeting assistants focus mainly on meeting summaries rather than classroom learning.

This project solves those problems.

---

# Vision

Build a personal AI learning assistant capable of becoming an intelligent study companion.

Long-term vision:

- Attend lectures automatically
- Build a personal knowledge base
- Generate revision material
- Answer questions from previous lectures
- Generate quizzes
- Generate flashcards
- Track learning progress
- Organize semester-wise notes automatically

The goal is **not** simply generating notes.

The goal is building an AI-powered learning ecosystem.

---

# Mission

Create an AI system that can transform every lecture into structured knowledge with minimal user interaction.

The user should never need to manually write lecture notes again.

---

# Primary Goals

The MVP must be able to:

- Join Google Meet automatically
- Capture lecture audio
- Transcribe lectures using faster-whisper
- Detect attendance calls
- Generate structured notes
- Generate lecture summaries
- Export notes to PDF
- Save transcripts locally
- Maintain meeting history

---

# Non Goals (MVP)

The first version will NOT include:

- Zoom support
- Microsoft Teams support
- Mobile application
- Multi-user support
- Cloud synchronization
- Calendar integration
- Speaker identification
- OCR on lecture slides
- Real-time collaborative editing

These may be added in future versions.

---

# Target Users

Current Target

- Single user
- Personal usage
- Windows laptop

Future Target

- Students
- Teachers
- Researchers
- Educational institutions

---

# MVP Scope

The MVP contains the following modules.

1. Meeting Agent
2. Audio Capture
3. Whisper Transcription
4. Attendance Detection
5. LLM Router
6. Notes Generation
7. Summary Generation
8. PDF Export
9. Storage Manager
10. Dashboard

No additional modules should be added until the MVP is stable.

---

# Core Features

## Meeting Automation

- Join Google Meet
- Leave automatically
- Disable microphone
- Disable camera

---

## Audio Pipeline

- Capture meeting audio
- Stream audio
- Save recordings

---

## Speech Recognition

- Faster Whisper
- Timestamp generation
- Incremental transcription

---

## Attendance Detection

Detect:

- User name
- Roll call
- Attendance events

Generate:

- Notification
- Timestamp
- Attendance log

---

## AI Notes

Generate:

- Classroom notes
- Bullet points
- Important concepts
- Definitions
- Examples
- Homework
- Assignments
- Action items

---

## PDF Export

Generate professional lecture notes.

---

## Search

Search previous lectures by:

- Topic
- Keyword
- Date
- Subject

---

# High-Level Architecture

```
                        AI Lecture Assistant

                               │
                               ▼

                        Meeting Agent

                               │
                               ▼

                         Audio Capture

                               │
                               ▼

                        Faster Whisper

                               │
                               ▼

                        Transcript Bus

        ┌──────────────────────┼──────────────────────┐

        ▼                      ▼                      ▼

 Attendance Agent       Storage Manager       Keyword Index

        │

        ▼

                        LLM Router

        ┌───────────────┼─────────────────┐

        ▼               ▼                 ▼

     OpenAI           Grok             Gemini

        │               │                 │

        └───────────────┼─────────────────┘

                        ▼

                 Merge / Review Agent

                        ▼

       Notes • Summary • Quiz • Flashcards • PDF
```

---

# Development Philosophy

This project follows several core principles.

## Documentation First

Every feature starts with documentation.

Code comes later.

---

## Modular Monolith

The project remains a single application.

Modules remain independent.

Microservices are intentionally avoided.

---

## Local First

Everything should work locally.

Cloud services should remain optional.

---

## AI Assisted Development

AI is treated as a development partner.

Every generated code must still follow project standards.

---

## Simplicity

Prefer simple solutions over clever solutions.

Readable code is more valuable than shorter code.

---

## Interface Driven Design

Modules communicate through well-defined interfaces.

Avoid tight coupling.

---

# AI Development Workflow

Every AI coding session must follow this workflow.

```
Understand

↓

Read Documentation

↓

Plan

↓

Implement

↓

Self Review

↓

Testing

↓

Update Documentation
```

Never skip documentation.

---

# Repository Structure

```
AI-Lecture-Assistant/

backend/

frontend/

docs/

storage/

tests/

scripts/

prompts/

models/
```

Each top-level directory has a single responsibility.

---

# Technology Stack

| Layer | Technology |
| --------- | ------------ |
| Backend | FastAPI |
| Frontend | Next.js |
| Browser Automation | Playwright |
| Speech Recognition | faster-whisper |
| AI Models | OpenAI / Grok / Gemini |
| Database | SQLite |
| ORM | SQLAlchemy |
| PDF | ReportLab |
| Language | Python 3.12 |

---

# Project Principles

The following principles are permanent.

1. Documentation before implementation.

2. One module should have one responsibility.

3. No duplicated business logic.

4. No hardcoded configuration.

5. Environment variables must be used.

6. Every module should be independently testable.

7. AI-generated code should remain readable.

8. Small functions are preferred over very large functions.

9. Every architectural change must update documentation.

10. Production-quality code from day one.

---

# Success Criteria

The MVP is considered complete when the system can:

- Join a Google Meet
- Capture lecture audio
- Generate transcripts
- Detect attendance
- Generate classroom notes
- Generate summaries
- Export PDF
- Save lecture history
- Search previous lectures

without manual intervention.

---

# Future Vision

Future versions may include:

- Chat with lectures (RAG)
- Flashcard generation
- Quiz generation
- Calendar integration
- OCR for shared slides
- Learning analytics
- Speaker identification
- Notion export
- Obsidian export
- Multi-language support

---

# Documentation Roadmap

The documentation should be read in this order.

```
00_PROJECT_MASTER_PLAN.md

↓

01_PROJECT_OVERVIEW.md

↓

02_PRODUCT_VISION.md

↓

03_SRS.md

↓

04_SYSTEM_ARCHITECTURE.md

↓

05_AI_AGENT_ARCHITECTURE.md

↓

06_LLM_ROUTER.md

↓

07_DATA_FLOW.md

↓

08_DATABASE_DESIGN.md

↓

09_API_SPECIFICATION.md

↓

10_FOLDER_STRUCTURE.md

↓

11_CONFIGURATION.md

↓

12_AI_CONTEXT.md

↓

13_AI_RULES.md

↓

14_PROJECT_MEMORY.md

↓

15_CODING_GUIDELINES.md

↓

16_TESTING_GUIDE.md

↓

17_DEPLOYMENT_GUIDE.md

↓

18_ROADMAP.md

↓

19_CHANGELOG.md
```

---

# Final Statement

This project is intended to be a **production-quality, AI-first software system**.

Every architectural decision should prioritize:

- Maintainability
- Simplicity
- Modularity
- Reliability
- Extensibility

The objective is not merely to automate note-taking but to build a **personal AI learning platform** that evolves into a long-term educational companion.

---

**End of Document**
