# System Architecture

## High-Level Design
The AI Lecture Assistant is a modular monolith designed for local-first execution with production-ready containerization.

## Component Breakdown
- **API Layer**: FastAPI providing a REST interface and WebSocket streams.
- **AI Orchestration**: A central LLM Router that handles requests across multiple providers (OpenAI, Grok, Gemini, etc.).
- **Speech Processing**: `faster-whisper` for high-performance transcription.
- **Browser Automation**: Playwright (Chromium) for Google Meet interaction.
- **Event System**: A central `EventDispatcher` for asynchronous communication between services.
- **Infrastructure**: 
    - **PostgreSQL**: Persistent storage for users and meeting metadata.
    - **Redis**: Caching and temporary state.
    - **Local Filesystem**: Storage for large audio files and generated documents.

## Data Flow
1. User triggers `join_meeting` $\rightarrow$ Playwright bot joins Meet.
2. Audio is captured $\rightarrow$ Saved to `storage/audio`.
3. Audio is transcribed $\rightarrow$ Saved to `storage/transcripts`.
4. LLM generates notes, quizzes, and flashcards $\rightarrow$ Saved to `storage/notes`, etc.
5. User retrieves artifacts via REST API or real-time updates via WebSockets.
