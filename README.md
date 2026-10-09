# AI Lecture Assistant - Project Documentation

## Installation
Follow the steps in `DEPLOYMENT.md` to install and run the project.

## Quick Start
1. Clone the repository.
2. Copy `.env.example` to `.env` and fill in your API keys.
3. Run `docker-compose up --build -d`.
4. Access the API at `http://localhost:8000/api/v1`.

## Project Structure
- `backend/`: FastAPI application.
- `frontend/`: Next.js frontend.
- `storage/`: Local storage for artifacts.
- `scripts/`: Deployment and utility scripts.
