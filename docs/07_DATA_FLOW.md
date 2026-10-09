# AI Lecture Assistant

# Data Flow

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

This document describes the complete movement of data throughout the AI Lecture Assistant.

It explains:

- How data enters the system
- How it is transformed
- Which modules process it
- Where it is stored
- What outputs are generated

This document is intended to help developers understand the end-to-end lifecycle of every lecture.

---

# Data Flow Principles

The system follows these principles.

- Data flows in one direction.
- Modules never modify another module's internal state.
- Every transformation is logged.
- Raw data is preserved.
- Processed data is versioned.
- Failures do not destroy existing data.

---

# High-Level Data Flow

```
Google Meet Link
        │
        ▼
Meeting Agent
        │
        ▼
Meeting Session
        │
        ▼
Audio Capture
        │
        ▼
Raw Audio (.wav)
        │
        ▼
Whisper Agent
        │
        ▼
Transcript
        │
        ├──────────────┐
        ▼              ▼
Attendance Agent   Storage Agent
        │
        ▼
Attendance Events
        │
        ▼
LLM Router
        │
        ▼
Notes Agent
        │
        ├──────────────┬───────────────┐
        ▼              ▼               ▼
Summary         Quiz Generator     Flashcards
        │
        ▼
PDF Generator
        │
        ▼
Storage
        │
        ▼
Dashboard
```

---

# Stage 1 — User Input

Input

- Google Meet URL

Optional

- Meeting Name
- Subject
- AI Provider
- Preferred Language

Output

Meeting Request

---

# Stage 2 — Meeting Agent

Receives

Meeting Request

Responsibilities

- Validate URL
- Launch browser
- Login if required
- Join meeting
- Detect successful connection

Output

Meeting Session

Stored

Meeting Metadata

---

# Stage 3 — Audio Capture

Receives

Meeting Session

Responsibilities

- Capture audio
- Buffer stream
- Save recording

Output

Raw Audio File

Example

```
lecture.wav
```

Stored

storage/audio/

---

# Stage 4 — Whisper Agent

Receives

Audio File

Responsibilities

- Speech Recognition
- Timestamp generation
- Segment creation

Output

Transcript

Example

```
00:00:02

Good morning everyone.

00:00:07

Today we will study Binary Trees.
```

Stored

storage/transcripts/

---

# Stage 5 — Attendance Detection

Receives

Transcript Stream

Responsibilities

- Detect student name
- Detect attendance phrases
- Record timestamps

Output

Attendance Event

Example

```
{
  student:"Adithya",
  timestamp:"00:18:12",
  status:"Detected"
}
```

Stored

attendance table

---

# Stage 6 — Storage

The Storage Agent stores every intermediate artifact.

Artifacts

- Meeting Metadata
- Raw Audio
- Transcript
- Attendance
- Processing Logs

Storage occurs before AI processing to ensure no information is lost.

---

# Stage 7 — LLM Processing

Receives

Transcript

Creates AI Request

Routes request to

LLM Router

Router selects provider.

Example

OpenAI

↓

Response

↓

Notes Agent

---

# Stage 8 — Notes Generation

Receives

Transcript

Produces

- Clean Notes
- Topics
- Definitions
- Examples
- Homework
- Assignments

Output

Markdown Notes

Stored

storage/notes/

---

# Stage 9 — Summary Generation

Receives

Transcript

Produces

- Short Summary
- Detailed Summary
- Key Takeaways

Stored

storage/summaries/

---

# Stage 10 — Quiz Generation

Receives

Transcript

Produces

- MCQs
- Short Questions
- Long Questions

Stored

storage/quizzes/

---

# Stage 11 — Flashcard Generation

Receives

Transcript

Produces

Question

↓

Answer

Pairs

Stored

storage/flashcards/

---

# Stage 12 — PDF Generation

Receives

- Notes
- Summary
- Quiz

Produces

Professional PDF

Stored

storage/pdf/

---

# Stage 13 — Dashboard

Dashboard loads

- Meeting History
- Notes
- PDFs
- Search
- Attendance
- Statistics

---

# Storage Flow

```
Meeting

↓

Audio

↓

Transcript

↓

Notes

↓

Summary

↓

Quiz

↓

Flashcards

↓

PDF
```

Nothing is deleted automatically.

---

# Data Persistence

Every lecture receives a unique folder.

Example

```
storage/

meeting_2026_10_01/

    audio/

    transcript/

    notes/

    summary/

    pdf/

    logs/

    metadata.json
```

This keeps all artifacts for a lecture together.

---

# Data Lifecycle

```
Created

↓

Validated

↓

Processed

↓

Stored

↓

Indexed

↓

Available for Search

↓

Archived
```

No stage should overwrite raw input.

---

# Error Flow

Example

Whisper Failure

```
Audio Saved

↓

Whisper Error

↓

Retry

↓

Success
```

Example

LLM Failure

```
Transcript Ready

↓

OpenAI Failed

↓

Router Retry

↓

Switch to Grok

↓

Generate Notes
```

Data already produced must remain intact.

---

# Event Flow

Every major stage emits an event.

Examples

```
MeetingJoined

AudioStarted

AudioSaved

TranscriptGenerated

AttendanceDetected

NotesGenerated

SummaryGenerated

PDFCreated

ProcessingCompleted
```

Future agents can subscribe to these events without modifying existing modules.

---

# Logging Flow

Each stage logs

- Start Time
- End Time
- Duration
- Status
- Errors
- Warnings

Logs are stored separately from lecture data.

---

# Performance Targets

Meeting Join

< 15 sec

Audio Capture

Real Time

Whisper Delay

< 5 sec

Attendance Detection

< 2 sec

Notes Generation

< 20 sec

Dashboard Loading

< 2 sec

---

# Future Data Flow

Future versions may introduce

```
Transcript

↓

Embedding Generator

↓

Vector Database

↓

RAG Engine

↓

Chat Assistant

↓

Student Questions

↓

AI Answers
```

The current pipeline should allow these additions without redesigning earlier stages.

---

# Design Rules

1. Data always flows forward.
2. Preserve raw inputs.
3. Never overwrite transcripts.
4. Every transformation is logged.
5. Every output is stored.
6. AI processing never destroys source data.
7. Each module processes only its own input.
8. Events are preferred over direct module coupling.
9. Every stage should be restartable.
10. Every artifact should be traceable to its originating meeting.

---

# Summary

The AI Lecture Assistant follows a linear, event-driven data pipeline where each module performs a single transformation before passing structured output to the next stage.

This architecture ensures reliability, traceability, maintainability, and prepares the system for future features such as semantic search, RAG, and AI-powered study assistance.
