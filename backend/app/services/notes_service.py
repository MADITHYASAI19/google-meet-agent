import logging
import json
import asyncio
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import asdict

from backend.app.core.event_dispatcher import dispatcher
from backend.app.events.meeting_events import (
    TranscriptionCompleted, NotesGenerationStarted, NotesGenerationProgress,
    NotesGenerationCompleted, NotesGenerationFailed
)
from backend.app.llm.router import llm_router
from backend.app.llm.models import LLMRequest
from backend.app.services.storage_service import storage_manager
from backend.app.config.settings import settings

logger = logging.getLogger("ai_lecture_assistant")

class NotesService:
    """
    AI Notes Generator Service.
    Transforms raw transcripts into structured study notes using the LLMRouter.
    """

    def __init__(self):
        self.settings = settings.notes

    async def handle_transcription_completed(self, event: TranscriptionCompleted):
        """
        Triggered by TranscriptionCompleted event to start the notes generation pipeline.
        """
        meeting_id = event.meeting_id
        package_path = event.transcript_package_path

        logger.info(f"Starting notes generation for meeting: {meeting_id}")
        await dispatcher.publish(NotesGenerationStarted(meeting_id=meeting_id))

        try:
            # 1. Load & 2. Validate
            transcript_data = await self._load_transcript(package_path)

            # 3. Chunking
            chunks = self._chunk_transcript(transcript_data["segments"])
            total_chunks = len(chunks)

            # 4. & 5. Prompt Preparation
            system_prompt = await self._load_prompt("notes_system_prompt.md")
            user_prompt_template = await self._load_prompt("notes_user_prompt.md")

            # 6. Generate (Iterative)
            all_chunk_results = []
            for i, chunk_text in enumerate(chunks):
                # Calculate progress
                progress = ((i + 1) / total_chunks) * 100
                await dispatcher.publish(NotesGenerationProgress(
                    meeting_id=meeting_id,
                    chunk_index=i,
                    total_chunks=total_chunks,
                    progress_percentage=progress
                ))

                # Replace placeholders
                prompt = user_prompt_template.replace("{{transcript}}", chunk_text)
                prompt = prompt.replace("{{lecture_title}}", "Lecture") # Simplified
                prompt = prompt.replace("{{subject}}", "General") # Simplified
                prompt = prompt.replace("{{language}}", transcript_data.get("language", "English"))

                # Invoke LLMRouter
                result = await llm_router.generate(LLMRequest(
                    prompt=prompt,
                    system_prompt=system_prompt,
                    temperature=settings.ai.temperature,
                    max_tokens=settings.ai.max_tokens
                ))
                all_chunk_results.append(result.text)

            # 7. Merge & 8. Normalize
            merged_json = await self._merge_and_normalize(all_chunk_results)

            # 9. Format & Save
            package_path = await self._save_notes_package(meeting_id, merged_json, total_chunks)

            logger.info(f"Notes generation completed successfully for meeting: {meeting_id}")
            await dispatcher.publish(NotesGenerationCompleted(
                meeting_id=meeting_id,
                notes_package_path=str(package_path)
            ))

        except Exception as e:
            logger.error(f"Notes generation failed for meeting {meeting_id}: {str(e)}")
            await dispatcher.publish(NotesGenerationFailed(
                meeting_id=meeting_id,
                error_message=str(e)
            ))

    # --- Pipeline Stage Helpers ---

    async def _load_transcript(self, package_path: str) -> Dict[str, Any]:
        path = Path(package_path) / "raw" / "transcript.json"
        if not path.exists():
            raise FileNotFoundError(f"Transcript file not found at {path}")

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if not data.get("segments"):
            raise ValueError("Transcript contains no segments.")

        return data

    def _chunk_transcript(self, segments: List[Dict[str, Any]]) -> List[str]:
        chunks = []
        current_chunk = []
        current_tokens = 0

        # Simplified token counting: 4 chars per token
        def get_tokens(text: str) -> int:
            return len(text) // 4

        for i, seg in enumerate(segments):
            text = seg.get("text", "")
            tokens = get_tokens(text)

            if current_tokens + tokens > self.settings.chunk_size:
                # Save current chunk
                chunks.append(" ".join([s["text"] for s in current_chunk]))

                # Implement Overlap: keep last few segments
                overlap_tokens = 0
                overlap_segments = []
                for seg_back in reversed(current_chunk):
                    t = get_tokens(seg_back["text"])
                    if overlap_tokens + t <= self.settings.chunk_overlap:
                        overlap_segments.insert(0, seg_back)
                        overlap_tokens += t
                    else:
                        break

                current_chunk = overlap_segments + [seg]
                current_tokens = overlap_tokens + tokens
            else:
                current_chunk.append(seg)
                current_tokens += tokens

        if current_chunk:
            chunks.append(" ".join([s["text"] for s in current_chunk]))

        return chunks

    async def _load_prompt(self, filename: str) -> str:
        path = Path("backend/app/prompts") / filename
        if not path.exists():
            raise FileNotFoundError(f"Prompt file not found: {path}")
        return path.read_text(encoding="utf-8")

    async def _merge_and_normalize(self, results: List[str]) -> Dict[str, Any]:
        """
        Merges multiple JSON responses from chunks into one structured document.
        """
        merged = {
            "title": "Lecture Notes",
            "overview": "",
            "key_concepts": [], "definitions": [], "important_points": [],
            "examples": [], "formulas": [], "code_snippets": [],
            "best_practices": [], "common_mistakes": [], "summary": ""
        }

        for res_text in results:
            try:
                # Attempt to extract JSON from response (handling potential markdown wrap)
                if "```json" in res_text:
                    res_text = res_text.split("```json")[1].split("```")[0].strip()
                elif "```" in res_text:
                    res_text = res_text.split("```")[1].split("```")[0].strip()

                data = json.loads(res_text)

                # Merge lists
                for key in ["key_concepts", "definitions", "important_points", "examples", "formulas", "code_snippets", "best_practices", "common_mistakes"]:
                    if key in data and isinstance(data[key], list):
                        merged[key].extend(data[key])

                # Update strings (last one wins or concatenate)
                if data.get("title"): merged["title"] = data["title"]
                if data.get("overview"): merged["overview"] += "\n" + data["overview"]
                if data.get("summary"): merged["summary"] += "\n" + data["summary"]

            except Exception as e:
                logger.warning(f"Failed to parse chunk response as JSON: {e}")

        return merged

    async def _save_notes_package(self, meeting_id: str, data: Dict[str, Any], chunk_count: int) -> Path:
        meeting_dir = storage_manager.get_meeting_folder(meeting_id)
        notes_dir = meeting_dir / "notes"
        notes_dir.mkdir(parents=True, exist_ok=True)

        # 1. notes.json
        with open(notes_dir / "notes.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        # 2. notes.md
        md_content = f"# {data['title']}\n\n"
        md_content += f"## Overview\n{data['overview']}\n\n"

        for section in ["key_concepts", "definitions", "important_points", "examples", "formulas", "code_snippets", "best_practices", "common_mistakes"]:
            items = data.get(section, [])
            if items:
                md_content += f"## {section.replace('_', ' ').title()}\n"
                for item in items:
                    if isinstance(item, dict) and "term" in item:
                        md_content += f"- **{item['term']}**: {item.get('explanation', item.get('definition', ''))}\n"
                    else:
                        md_content += f"- {item}\n"
                md_content += "\n"

        md_content += f"## Summary\n{data['summary']}"

        with open(notes_dir / "notes.md", "w", encoding="utf-8") as f:
            f.write(md_content)

        # 3. metadata.json
        metadata = {
            "meeting_id": meeting_id,
            "generation_time": datetime.now().isoformat(),
            "chunk_count": chunk_count,
            "provider": settings.ai.default_provider,
            "model": settings.ai.default_model
        }
        with open(notes_dir / "metadata.json", "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2)

        # 4. statistics.json
        stats = {
            "word_count": len(data["summary"].split()) if data["summary"] else 0,
            "chunk_count": chunk_count
        }
        with open(notes_dir / "statistics.json", "w", encoding="utf-8") as f:
            json.dump(stats, f, indent=2)

        return notes_dir

notes_service = NotesService()
