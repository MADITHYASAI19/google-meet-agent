# AI Lecture Assistant

# LLM Router Architecture

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
> - 07_DATA_FLOW.md

---

# Purpose

The LLM Router is responsible for managing all interactions with Large Language Models (LLMs).

No module in the system should communicate directly with an AI provider.

Instead, every AI request must go through the LLM Router.

This provides:

- Provider independence
- Better maintainability
- Automatic failover
- Unified interface
- Future scalability

---

# Objectives

The router must:

- Support multiple AI providers.
- Route requests intelligently.
- Retry failed requests.
- Handle provider failures.
- Normalize responses.
- Log every request.
- Be easily extensible.

---

# Supported Providers

Current

- OpenAI
- Grok
- Gemini

Future

- Claude
- DeepSeek
- Ollama
- LM Studio
- Local LLMs

---

# High-Level Architecture

```
                  AI Agent

                     │

                     ▼

              LLM Router API

                     │

        ┌────────────┼────────────┐

        ▼            ▼            ▼

     OpenAI        Grok        Gemini

        ▼            ▼            ▼

      Response Normalizer

               │

               ▼

         Standard Response

               │

               ▼

             AI Agent
```

---

# Why a Router?

Without Router

```
Notes Agent

↓

OpenAI
```

Summary Agent

↓

Gemini

Quiz Agent

↓

Grok

Every module knows every provider.

This becomes difficult to maintain.

---

With Router

```
Notes Agent

↓

LLM Router

↓

Provider

↓

Result
```

Every agent only knows one interface.

---

# Responsibilities

The router is responsible for:

- Selecting provider
- Selecting model
- Retry handling
- Timeout handling
- Failover
- Response normalization
- Cost tracking
- Usage logging

---

# Responsibilities NOT Included

The router does NOT:

- Generate prompts
- Modify prompts
- Store notes
- Save transcripts
- Generate PDFs
- Manage meetings

---

# Routing Flow

```
Notes Agent

↓

Create AI Request

↓

LLM Router

↓

Choose Provider

↓

Execute Request

↓

Normalize Response

↓

Return Result
```

---

# Request Format

Every request should contain:

- Request ID
- Agent Name
- Prompt
- Context
- Preferred Provider
- Preferred Model
- Temperature
- Max Tokens

Example

```
{
    request_id,
    agent,
    prompt,
    context,
    provider,
    model
}
```

---

# Response Format

Every provider returns different formats.

The router converts them into one standard structure.

Example

```
{
    success,
    provider,
    model,
    response,
    latency,
    token_usage,
    error
}
```

Every AI agent receives the same response format.

---

# Provider Selection

Possible strategies:

## Manual

Always use selected provider.

Example

OpenAI

---

## Automatic

Router selects the best provider.

Based on:

- Availability
- Speed
- Cost
- Success Rate

---

## Hybrid

Preferred provider first.

Fallback providers if needed.

---

# Failover Strategy

Example

```
OpenAI

↓

Failure

↓

Retry

↓

Failure

↓

Switch

↓

Grok

↓

Success
```

No AI agent should know this happened.

---

# Retry Policy

Maximum Retries

3

Delay

Exponential Backoff

Example

Attempt 1

↓

1 second

↓

Attempt 2

↓

2 seconds

↓

Attempt 3

↓

4 seconds

---

# Timeouts

Every request should have a timeout.

Example

30 seconds

After timeout

↓

Retry

↓

Fallback

---

# Response Normalization

Different providers return different schemas.

The router converts them into one structure.

This prevents provider-specific logic from leaking into AI agents.

---

# Logging

Every request should log:

- Request ID
- Provider
- Model
- Start Time
- End Time
- Latency
- Tokens Used
- Success/Failure
- Error

---

# Cost Tracking

Track:

- Prompt Tokens
- Completion Tokens
- Total Tokens
- Estimated Cost

Useful for future analytics.

---

# Performance Metrics

Track:

Average Latency

Success Rate

Failure Rate

Provider Usage

Retry Count

Average Cost

---

# Configuration

Configuration should come from environment variables.

Example

```
DEFAULT_PROVIDER

DEFAULT_MODEL

MAX_RETRIES

TIMEOUT

ENABLE_FAILOVER
```

No hardcoded API keys.

---

# Error Handling

Possible Errors

- API Timeout
- Invalid Key
- Rate Limit
- Network Failure
- Provider Down
- Invalid Model

Every error should be standardized.

---

# Future Enhancements

The router should support:

- Load Balancing
- Cost-Based Routing
- Latency-Based Routing
- Confidence-Based Routing
- Multi-Provider Voting
- Local LLM Routing
- Streaming Responses

---

# Example Workflow

```
Transcript

↓

Notes Agent

↓

LLM Router

↓

OpenAI

↓

Normalized Response

↓

Notes Agent

↓

Markdown Notes

↓

Storage
```

---

# Design Rules

1. No direct provider calls.

2. One router for all AI requests.

3. Providers are interchangeable.

4. Responses are normalized.

5. Every request is logged.

6. Retry before failover.

7. Configuration via environment variables.

8. Easy to add new providers.

9. Provider SDKs remain isolated.

10. Router should never generate prompts.

---

# Summary

The LLM Router is the central gateway between the application and all AI providers.

It abstracts provider-specific implementations, improves reliability, enables failover, standardizes responses, and prepares the project for future expansion with additional cloud or local language models.

Every AI-powered feature in the project must communicate through the LLM Router.
