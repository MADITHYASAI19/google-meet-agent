import logging
import json
import asyncio
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple

from backend.app.core.event_dispatcher import dispatcher
from backend.app.events.meeting_events import (
    NotesGenerationCompleted, QuizGenerationStarted, QuizGenerationProgress,
    QuizGenerationCompleted, QuizGenerationFailed
)
from backend.app.llm.router import llm_router
from backend.app.llm.models import LLMRequest
from backend.app.services.storage_service import storage_manager
from backend.app.config.settings import settings

logger = logging.getLogger("ai_lecture_assistant")

class QuizService:
    """
    AI Quiz Generator Service.
    Transforms structured study notes into a complete quiz package using the LLMRouter.
    """

    def __init__(self):
        self.settings = settings.quiz

    async def handle_notes_completed(self, event: NotesGenerationCompleted):
        """
        Triggered by NotesGenerationCompleted event to start the quiz generation pipeline.
        """
        meeting_id = event.meeting_id
        notes_package_path = event.notes_package_path

        logger.info(f"Starting quiz generation for meeting: {meeting_id}")
        await dispatcher.publish(QuizGenerationStarted(meeting_id=meeting_id))

        try:
            # Stage 1 & 2: Load & Validate
            notes_data = await self._load_notes(notes_package_path)

            # Stage 3: Load Prompts
            system_prompt = await self._load_prompt("quiz_system_prompt.md")
            user_prompt_template = await self._load_prompt("quiz_user_prompt.md")

            # Stage 4: Replace Placeholders
            prompt = self._prepare_prompt(notes_data, user_prompt_template)

            # Stage 5: Generate
            await dispatcher.publish(QuizGenerationProgress(
                meeting_id=meeting_id,
                stage="Generating Quiz Content",
                progress_percentage=30.0
            ))

            result = await llm_router.generate(LLMRequest(
                prompt=prompt,
                system_prompt=system_prompt,
                temperature=self.settings.temperature,
                max_tokens=self.settings.max_tokens
            ))

            # Stage 6 & 7: Validate & Normalize
            await dispatcher.publish(QuizGenerationProgress(
                meeting_id=meeting_id,
                stage="Validating and Normalizing",
                progress_percentage=60.0
            ))
            quiz_data = self._validate_and_normalize(result.text)

            # Stage 8, 9, 10: Format & Save
            package_path = await self._save_quiz_package(meeting_id, quiz_data, result)

            logger.info(f"Quiz generation completed successfully for meeting: {meeting_id}")
            await dispatcher.publish(QuizGenerationCompleted(
                meeting_id=meeting_id,
                quiz_package_path=str(package_path)
            ))

        except Exception as e:
            logger.error(f"Quiz generation failed for meeting {meeting_id}: {str(e)}")
            await dispatcher.publish(QuizGenerationFailed(
                meeting_id=meeting_id,
                error_message=str(e)
            ))

    # --- Pipeline Stage Helpers ---

    async def _load_notes(self, package_path: str) -> Dict[str, Any]:
        """Loads notes.json from the provided package path."""
        path = Path(package_path) / "notes.json"
        if not path.exists():
            raise FileNotFoundError(f"Notes file not found at {path}")

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if not data or not data.get("summary") and not data.get("key_concepts"):
            raise ValueError("Notes content is empty or invalid.")

        return data

    async def _load_prompt(self, filename: str) -> str:
        """Loads a prompt file from the prompts directory."""
        path = Path("backend/app/prompts") / filename
        if not path.exists():
            raise FileNotFoundError(f"Prompt file not found: {path}")
        return path.read_text(encoding="utf-8")

    def _prepare_prompt(self, notes_data: Dict[str, Any], template: str) -> str:
        """Injects metadata and notes into the user prompt template."""
        # Convert notes dict to a readable string for the LLM
        notes_text = json.dumps(notes_data, indent=2)

        prompt = template.replace("{{notes}}", notes_text)
        prompt = prompt.replace("{{difficulty}}", self.settings.difficulty)
        prompt = prompt.replace("{{mcq_count}}", str(self.settings.mcq_count))
        prompt = prompt.replace("{{true_false_count}}", str(self.settings.true_false_count))
        prompt = prompt.replace("{{fill_blank_count}}", str(self.settings.fill_blank_count))
        prompt = prompt.replace("{{subjective_count}}", str(self.settings.subjective_count))

        # Default values for missing fields in notes_data
        title = notes_data.get("title", "Lecture")
        prompt = prompt.replace("{{lecture_title}}", title)

        return prompt

    def _validate_and_normalize(self, raw_text: str) -> Dict[str, Any]:
        """
        Extracts JSON from LLM response and ensures it matches the required schema.
        """
        # Handle potential markdown wrapping
        if "```json" in raw_text:
            raw_text = raw_text.split("```json")[1].split("```")[0].strip()
        elif "```" in raw_text:
            raw_text = raw_text.split("```")[1].split("```")[0].strip()

        try:
            data = json.loads(raw_text)
        except json.JSONDecodeError as e:
            raise ValueError(f"LLM returned malformed JSON: {str(e)}")

        # Required keys
        required_keys = ["mcqs", "true_false", "fill_blanks", "subjective", "answer_key"]
        for key in required_keys:
            if key not in data:
                raise ValueError(f"Missing required quiz section: {key}")

        return data

    async def _save_quiz_package(self, meeting_id: str, quiz_data: Dict[str, Any], llm_response: Any) -> Path:
        """
        Saves the quiz artifacts into the storage directory.
        """
        meeting_dir = storage_manager.get_meeting_folder(meeting_id)
        quiz_dir = meeting_dir / "quiz"
        quiz_dir.mkdir(parents=True, exist_ok=True)

        # 1. Type-specific JSONs
        with open(quiz_dir / "mcq.json", "w", encoding="utf-8") as f:
            json.dump(quiz_data["mcqs"], f, indent=2)

        with open(quiz_dir / "true_false.json", "w", encoding="utf-8") as f:
            json.dump(quiz_data["true_false"], f, indent=2)

        with open(quiz_dir / "fill_blanks.json", "w", encoding="utf-8") as f:
            json.dump(quiz_data["fill_blanks"], f, indent=2)

        with open(quiz_dir / "subjective.json", "w", encoding="utf-8") as f:
            json.dump(quiz_data["subjective"], f, indent=2)

        with open(quiz_dir / "answer_key.json", "w", encoding="utf-8") as f:
            json.dump(quiz_data["answer_key"], f, indent=2)

        # 2. quiz.md (Markdown)
        md_content = f"# Quiz: {quiz_data.get('title', 'Lecture Quiz')}\n\n"

        # MCQ Section
        if quiz_data.get("mcqs"):
            md_content += "## Multiple Choice Questions\n\n"
            for i, q in enumerate(quiz_data["mcqs"], 1):
                md_content += f"{i}. {q['question']}\n"
                for opt in q.get("options", []):
                    md_content += f"   - {opt}\n"
                md_content += "\n"

        # True/False Section
        if quiz_data.get("true_false"):
            md_content += "## True or False\n\n"
            for i, q in enumerate(quiz_data["true_false"], 1):
                md_content += f"{i}. {q['question']}\n"
                md_content += "\n"

        # Fill Blanks Section
        if quiz_data.get("fill_blanks"):
            md_content += "## Fill in the Blanks\n\n"
            for i, q in enumerate(quiz_data["fill_blanks"], 1):
                md_content += f"{i}. {q['question']}\n"
                md_content += "\n"

        # Subjective Section
        if quiz_data.get("subjective"):
            md_content += "## Subjective Questions\n\n"
            for i, q in enumerate(quiz_data["subjective"], 1):
                md_content += f"{i}. {q['question']} ({q.get('marks', 0)} marks)\n"
                md_content += "\n"

        # Answer Key Section
        md_content += "## Answer Key\n\n"
        for i, q in enumerate(quiz_data["mcqs"], 1):
            md_content += f"MCQ {i}: {q.get('answer', 'N/A')}\n"
        for i, q in enumerate(quiz_data["true_false"], 1):
            md_content += f"T/F {i}: {q.get('answer', 'N/A')}\n"
        for i, q in enumerate(quiz_data["fill_blanks"], 1):
            md_content += f"Fill {i}: {q.get('answer', 'N/A')}\n"
        for i, q in enumerate(quiz_data["subjective"], 1):
            md_content += f"Subj {i}: {q.get('answer', 'N/A')}\n"

        with open(quiz_dir / "quiz.md", "w", encoding="utf-8") as f:
            f.write(md_content)

        # 3. metadata.json
        metadata = {
            "meeting_id": meeting_id,
            "generation_time": datetime.now().isoformat(),
            "provider": llm_response.provider,
            "model": llm_response.model,
            "token_usage": llm_response.usage.total_tokens,
            "prompt_version": "1.0"
        }
        with open(quiz_dir / "metadata.json", "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2)

        # 4. statistics.json
        stats = {
            "total_questions": len(quiz_data["mcqs"]) + len(quiz_data["true_false"]) +
                               len(quiz_data["fill_blanks"]) + len(quiz_data["subjective"]),
            "type_distribution": {
                "mcq": len(quiz_data["mcqs"]),
                "true_false": len(quiz_data["true_false"]),
                "fill_blanks": len(quiz_data["fill_blanks"]),
                "subjective": len(quiz_data["subjective"])
            },
            "generation_time": f"{llm_response.latency:.2f}s"
        }
        with open(quiz_dir / "statistics.json", "w", encoding="utf-8") as f:
            json.dump(stats, f, indent=2)

        return quiz_dir

quiz_service = QuizService()
