# AI Lecture Assistant

# AI Agent Architecture

> Version: 1.0.0
>
> Status: Active
>
> Priority: Critical
>
> Related Documents
>
> - 04_SYSTEM_ARCHITECTURE.md
> - 06_LLM_ROUTER.md
> - 07_DATA_FLOW.md

---

# Purpose

This document defines every AI agent used in the AI Lecture Assistant.

It specifies:

- Agent responsibilities
- Agent ownership
- Agent communication
- Agent lifecycle
- Inputs
- Outputs
- Internal rules
- Future extensibility

Every AI coding agent should understand this document before implementing any module.

---

# What is an Agent?

An agent is an independent software component responsible for performing one well-defined task.

An agent:

- owns its own logic
- owns its own state
- performs one responsibility
- communicates through interfaces
- never directly manipulates another agent

---

# Design Philosophy

The project follows these principles.

## Single Responsibility

One agent.

One responsibility.

Example

Meeting Agent

Only manages meetings.

Never generates notes.

---

## Independent

Agents should be replaceable.

Meeting Agent Version 2

should not affect

Notes Agent.

---

## Stateless by Default

Agents should avoid storing long-term state.

Persistent information belongs inside Storage Manager.

---

## Observable

Every action must be logged.

Example

Meeting Joined

↓

Audio Started

↓

Transcript Generated

↓

Notes Generated

---

## Recoverable

If one agent crashes,

other agents continue working whenever possible.

---

# High-Level Agent Architecture

```
                    AI Lecture Assistant

                             │

                    Agent Orchestrator

                             │

 ───────────────────────────────────────────────────

        │

        ├──────── Meeting Agent

        ├──────── Audio Agent

        ├──────── Whisper Agent

        ├──────── Attendance Agent

        ├──────── Storage Agent

        ├──────── Search Agent

        ├──────── LLM Router

        ├──────── Notes Agent

        ├──────── Summary Agent

        ├──────── Quiz Agent

        ├──────── Flashcard Agent

        ├──────── PDF Agent

        └──────── Notification Agent
```

---

# Agent Orchestrator

The Agent Orchestrator controls the entire application.

Responsibilities

- start agents
- stop agents
- restart failed agents
- manage dependencies
- monitor health
- coordinate workflows

The orchestrator contains no business logic.

It only coordinates.

---

# Meeting Agent

Purpose

Manage Google Meet sessions.

Responsibilities

- launch browser
- join meeting
- leave meeting
- detect meeting end
- mute microphone
- disable camera

Input

Google Meet URL

Output

Meeting Session

Dependencies

Playwright

Owns

Meeting lifecycle only.

---

# Audio Agent

Purpose

Capture meeting audio.

Responsibilities

- record audio
- stream audio
- save raw audio
- buffer audio

Input

Meeting Session

Output

Audio Stream

Owns

Audio pipeline.

---

# Whisper Agent

Purpose

Convert speech into text.

Responsibilities

- speech recognition
- timestamps
- transcript generation
- transcript chunks

Input

Audio Stream

Output

Transcript

Dependencies

faster-whisper

Never

Generate summaries.

---

# Attendance Agent

Purpose

Detect attendance.

Responsibilities

- monitor transcript
- detect user name
- record attendance event
- notify user

Input

Transcript

Output

Attendance Event

Uses

Simple matching.

No LLM required.

---

# Storage Agent

Purpose

Store all project data.

Responsibilities

- save transcript
- save notes
- save metadata
- save PDFs
- save audio
- load previous meetings

Never

Generate data.

---

# Search Agent

Purpose

Search stored knowledge.

Responsibilities

- keyword search
- transcript search
- meeting search
- note search

Future

Semantic search.

---

# LLM Router

Purpose

Select the correct AI model.

Responsibilities

- provider selection
- retries
- failover
- model configuration

Input

AI Request

Output

LLM Response

Never

Generate prompts.

---

# Notes Agent

Purpose

Generate classroom notes.

Responsibilities

