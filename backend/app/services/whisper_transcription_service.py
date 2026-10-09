import asyncio
import json
import logging
import time
from pathlib import Path
from typing import List, Dict, Any, Optional

from backend.app.config.settings import settings
from backend.app.core.event_dispatcher import dispatcher
from backend.app.events.meeting_events import (
    AudioCaptureStopped, TranscriptionStarted, TranscriptionCompleted,
    TranscriptionFailed, TranscriptionQueued, TranscriptionProgress
)
from backend.app.services.storage_service import storage_manager
from backend.app.services.whisper_model_manager import whisper_model_manager

logger = logging.getLogger("ai_lecture_assistant.whisper_service")

class TranscriptionJob:
    """
    Tracks the state of a single transcription task.
    """
    def __init__(self, meeting_id: str, audio_file: str):
        self.job_id = f"job_{int(time.time())}_{meeting_id[:8]}"
        self.meeting_id = meeting_id
        self.audio_file = audio_file
        self.status = "QUEUED"
        self.created_at = time.time()
        self.started_at: Optional[float] = None
        self.finished_at: Optional[float] = None
        self.processing_time: Optional[float] = None
        self.progress_percentage: float = 0.0

class WhisperTranscriptionService:
    """
    Orchestrates the transcription of audio files using faster-whisper.
    Implements incremental writing to support long lectures and failure recovery.
    """
    def __init__(self):
        self._active_jobs: Dict[str, TranscriptionJob] = {}

    async def handle_audio_capture_stopped(self, event: AudioCaptureStopped):
        """
        Event handler triggered when audio recording is finalized.
        """
        meeting_id = event.meeting_id
        audio_file = event.file_path

        # Create and track job
        job = TranscriptionJob(meeting_id, audio_file)
        self._active_jobs[meeting_id] = job

        await dispatcher.publish(TranscriptionQueued(meeting_id=meeting_id, audio_file_path=audio_file))
        logger.info(f"Transcription queued for meeting {meeting_id}")

        # Process in background to avoid blocking FastAPI
        asyncio.create_task(self._process_transcription(job))

    async def _process_transcription(self, job: TranscriptionJob):
        """
        The core transcription pipeline.
        """
        meeting_id = job.meeting_id
        try:
            job.status = "STARTING"
            job.started_at = time.time()
            await dispatcher.publish(TranscriptionStarted(meeting_id=meeting_id, audio_file_path=job.audio_file))
            logger.info(f"Starting transcription for meeting {meeting_id}...")

            # 1. Get model from manager (Lazy Loading)
            model = whisper_model_manager.get_model()

            # 2. Setup Storage Package
            meeting_dir = storage_manager.get_meeting_folder(meeting_id)
            transcript_dir = meeting_dir / "transcript"
            transcript_dir.mkdir(parents=True, exist_ok=True)

            raw_dir = transcript_dir / "raw"
            raw_dir.mkdir(parents=True, exist_ok=True)

            temp_dir = transcript_dir / "temp"
            temp_dir.mkdir(parents=True, exist_ok=True)

            temp_file = temp_dir / "transcript.jsonl"

            # 3. Transcribe (Offload to thread)
            job.status = "PROCESSING"
            segments, info = await asyncio.to_thread(
                self._run_whisper, model, job.audio_file
            )

            # 4. Incremental Write & Processing
            transcript_data = []
            total_segments = len(list(segments)) if hasattr(segments, '__len__') else 100 # fallback

            # Since segments is a generator, we iterate and save
            # Note: We re-run transcription if we need to count segments accurately,
            # or we estimate based on duration.

            # Re-running the generator to stream results
            segments = model.transcribe(job.audio_file, beam_size=settings.whisper.beam_size, language=settings.whisper.language)

            segment_id = 0
            for segment in segments:
                # Save to JSONL for recovery
                with open(temp_file, "a", encoding="utf-8") as f:
                    f.write(json.dumps({
                        "segment_id": segment_id,
                        "start": segment.start,
                        "end": segment.end,
                        "text": segment.text,
                        "probability": segment.avg_logprob,
                        "no_speech_prob": segment.no_speech_prob
                    }) + "\n")

                # Collect for final JSON
                transcript_data.append({
                    "segment_id": segment_id,
                    "start": segment.start,
                    "end": segment.end,
                    "text": segment.text,
                    "probability": segment.avg_logprob,
                    "no_speech_prob": segment.no_speech_prob,
                    "words": getattr(segment, 'words', []) # Word timestamps if enabled
                })

                segment_id += 1
                # Periodically publish progress
                if segment_id % 10 == 0:
                    progress = (segment.end / info.duration) * 100 if info.duration else 0
                    job.progress_percentage = progress
                    await dispatcher.publish(TranscriptionProgress(
                        meeting_id=meeting_id,
                        progress_percentage=progress,
                        current_segment=segment_id
                    ))

            # 5. Finalize Transcript Package
            self._save_transcript_package(meeting_id, transcript_dir, transcript_data, info, job)

            # Cleanup temp files
            if temp_file.exists():
                temp_file.unlink()

            job.finished_at = time.time()
            job.processing_time = job.finished_at - job.started_at
            job.status = "COMPLETED"

            await dispatcher.publish(TranscriptionCompleted(
                meeting_id=meeting_id,
                transcript_package_path=str(transcript_dir)
            ))
            logger.info(f"Transcription completed for meeting {meeting_id} in {job.processing_time:.2f}s")

        except Exception as e:
            logger.error(f"Transcription failed for meeting {meeting_id}: {e}", exc_info=True)
            job.status = "FAILED"
            await dispatcher.publish(TranscriptionFailed(meeting_id=meeting_id, error_message=str(e)))
        finally:
            self._active_jobs.pop(meeting_id, None)

    def _run_whisper(self, model, audio_path):
        """
        Synchronous wrapper for faster-whisper.
        """
        return model.transcribe(
            audio_path,
            beam_size=settings.whisper.beam_size,
            language=settings.whisper.language,
            vad_filter=settings.whisper.vad_enabled,
            word_timestamps=settings.whisper.word_timestamps
        )

    def _save_transcript_package(self, meeting_id: str, transcript_dir: Path, data: List[Dict], info: Any, job: TranscriptionJob):
        """
        Saves the la-layered transcript package (raw, metadata, language, stats).
        """
        raw_dir = transcript_dir / "raw"
        raw_dir.mkdir(parents=True, exist_ok=True)

        # 1. transcript.json (Normalized)
        with open(raw_dir / "transcript.json", "w", encoding="utf-8") as f:
            json.dump({
                "version": "1.0",
                "meeting_id": meeting_id,
                "language": info.language,
                "segments": data
            }, f, indent=2)

        # 2. metadata.json (Audit)
        with open(raw_dir / "metadata.json", "w", encoding="utf-8") as f:
            json.dump({
                "processing_info": {
                    "model_size": settings.whisper.model_size,
                    "compute_type": settings.whisper.compute_type,
                    "device": settings.whisper.device,
                    "transcription_time_seconds": job.processing_time,
                    "wall_clock_start": time.ctime(job.started_at),
                    "wall_clock_end": time.ctime(job.finished_at),
                },
                "audio_info": {
                    "source_file": job.audio_file,
                    "duration_seconds": info.duration,
                    "sample_rate": settings.audio.sample_rate
                },
                "status": job.status
            }, f, indent=2)

        # 3. language.json
        with open(raw_dir / "language.json", "w", encoding="utf-8") as f:
            json.dump({
                "detected_language": info.language,
                "confidence": info.language_probability,
                "timestamp": time.ctime()
            }, f, indent=2)

        # 4. statistics.json
        total_words = sum(len(s['text'].split()) for s in data)
        avg_conf = sum(s['probability'] for s in data) / len(data) if data else 0

        with open(transcript_dir / "statistics.json", "w", encoding="utf-8") as f:
            json.dump({
                "duration_seconds": info.duration,
                "segments": len(data),
                "words": total_words,
                "characters": sum(len(s['text']) for s in data),
                "average_confidence": avg_conf,
                "language": info.language
            }, f, indent=2)

# Singleton instance
whisper_transcription_service = WhisperTranscriptionService()
