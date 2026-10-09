# AI Lecture Assistant

# 01 - Project Overview

> Version: 1.0.0
>
> Status: Draft
>
> Last Updated: YYYY-MM-DD

---

# Purpose

This document provides a high-level overview of the AI Lecture Assistant.

It explains:

- What the application does
- Who it is designed for
- The major workflows
- The core modules
- User interactions
- Project boundaries

This document intentionally avoids implementation details.

For architecture, refer to:

- 04_SYSTEM_ARCHITECTURE.md
- 05_AI_AGENT_ARCHITECTURE.md
- 07_DATA_FLOW.md

---

# Product Description

AI Lecture Assistant is a personal AI system that automatically attends online lectures, captures lecture audio, converts speech into text, generates structured classroom notes, detects attendance calls, and builds a searchable archive of lecture knowledge.

The system is designed to remove the burden of manual note-taking while improving revision and long-term knowledge retention.

The assistant acts as a digital learning companion rather than a meeting recorder.

---

# Primary Users

Current Target

- Individual students
- Personal use
- Windows laptop

Future Target

- Universities
- Teachers
- Research groups
- Educational organizations

---

# Problems Being Solved

Students commonly experience the following during online lectures:

- Missing important explanations while taking notes.
- Difficulty listening and writing simultaneously.
- Losing track of assignments.
- Forgetting formulas and definitions.
- Poor revision material before examinations.
- Missing attendance calls.
- Spending hours organizing notes after class.

The AI Lecture Assistant automates these tasks.

---

# Product Goals

The application should:

- Join Google Meet automatically.
- Capture lecture audio.
- Produce high-quality transcripts.
- Detect attendance calls.
- Generate organized classroom notes.
- Create summaries.
- Store lecture history.
- Enable searching previous lectures.
- Export notes into PDF.

---

# Product Scope

The first version focuses only on Google Meet lectures.

Included:

- Google Meet
- Audio transcription
- AI note generation
- Attendance detection
- PDF export
- Local storage

Not Included:

- Zoom
- Microsoft Teams
- Cloud synchronization
- Mobile application
- Multi-user collaboration

---

# User Journey

A typical workflow looks like this.

```
User

↓

Paste Google Meet Link

↓

Click Join

↓

Meeting Agent joins lecture

↓

Audio is captured

↓

Whisper generates transcript

↓

Attendance detection runs

↓

Transcript is stored

↓

LLM generates notes

↓

Summary is generated

↓

PDF is created

↓

Everything is saved
```

The user only interacts at the beginning and after the lecture.

---

# Major Capabilities

## 1. Meeting Automation

Responsible for:

- Joining meetings
- Leaving meetings
- Managing browser automation

---

## 2. Audio Processing

Responsible for:

- Capturing meeting audio
- Streaming audio
- Saving recordings

---

## 3. Speech Recognition

Responsible for:

- Converting speech into text
- Timestamp generation
- Transcript creation

---

## 4. Attendance Detection

Responsible for:

- Monitoring transcripts
- Detecting attendance calls
- Recording attendance events

---

## 5. AI Processing

Responsible for:

- Cleaning transcripts
- Summarizing lectures
- Creating classroom notes
- Extracting definitions
- Creating quizzes
- Generating flashcards

---

## 6. Storage

Responsible for:

- Saving transcripts
- Saving notes
- Saving PDFs
- Saving metadata

---

## 7. Search

Responsible for:

- Finding previous lectures
- Searching notes
- Searching transcripts

---

# Functional Workflow

```
Google Meet

↓

Meeting Agent

↓

Audio Capture

↓

Speech Recognition

↓

Transcript

↓

Attendance Detection

↓

LLM Processing

↓

Notes

↓

Storage

↓

Dashboard
```

---

# Core Modules

| Module | Responsibility |
| ---------- | --------------- |
| Meeting Agent | Join and leave meetings |
| Audio Module | Capture lecture audio |
| Whisper Module | Speech-to-text |
| Attendance Module | Detect attendance calls |
| LLM Router | Select AI provider |
| Notes Agent | Generate notes |
| Summary Agent | Create summaries |
| Storage Manager | Save project data |
| Search Module | Search historical lectures |
| Dashboard | User interface |

---

# Inputs

The system receives:

- Google Meet URL
- User configuration
- Audio stream
- AI model configuration

---

# Outputs

The system produces:

- Transcript
- Summary
- Classroom Notes
- PDF
- Quiz
- Flashcards
- Attendance Log
- Meeting Metadata

---

# Success Criteria

The application is successful if it can consistently:

- Join meetings automatically.
- Produce accurate transcripts.
- Detect attendance events.
- Generate useful notes.
- Save all lecture data.
- Allow future search and revision.

---

# Assumptions

The project assumes:

- Stable internet connection.
- Valid Google account.
- Chrome installed.
- Whisper model available.
- AI API keys configured.
- User has permission to join the meeting.

---

# Constraints

The project currently supports:

- Windows operating system.
- Single-user environment.
- Local execution.
- Google Meet only.

---

# Out of Scope

The following are intentionally excluded from Version 1:

- Video recording
- Face recognition
- Automatic speaker identification
- Mobile application
- Cloud synchronization
- LMS integration
- Real-time collaboration

---

# Related Documents

Read next:

- 02_PRODUCT_VISION.md
- 03_SRS.md
- 04_SYSTEM_ARCHITECTURE.md

---

# Summary

AI Lecture Assistant is a local-first, AI-powered learning assistant focused on automating lecture attendance, note generation, and knowledge management.

It combines browser automation, speech recognition, multiple LLMs, and structured storage into a single application that helps students spend less time taking notes and more time learning.
