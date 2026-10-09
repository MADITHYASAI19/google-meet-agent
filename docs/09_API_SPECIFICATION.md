# AI Lecture Assistant

# API Specification

> Version: 1.0.0
>
> Status: Active
>
> API Style: REST
>
> Backend: FastAPI
>
> Base URL: /api/v1
>
> Response Format: JSON

---

# Purpose

This document defines every public API exposed by the backend.

It includes:

- Endpoints
- Request format
- Response format
- Status codes
- Error responses
- Versioning strategy
- Future APIs

The API should remain stable.

Breaking changes require a new API version.

---

# API Design Principles

The API follows these principles.

- RESTful
- Predictable
- Versioned
- Stateless
- Consistent
- JSON only
- Proper HTTP Status Codes
- Strong validation

---

# Base URL

```
/api/v1
```

Future

```
/api/v2
```

---

# Response Format

Every endpoint returns the same structure.

Success

```json
{
    "success": true,
    "message": "Operation completed.",
    "data": {},
    "timestamp": "2026-10-01T10:00:00Z"
}
```

Failure

```json
{
    "success": false,
    "error": {
        "code": "MEETING_NOT_FOUND",
        "message": "Meeting does not exist."
    },
    "timestamp": "2026-10-01T10:00:00Z"
}
```

---

# Status Codes

|Code|Meaning|
|-------|----------|
|200|Success|
|201|Created|
|202|Accepted|
|204|No Content|
|400|Bad Request|
|401|Unauthorized|
|403|Forbidden|
|404|Not Found|
|409|Conflict|
|422|Validation Error|
|429|Rate Limited|
|500|Internal Server Error|

---

# API Modules

The API is divided into modules.

```
Meeting API

Audio API

Transcript API

Attendance API

Notes API

Summary API

Quiz API

Flashcards API

Search API

PDF API

Settings API

Health API
```

---

# Meeting API

## Create Meeting Session

POST

```
/meetings
```

Purpose

Start a new meeting workflow.

Request

```json
{
    "meet_url":"...",
    "title":"DBMS Lecture",
    "subject":"Database"
}
```

Response

```json
{
    "meeting_id":"uuid",
    "status":"created"
}
```

---

## Join Meeting

POST

```
/meetings/{id}/join
```

Starts browser automation.

---

## Leave Meeting

POST

```
/meetings/{id}/leave
```

Leaves meeting safely.

---

## Get Meeting

GET

```
/meetings/{id}
```

Returns

- Metadata
- Status
- Duration

---

## List Meetings

GET

```
/meetings
```

Supports

- Pagination
- Search
- Date filter
- Subject filter

---

# Transcript API

## Get Transcript

GET

```
/transcripts/{meeting_id}
```

Returns

Complete transcript.

---

## Transcript Segments

GET

```
/transcripts/{meeting_id}/segments
```

Returns timestamped transcript.

---

# Attendance API

## Attendance Events

GET

```
/attendance/{meeting_id}
```

Returns

Attendance detections.

---

# Notes API

## Generate Notes

POST

```
/notes/generate
```

Input

Meeting ID

Output

Generated notes.

---

## Get Notes

GET

```
/notes/{meeting_id}
```

---

## Regenerate Notes

POST

```
/notes/{meeting_id}/regenerate
```

Allows another AI model.

---

# Summary API

Generate

```
POST /summary/generate
```

Retrieve

```
GET /summary/{meeting_id}
```

---

# Quiz API

Generate

```
POST /quiz/generate
```

Retrieve

```
GET /quiz/{meeting_id}
```

---

# Flashcards API

Generate

```
POST /flashcards/generate
```

Retrieve

```
GET /flashcards/{meeting_id}
```

---

# Search API

Global Search

```
GET /search
```

Query Parameters

```
keyword

subject

date

provider

meeting
```

Returns

Relevant lectures.

---

# PDF API

Generate PDF

```
POST /pdf/generate
```

Download PDF

```
GET /pdf/{meeting_id}
```

---

# Settings API

Get Settings

```
GET /settings
```

Update Settings

```
PUT /settings
```

Possible Settings

- AI Provider
- Whisper Model
- Theme
- Auto Join
- Auto Export

---

# Health API

Health Check

```
GET /health
```

Returns

- Database
- Whisper
- AI Providers
- Storage
- Overall Status

---

# Future APIs

Future endpoints

```
/chat

/rag

/analytics

/calendar

/plugins

/slides

/vector-search
```

---

# WebSocket API

Future

```
/ws
```

Events

Meeting Started

Transcript Updated

Attendance Detected

Notes Ready

Summary Ready

PDF Generated

Meeting Finished

---

# API Versioning

Current

```
v1
```

Future

```
v2
```

Breaking changes require

New version.

---

# Authentication

MVP

No authentication.

Future

JWT

OAuth

Google Login

API Keys

---

# Pagination

List endpoints should support

```
?page=1

?page_size=20
```

---

# Filtering

Example

```
GET

/meetings

?subject=AIML

&status=completed

&date=2026-10-01
```

---

# Sorting

```
sort=created_at

order=desc
```

---

# Error Codes

Examples

```
MEETING_NOT_FOUND

INVALID_URL

WHISPER_FAILED

AI_PROVIDER_DOWN

TRANSCRIPT_NOT_FOUND

PDF_GENERATION_FAILED

DATABASE_ERROR

VALIDATION_ERROR
```

---

# Validation Rules

Validate

- UUID
- URL
- Empty strings
- Invalid providers
- Invalid models
- Required fields

Never trust client input.

---

# Rate Limiting

Future

Default

100 requests/minute

---

# Logging

Every request logs

- Request ID
- Endpoint
- Duration
- Status
- Client
- Errors

---

# Security

- HTTPS (Future)
- Input validation
- Output sanitization
- Secure headers
- API key protection

---

# Design Rules

1. REST only.
2. JSON only.
3. Version every endpoint.
4. Never expose database models.
5. Validate every request.
6. Return meaningful errors.
7. Log every request.
8. Consistent response format.
9. Backward compatibility.
10. Documentation first.

---

# Summary

The API provides a stable, versioned interface between the frontend, backend, and future integrations.

All application functionality is exposed through well-defined REST endpoints that prioritize consistency, maintainability, and future scalability.
