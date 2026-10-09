# CLAUDE.md

## Project Overview
The **AI Lecture Assistant** is a personal AI-powered system designed for students to automatically attend Google Meet lectures, capture audio, transcribe speech, detect attendance, and generate structured study materials (notes, summaries, quizzes, flashcards). It transforms online lectures into a searchable personal knowledge base.

## Architecture Overview
- **Style**: Modular Monolith.
- **Backend**: FastAPI (Python 3.12+).
- **Frontend**: Next.js (TypeScript).
- **Database**: SQLite with SQLAlchemy ORM.
- **Browser Automation**: Playwright (Chromium).
- **Speech-to-Text**: faster-whisper.
- **AI Orchestration**: Centralized LLM Router for multi-provider support (OpenAI, Grok, Gemini).
- **Communication**: Event-driven asynchronous communication between modules using a central `EventDispatcher`.

## Repository Structure
- `backend/`: FastAPI application.
    - `app/`: Source code.
        - `api/`: REST endpoints.
        - `agents/`: Autonomous AI agents.
        - `services/`: Business logic.
        - `database/`: Persistence setup.
        - `models/`: SQLAlchemy ORM models.
        - `schemas/`: Pydantic validation models.
        - `core/`: Application core (event dispatcher, etc.).
        - `config/`: Settings and logging.
- `frontend/`: Next.js application.
- `docs/`: Complete project documentation (Source of Truth).
- `storage/`: Local storage for audio, transcripts, and notes.
- `prompts/`: LLM prompt templates.
- `tests/`: Unit, integration, and E2E tests.
- `scripts/`: Utility scripts.

## Coding Standards
- **Naming**: 
    - Files/Functions/Variables: `snake_case`
    - Classes: `PascalCase`
    - Constants: `UPPER_CASE`
- **Type Safety**: Mandatory type hints for all function signatures.
- **Documentation**: Docstrings for all public classes and functions.
- **Modularity**: 
    - Single Responsibility Principle (SRP).
    - Thin API routes $\rightarrow$ Service layer $\rightarrow$ Repository layer $\rightarrow$ Database.
    - No business logic in API routes or Repositories.
- **AI Guidelines**: 
    - No hardcoded API keys or paths.
    - Use the LLM Router for all AI requests.
    - Event-driven communication between agents.

## Development Workflow
1. **Understand**: Read relevant `docs/*.md`.
2. **Plan**: Define implementation in a plan file.
3. **Implement**: Write modular, typed code.
4. **Review**: Self-review against `docs/15_CODING_GUIDELINES.md`.
5. **Test**: Create unit/integration tests.
6. **Document**: Update architecture/API docs if changed.

## AI Workflow
- **Source of Truth**: Always treat `docs/` as the highest priority.
- **Step-by-Step**: Understand $\rightarrow$ Plan $\rightarrow$ Implement $\rightarrow$ Review $\rightarrow$ Test $\rightarrow$ Document.
- **Modularity**: Ensure new features don't introduce tight coupling or circular dependencies.

## Rules for Modifying Code
- **No Hardcoding**: All config must be in `.env` or `settings.py`.
- **No Raw SQL**: Use SQLAlchemy ORM.
- **No Direct Provider Calls**: Use the LLM Router.
- **Event-First**: Prefer publishing events over direct module calls.
- **Fail Gracefully**: Use global exception handlers and structured logging.

## Definition of Done
- [ ] Implementation meets SRS requirements.
- [ ] Code follows coding guidelines (types, docstrings, naming).
- [ ] Unit and integration tests pass.
- [ ] Documentation updated (`docs/`).
- [ ] No new technical debt introduced without recording in `docs/14_PROJECT_MEMORY.md`.

## Important Project Documents
- `docs/00_PROJECT_MASTER_PLAN.md`: Single source of truth.
- `docs/04_SYSTEM_ARCHITECTURE.md`: High-level design.
- `docs/05_AI_AGENT_ARCHITECTURE.md`: Agent definitions.
- `docs/08_DATABASE_DESIGN.md`: Schema and persistence.
- `docs/09_API_SPECIFICATION.md`: Endpoint definitions.
- `docs/11_CONFIGURATION.md`: Environment variables.
- `docs/15_CODING_GUIDELINES.md`: Standards.

## Scope Control
- **MVP Focus**: Google Meet only. Local-first execution.
- **Out of Scope**: Zoom/Teams, Mobile App, Cloud Sync, Multi-user support.
