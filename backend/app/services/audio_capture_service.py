import asyncio
import logging
import wave
import time
from typing import Dict, Optional
from pathlib import Path

import pyaudio
from backend.app.config.settings import settings
from backend.app.core.event_dispatcher import dispatcher
from backend.app.events.meeting_events import (
    MeetingJoined, MeetingEnded, AudioCaptureStarted, AudioCaptureStopped, AudioCaptureFailed
)
from backend.app.services.storage_service import storage_manager

logger = logging.getLogger("ai_lecture_assistant.audio_capture")

class AudioCaptureService:
    """
    Service responsible for capturing system audio during a meeting.
    Uses WASAPI Loopback on Windows to record output audio.
    """
    def __init__(self):
        self.p = pyaudio.PyAudio()
        self._active_recordings: Dict[str, asyncio.Task] = {}
        self._stop_events: Dict[str, asyncio.Event] = {}

    async def handle_meeting_joined(self, event: MeetingJoined):
        """
        Callback triggered when a meeting is joined.
        """
        meeting_id = event.meeting_id
        if meeting_id in self._active_recordings:
            logger.warning(f"Recording already active for meeting {meeting_id}. Skipping.")
            return

        logger.info(f"Starting audio capture for meeting {meeting_id}...")

        # Setup storage path
        try:
            meeting_dir = storage_manager.get_meeting_folder(meeting_id)
            audio_dir = meeting_dir / "audio"
            audio_dir.mkdir(parents=True, exist_ok=True)
            file_path = audio_dir / "raw_audio.wav"
        except Exception as e:
            logger.error(f"Failed to setup audio storage for {meeting_id}: {e}")
            await dispatcher.publish(AudioCaptureFailed(meeting_id=meeting_id, error_message=str(e)))
            return

        # Start recording loop in background
        stop_event = asyncio.Event()
        self._stop_events[meeting_id] = stop_event

        recording_task = asyncio.create_task(
            self._recording_loop(meeting_id, file_path, stop_event)
        )
        self._active_recordings[meeting_id] = recording_task

        await dispatcher.publish(AudioCaptureStarted(meeting_id=meeting_id, file_path=str(file_path)))
        logger.info(f"Audio capture started. Saving to {file_path}")

    async def handle_meeting_ended(self, event: MeetingEnded):
        """
        Callback triggered when a meeting ends.
        """
        meeting_id = event.meeting_id
        if meeting_id not in self._active_recordings:
            return

        logger.info(f"Stopping audio capture for meeting {meeting_id}...")

        # Signal the loop to stop
        stop_event = self._stop_events.get(meeting_id)
        if stop_event:
            stop_event.set()

        # Wait for the task to finish and cleanup
        task = self._active_recordings.pop(meeting_id)
        try:
            await task
        except Exception as e:
            logger.error(f"Error while stopping recording for {meeting_id}: {e}")
        finally:
            self._stop_events.pop(meeting_id, None)

        # Note: The actual file path is recovered from the storage manager
        meeting_dir = storage_manager.get_meeting_folder(meeting_id)
        file_path = meeting_dir / "audio" / "raw_audio.wav"

        await dispatcher.publish(AudioCaptureStopped(
            meeting_id=meeting_id,
            file_path=str(file_path),
            duration_seconds=0.0 # Simplified for MVP
        ))
        logger.info(f"Audio capture stopped for meeting {meeting_id}.")

    async def _recording_loop(self, meeting_id: str, file_path: Path, stop_event: asyncio.Event):
        """
        The core recording loop using PyAudio WASAPI Loopback.
        """
        try:
            # Find WASAPI Loopback device
            device_index = self._find_loopback_device()
            if device_index is None:
                raise RuntimeError("No WASAPI loopback device found. Please check your system audio settings.")

            # Open stream
            stream = self.p.open(
                format=pyaudio.paInt16,
                channels=settings.audio.channels,
                rate=settings.audio.sample_rate,
                input=True,
                input_device_index=device_index,
                frames_per_buffer=settings.audio.chunk_size
            )

            # Open WAV file
            with wave.open(str(file_path), 'wb') as wf:
                wf.setnchannels(settings.audio.channels)
                wf.setsampwidth(self.p.get_sample_size(pyaudio.paInt16))
                wf.setframerate(settings.audio.sample_rate)

                while not stop_event.is_set():
                    try:
                        # Read audio data in a thread pool to avoid blocking the event loop
                        data = await asyncio.to_thread(stream.read, settings.audio.chunk_size)
                        wf.writeframes(data)
                    except Exception as e:
                        logger.error(f"Error reading audio chunk for {meeting_id}: {e}")
                        break

            stream.stop_stream()
            stream.close()

        except Exception as e:
            logger.error(f"Critical recording failure for {meeting_id}: {e}", exc_info=True)
            await dispatcher.publish(AudioCaptureFailed(meeting_id=meeting_id, error_message=str(e)))
        finally:
            # Final cleanup happens here
            pass

    def _find_loopback_device(self) -> Optional[int]:
        """
        Search for the default WASAPI loopback device.
        """
        # PyAudio doesn't explicitly flag loopback devices in a standard way across all versions
        # but we look for 'Stereo Mix' or 'WASAPI' in the device names.
        for i in range(self.p.get_device_count()):
            dev = self.p.get_device_info_by_index(i)
            if dev['hostApi'] == self.p.get_host_api_info_by_index(0)['index']: # Simplified WASAPI check
                if "loopback" in dev['name'].lower() or "stereo mix" in dev['name'].lower():
                    return i

        # Fallback: try the default input device
        return self.p.get_default_input_device()

    def shutdown(self):
        """
        Cleanly shut down PyAudio resources.
        """
        self.p.terminate()

# Singleton instance
audio_capture_service = AudioCaptureService()
