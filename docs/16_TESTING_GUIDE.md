# AI Lecture Assistant

# Testing Guide

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
> Every feature must follow this testing guide before being considered complete.

---

# Purpose

This document defines the official testing strategy for the AI Lecture Assistant.

Goals:

- Prevent regressions
- Validate AI output
- Ensure reliability
- Verify automation
- Measure performance

Testing is a required part of development.

---

# Testing Philosophy

Every feature should be tested at multiple levels.

```
Unit Test

↓

Integration Test

↓

End-to-End Test

↓

Manual Validation
```

Never rely on only one testing method.

---

# Testing Pyramid

```
            E2E
           /   \
 Integration
     /       \
 Unit Tests
```

Most tests should be unit tests.

---

# Test Categories

The project contains:

- Unit Tests
- Integration Tests
- End-to-End Tests
- Performance Tests
- AI Output Tests
- Browser Automation Tests
- Database Tests
- API Tests
- Regression Tests
- Manual Tests

---

# Folder Structure

```
tests/

├── unit/
├── integration/
├── e2e/
├── performance/
├── ai/
├── browser/
├── api/
├── regression/
├── fixtures/
├── mocks/
└── data/
```

---

# Unit Testing

Purpose

Test one function or class in isolation.

Examples

- File utilities
- Storage manager
- Attendance parser
- Prompt builder
- Config loader

Requirements

- Fast
- Deterministic
- Independent
- No network

---

# Integration Testing

Purpose

Verify interaction between modules.

Examples

Meeting

↓

Transcript

↓

Notes

Database

↓

Repository

↓

Service

AI Router

↓

Provider

Requirements

- Real dependencies where appropriate
- Temporary database
- Controlled test environment

---

# End-to-End Testing

Purpose

Validate the complete workflow.

Example

```
Join Meeting

↓

Capture Audio

↓

Transcribe

↓

Generate Notes

↓

Generate PDF

↓

Save Files
```

Expected Result

Every step completes successfully.

---

# API Testing

Verify

- Status Codes
- Validation
- Error Handling
- Response Format
- Pagination
- Filtering

Every endpoint must have API tests.

---

# Database Testing

Verify

- Inserts
- Updates
- Deletes
- Foreign Keys
- Constraints
- Transactions
- Migrations

Never ship without database tests.

---

# Browser Automation Testing

Test

- Browser Launch
- Google Login (manual-assisted if needed)
- Meeting Join
- Leave Meeting
- Selector Stability
- Permission Handling

Use Playwright.

---

# Whisper Testing

Verify

- Audio loading
- Language detection
- Timestamp generation
- Segment creation
- CPU compatibility

Measure

- Accuracy
- Processing time

---

# Attendance Testing

Verify

- Name detection
- Duplicate prevention
- Timestamp accuracy
- Confidence threshold

Example

Input

```
Adithya Sai
```

Expected

Attendance event stored.

---

# LLM Router Testing

Verify

- Provider selection
- Retry logic
- Timeout handling
- Failover
- Normalization

Scenario

Primary provider fails.

Expected

Fallback provider responds.

---

# AI Output Testing

Verify generated

- Notes
- Summary
- Quiz
- Flashcards

Check

- Markdown validity
- Empty responses
- Required sections
- Formatting consistency

Do not compare exact wording.

Validate structure instead.

---

# PDF Testing

Verify

- PDF creation
- File size
- Fonts
- Images
- Markdown rendering
- Export speed

---

# Storage Testing

Verify

- Folder creation
- File writing
- File reading
- Cleanup
- Duplicate prevention

---

# Performance Testing

Measure

Meeting Join

Target

<15 seconds

Whisper

<5 seconds

Notes Generation

<20 seconds

Dashboard Load

<2 seconds

PDF Export

<10 seconds

---

# Stress Testing

Examples

- 5-hour lecture
- Very large transcript
- Repeated note generation
- Multiple AI retries
- Large PDF export

The application should fail gracefully if limits are exceeded.

---

# Regression Testing

Whenever a bug is fixed:

Add a regression test.

Bug

↓

Fix

↓

Regression Test

Never allow the same bug to return.

---

# Mocking Strategy

Mock

- AI providers
- External APIs
- Network failures
- Browser failures
- File errors

Do not mock core business logic.

---

# Test Data

Store reusable data in

```
tests/data/
```

Examples

- Sample audio
- Sample transcript
- Meeting metadata
- AI responses
- PDFs

Never duplicate test data.

---

# Test Fixtures

Store reusable fixtures in

```
tests/fixtures/
```

Examples

- Database session
- Meeting object
- Transcript object
- Mock provider

---

# Continuous Testing

Before every merge

Run

- Unit Tests
- Integration Tests
- API Tests

Nightly

Run

- Performance Tests
- End-to-End Tests

---

# Code Coverage

Minimum

```
80%
```

Target

```
90%
```

Critical modules

```
95%+
```

Critical modules include

- Meeting
- Whisper
- Storage
- LLM Router

Coverage alone is not sufficient.

Quality matters.

---

# Manual Testing Checklist

Verify

- Join Google Meet
- Leave Meeting
- Transcript accuracy
- Attendance detection
- Note quality
- Summary quality
- Quiz generation
- Flashcards
- PDF export
- Search

---

# Failure Testing

Verify behavior when

- AI provider is unavailable
- Network disconnects
- Audio device fails
- Disk is full
- Database is locked
- Invalid meeting URL
- Empty transcript

The application should recover whenever possible.

---

# AI Evaluation

AI-generated outputs should be evaluated using

- Completeness
- Correct structure
- Readability
- Missing sections
- Hallucination detection

Never assume AI output is always correct.

---

# Testing Rules

1. Every feature requires tests.
2. Every bug requires a regression test.
3. Never merge failing tests.
4. Prefer automated tests.
5. Keep tests deterministic.
6. Avoid flaky tests.
7. Use realistic test data.
8. Measure performance regularly.
9. Document known limitations.
10. Testing is part of the feature.

---

# Release Checklist

Before a release

- All tests pass
- Coverage threshold met
- Documentation updated
- Manual validation completed
- No critical bugs
- Performance targets achieved

---

# Summary

The AI Lecture Assistant follows a comprehensive testing strategy that combines unit, integration, end-to-end, AI validation, browser automation, and performance testing.

Every feature must be verified not only for correctness but also for reliability, maintainability, and long-term stability.
