# AI Lecture Assistant

# Database Design

> Version: 1.0.0
>
> Status: Active
>
> Priority: High
>
> Database: SQLite (MVP)
>
> ORM: SQLAlchemy
>
> Related Documents
>
> - 04_SYSTEM_ARCHITECTURE.md
> - 07_DATA_FLOW.md
> - 09_API_SPECIFICATION.md

---

# Purpose

This document defines the database architecture used by the AI Lecture Assistant.

The goals are:

- Store all lecture-related information
- Maintain data consistency
- Support future expansion
- Enable fast search
- Preserve historical data
- Keep schema simple for MVP

---

# Database Philosophy

The database follows these principles.

- Local-first
- Normalized schema
- One source of truth
- Immutable raw lecture artifacts
- Versioned AI outputs
- Easy migration

---

# Database Technology

Current

SQLite

Future

- PostgreSQL
- MySQL
- Cloud Database

The application must use SQLAlchemy so the underlying database can be replaced without changing business logic.

---

# High-Level ER Diagram

```
Meeting
   │
   ├──────── Transcript
   │
   ├──────── Attendance
   │
   ├──────── Notes
   │
   ├──────── Summary
   │
   ├──────── Quiz
   │
   ├──────── Flashcards
   │
   ├──────── PDF
   │
   └──────── Logs
```

---

# Tables

The MVP contains the following tables.

1. meetings

2. transcripts

3. transcript_segments

4. attendance_events

5. notes

6. summaries

7. quizzes

8. flashcards

9. generated_files

10. ai_requests

11. ai_responses

12. settings

13. processing_logs

---

# Table — meetings

Purpose

Stores one record for every lecture.

Columns

| Column | Type |
| --------- | ------ |
| id | UUID |
| title | TEXT |
| meet_url | TEXT |
| subject | TEXT |
| status | TEXT |
| started_at | DATETIME |
| ended_at | DATETIME |
| duration_seconds | INTEGER |
| created_at | DATETIME |
| updated_at | DATETIME |

Status

- Scheduled
- Joining
- Active
- Completed
- Failed

---

# Table — transcripts

Purpose

Stores the complete transcript.

Columns

| Column | Type |
| --------- | ------ |
| id | UUID |
| meeting_id | UUID |
| language | TEXT |
| transcript_text | LONGTEXT |
| word_count | INTEGER |
| created_at | DATETIME |

Relationship

Many transcripts belong to one meeting (future versioning).

---

# Table — transcript_segments

Purpose

Store timestamped transcript chunks.

Columns

| Column | Type |
| --------- | ------ |
| id | UUID |
| transcript_id | UUID |
| start_time | FLOAT |
| end_time | FLOAT |
| text | TEXT |

Benefits

- Search
- Timestamp navigation
- Future RAG
- Clip generation

---

# Table — attendance_events

Purpose

Store attendance detections.

Columns

| Column | Type |
| --------- | ------ |
| id | UUID |
| meeting_id | UUID |
| detected_name | TEXT |
| timestamp | FLOAT |
| confidence | FLOAT |
| status | TEXT |
| created_at | DATETIME |

---

# Table — notes

Purpose

Store AI-generated classroom notes.

Columns

| Column | Type |
| --------- | ------ |
| id | UUID |
| meeting_id | UUID |
| provider | TEXT |
| model | TEXT |
| markdown | LONGTEXT |
| version | INTEGER |
| created_at | DATETIME |

Versioning allows regenerated notes to coexist.

---

# Table — summaries

Purpose

Store lecture summaries.

Columns

| Column | Type |
| --------- | ------ |
| id | UUID |
| meeting_id | UUID |
| summary | LONGTEXT |
| provider | TEXT |
| model | TEXT |
| created_at | DATETIME |

---

# Table — quizzes

Purpose

Store generated quizzes.

Columns

| Column | Type |
| --------- | ------ |
| id | UUID |
| meeting_id | UUID |
| quiz_markdown | LONGTEXT |
| difficulty | TEXT |
| provider | TEXT |
| created_at | DATETIME |

---