- clean transcript
- organize notes
- create headings
- extract concepts
- extract examples

Input

Transcript

Output

Notes

---

# Summary Agent

Purpose

Generate lecture summary.

Responsibilities

- short summary
- detailed summary
- key points

Independent from Notes Agent.

---

# Quiz Agent

Purpose

Generate revision questions.

Output

- MCQs
- Short Questions
- Long Questions

---

# Flashcard Agent

Purpose

Generate flashcards.

Output

Question

↓

Answer

Supports future Anki export.

---

# PDF Agent

Purpose

Generate professional PDFs.

Input

Notes

Summary

Output

Lecture PDF

---

# Notification Agent

Purpose

Notify the user.

Examples

Meeting Joined

Attendance Called

Meeting Finished

Notes Ready

---

# Agent Lifecycle

Every agent follows the same lifecycle.

```
Created

↓

Initialized

↓

Ready

↓

Running

↓

Completed

↓

Stopped
```

If an error occurs

```
Running

↓

Failed

↓

Retry

↓

Recovered

or

Stopped
```

---

# Agent Communication

Agents never call each other directly.

Instead

```
Meeting Agent

↓

Event

↓

Audio Agent

↓

Event

↓

Whisper Agent

↓

Event

↓

Notes Agent
```

The orchestrator manages the sequence.

---

# Shared Data

Agents share only structured data.

Examples

Transcript

Meeting Metadata

Attendance Event

Summary

Notes

Audio Path

Never share internal variables.

---

# Agent Interfaces

Every agent exposes a consistent interface.

Example

initialize()

start()

stop()

status()

health()

reset()

Every new agent should follow the same interface.

---

# Failure Recovery

Example

Whisper crashes.

Meeting Agent

continues recording.

Storage Agent

continues saving.

Orchestrator

restarts Whisper.

The meeting should not terminate because one agent fails.

---

# Logging

Every agent must log:

- startup
- shutdown
- errors
- warnings
- processing time
- important events

---

# Performance Goals

Meeting Agent

Join

<15 sec

Whisper

Latency

<5 sec

Attendance

Detection

<2 sec

Notes

Generation

<20 sec

---

# Future Agents

Possible future additions

Slide OCR Agent

Calendar Agent

Assignment Agent

Revision Planner

Learning Analytics Agent

Voice Assistant

Knowledge Graph Agent

Study Planner

RAG Agent

Email Agent

Plugin Agent

The architecture should support adding these without modifying existing agents.

---

# Agent Dependency Graph

```
Meeting Agent

↓

Audio Agent

↓

Whisper Agent

↓

Transcript

↓

Attendance Agent

↓

LLM Router

↓

Notes Agent

↓

Summary Agent

↓

Quiz Agent

↓

Flashcard Agent

↓

PDF Agent

↓

Storage Agent

↓

Search Agent
```

---

# Agent Ownership

| Agent | Owns |
| -------- | ------ |
| Meeting | Meeting lifecycle |
| Audio | Audio capture |
| Whisper | Speech recognition |
| Attendance | Attendance detection |
| Router | AI provider selection |
| Notes | Classroom notes |
| Summary | Lecture summary |
| Quiz | Revision questions |
| Flashcard | Flashcards |
| PDF | PDF export |
| Storage | Persistence |
| Search | Retrieval |
| Notification | User notifications |

---

# Design Rules

Every agent must follow these rules.

1. One responsibility.

2. No shared mutable state.

3. No business logic outside ownership.

4. Every action logged.

5. Easy to replace.

6. Easy to test.

7. Independent failures.

8. Interface driven.

9. Minimal dependencies.

10. Documentation updated before behavior changes.

---

# Summary

The AI Lecture Assistant follows a multi-agent architecture coordinated by a central Agent Orchestrator.

Each agent owns one responsibility, communicates through structured interfaces, and can evolve independently.

This design allows the project to remain modular, maintainable, and ready for future AI capabilities while keeping the MVP simple and reliable.
