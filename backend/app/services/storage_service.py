from pathlib import Path
import logging
from backend.app.config.settings import settings

logger = logging.getLogger("ai_lecture_assistant")

class StorageManager:
    """
    Handles the creation and management of the application's storage directories.
    """
    def __init__(self):
        self.base_path = Path(settings.storage.base_path)
        self.required_dirs = [
            settings.storage.meeting_path,
            settings.storage.transcript_path,
            settings.storage.notes_path,
            settings.storage.pdf_path,
            settings.storage.temp_path,
        ]

    def initialize_storage(self):
        """
        Creates all required storage directories if they do not exist.
        """
        try:
            self.base_path.mkdir(parents=True, exist_ok=True)
            for dir_path in self.required_dirs:
                Path(dir_path).mkdir(parents=True, exist_ok=True)
            logger.info("Storage directories initialized successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize storage directories: {e}")
            raise RuntimeError(f"Critical failure initializing storage: {e}")

    def get_meeting_folder(self, meeting_id: str) -> Path:
        """
        Returns the dedicated folder for a specific meeting.
        """
        meeting_dir = Path(settings.storage.meeting_path) / meeting_id
        meeting_dir.mkdir(parents=True, exist_ok=True)
        return meeting_dir

storage_manager = StorageManager()