# Table — flashcards

Purpose

Store generated flashcards.

Columns

| Column | Type |
| --------- | ------ |
| id | UUID |
| meeting_id | UUID |
| question | TEXT |
| answer | TEXT |
| topic | TEXT |

---

# Table — generated_files

Purpose

Track exported files.

Columns

| Column | Type |
| --------- | ------ |
| id | UUID |
| meeting_id | UUID |
| file_type | TEXT |
| file_path | TEXT |
| file_size | INTEGER |
| checksum | TEXT |
| created_at | DATETIME |

Types

- PDF
- Markdown
- Audio
- JSON

---

# Table — ai_requests

Purpose

Track every request sent to an LLM.

Columns

| Column | Type |
| --------- | ------ |
| id | UUID |
| meeting_id | UUID |
| provider | TEXT |
| model | TEXT |
| prompt_type | TEXT |
| tokens_input | INTEGER |
| tokens_output | INTEGER |
| latency_ms | INTEGER |
| cost | REAL |
| status | TEXT |
| created_at | DATETIME |

---

# Table — ai_responses

Purpose

Store raw AI responses.

Columns

| Column | Type |
| --------- | ------ |
| id | UUID |
| request_id | UUID |
| response | LONGTEXT |
| normalized | LONGTEXT |
| created_at | DATETIME |

---

# Table — settings

Purpose

Application configuration.

Examples

- Default Provider
- Whisper Model
- Theme
- Language
- Auto Join
- Auto Export PDF

---

# Table — processing_logs

Purpose

Store processing history.

Columns

| Column | Type |
| --------- | ------ |
| id | UUID |
| meeting_id | UUID |
| module | TEXT |
| level | TEXT |
| message | TEXT |
| created_at | DATETIME |

---

# Relationships

```
Meeting

├── Transcript

│      └── Transcript Segments

├── Attendance

├── Notes

├── Summary

├── Quiz

├── Flashcards

├── Generated Files

├── AI Requests

│      └── AI Responses

└── Logs
```

---

# Indexing Strategy

Indexes should exist on:

meetings

- created_at
- status

transcripts

- meeting_id

notes

- meeting_id

attendance

- meeting_id

logs

- meeting_id

These indexes optimize dashboard loading and lecture history queries.

---

# Storage Strategy

Database stores metadata.

Large files remain on disk.

Example

```
Database

meeting_id

↓

File Path

↓

storage/

↓

meeting_xxx/

↓

notes.md
```

This keeps the database lightweight.

---

# File Structure

```
storage/

meeting_uuid/

    audio/

    transcript/

    notes/

    summary/

    quiz/

    flashcards/

    pdf/

    metadata.json
```

---

# Data Integrity Rules

- Every meeting has a unique ID.
- Every transcript belongs to one meeting.
- Every note belongs to one meeting.
- Every summary belongs to one meeting.
- Every AI request is traceable.
- Raw transcript is never deleted automatically.

---

# Migration Strategy

Migration Tool

Alembic

Every schema modification must:

- Create migration
- Update documentation
- Preserve existing data

---

# Backup Strategy

Automatic backups are optional.

Suggested schedule

- Daily
- Before migrations
- Before major upgrades

Backups include:

- SQLite database
- Storage directory
- Configuration

---

# Future Database Extensions

Planned additions

- User table
- Subjects
- Courses
- Semester
- Tags
- Embeddings
- Vector database
- Learning analytics
- Revision history
- Plugin metadata

The current schema should allow these additions without redesign.

---

# Design Rules

1. Metadata in database.
2. Large files on disk.
3. Never duplicate data.
4. Every table has timestamps.
5. Every record has a UUID.
6. Keep schema normalized.
7. Preserve raw artifacts.
8. Version AI-generated content.
9. Use foreign keys where applicable.
10. Document every schema change.

---

# Summary

The AI Lecture Assistant uses a lightweight, normalized SQLite database to manage lecture metadata, AI-generated content, attendance events, and processing history.

The database is designed to support the MVP while remaining extensible for future features such as semantic search, RAG, analytics, and multi-user support.
