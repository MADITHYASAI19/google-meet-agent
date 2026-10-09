import logging
from typing import Optional
from faster_whisper import WhisperModel
from backend.app.config.settings import settings

logger = logging.getLogger("ai_lecture_assistant.whisper_model_manager")

class WhisperModelManager:
    """
    Manages the lifecycle of the faster-whisper model.
    Ensures lazy loading and caching to optimize VRAM/RAM usage.
    """
    def __init__(self):
        self._model: Optional[WhisperModel] = None

    def get_model(self) -> WhisperModel:
        """
        Returns the cached Whisper model, loading it if necessary.
        """
        if self._model is None:
            logger.info(f"Loading Whisper model ({settings.whisper.model_size}) on {settings.whisper.device}...")
            try:
                self._model = WhisperModel(
                    model_size=settings.whisper.model_size,
                    device=settings.whisper.device,
                    compute_type=settings.whisper.compute_type
                )
                logger.info("Whisper model loaded successfully.")
            except Exception as e:
                logger.error(f"Failed to load Whisper model: {e}")
                raise RuntimeError(f"Could not initialize Whisper model: {e}")

        return self._model

    def unload_model(self):
        """
        Explicitly releases the model from memory.
        """
        if self._model:
            logger.info("Unloading Whisper model from memory...")
            self._model = None # Python's GC and faster-whisper's internal cleanup handle this
            logger.info("Whisper model unloaded.")

# Singleton instance
whisper_model_manager = WhisperModelManager()
