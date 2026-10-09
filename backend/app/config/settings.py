from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional, List
import os

class AppSettings(BaseSettings):
    name: str = Field("AI Lecture Assistant", validation_alias="APP_NAME")
    env: str = Field("development", validation_alias="ENVIRONMENT")
    debug: bool = Field(True, validation_alias="APP_DEBUG")
    version: str = Field("1.0.0", validation_alias="APP_VERSION")

    @field_validator("env")
    @classmethod
    def validate_env(cls, v: str) -> str:
        allowed = ["development", "testing", "production"]
        if v not in allowed:
            raise ValueError(f"ENVIRONMENT must be one of {allowed}")
        return v

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

class ServerSettings(BaseSettings):
    host: str = Field("127.0.0.1", validation_alias="HOST")
    port: int = Field(8000, validation_alias="PORT")
    api_prefix: str = Field("/api/v1", validation_alias="API_PREFIX")

    # Production Hardening
    trusted_hosts: List[str] = Field(["*"], validation_alias="TRUSTED_HOSTS")
    gzip_enabled: bool = Field(True, validation_alias="GZIP_ENABLED")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

class DatabaseSettings(BaseSettings):
    url: str = Field("sqlite:///storage/database.db", validation_alias="DATABASE_URL")
    pool_size: int = Field(20, validation_alias="DB_POOL_SIZE")
    max_overflow: int = Field(10, validation_alias="DB_MAX_OVERFLOW")
    pool_timeout: int = Field(30, validation_alias="DB_POOL_TIMEOUT")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

class StorageSettings(BaseSettings):
    base_path: str = Field("storage/", validation_alias="STORAGE_PATH")
    meeting_path: str = Field("storage/meetings/", validation_alias="MEETING_PATH")
    transcript_path: str = Field("storage/transcripts/", validation_alias="TRANSCRIPT_PATH")
    notes_path: str = Field("storage/notes/", validation_alias="NOTES_PATH")
    pdf_path: str = Field("storage/pdf/", validation_alias="PDF_PATH")
    temp_path: str = Field("storage/temp/", validation_alias="TEMP_PATH")

    # Auto-creation paths
    required_dirs: List[str] = [
        "meetings", "logs", "temp", "cache", "uploads"
    ]

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

class LoggingSettings(BaseSettings):
    level: str = Field("INFO", validation_alias="LOG_LEVEL")
    path: str = Field("logs/", validation_alias="LOG_PATH")
    enable_file: bool = Field(True, validation_alias="ENABLE_FILE_LOGGING")
    enable_console: bool = Field(True, validation_alias="ENABLE_CONSOLE_LOGGING")
    json_format: bool = Field(False, validation_alias="LOG_JSON_FORMAT")
    max_bytes: int = Field(10 * 1024 * 1024, validation_alias="LOG_MAX_BYTES")
    backup_count: int = Field(5, validation_alias="LOG_BACKUP_COUNT")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

class AISettings(BaseSettings):
    default_provider: str = Field("grok", validation_alias="DEFAULT_PROVIDER")
    default_model: str = Field("grok-4-fast", validation_alias="DEFAULT_MODEL")
    fallback_providers: List[str] = Field(
        ["openai", "gemini"],
        validation_alias="FALLBACK_PROVIDERS"
    )
    max_retries: int = Field(3, validation_alias="MAX_AI_RETRIES")
    timeout: int = Field(30, validation_alias="AI_TIMEOUT")
    retry_delay: int = Field(5, validation_alias="AI_RETRY_DELAY")
    max_tokens: int = Field(2048, validation_alias="AI_MAX_TOKENS")
    temperature: float = Field(0.7, validation_alias="AI_TEMPERATURE")
    top_p: float = Field(1.0, validation_alias="AI_TOP_P")

    openai_api_key: Optional[str] = Field(None, validation_alias="OPENAI_API_KEY")
    openai_base_url: Optional[str] = Field(None, validation_alias="OPENAI_BASE_URL")
    anthropic_api_key: Optional[str] = Field(None, validation_alias="ANTHROPIC_API_KEY")
    gemini_api_key: Optional[str] = Field(None, validation_alias="GEMINI_API_KEY")
    grok_api_key: Optional[str] = Field(None, validation_alias="GROK_API_KEY")
    grok_base_url: str = Field("https://api.x.ai/v1", validation_alias="GROK_BASE_URL")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

class NotesSettings(BaseSettings):
    chunk_size: int = Field(4000, validation_alias="NOTES_CHUNK_SIZE")
    chunk_overlap: int = Field(500, validation_alias="NOTES_CHUNK_OVERLAP")
    max_parallel_chunks: int = Field(3, validation_alias="NOTES_MAX_PARALLEL_CHUNKS")
    prompt_version: str = Field("1.0", validation_alias="NOTES_PROMPT_VERSION")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

class QuizSettings(BaseSettings):
    mcq_count: int = Field(5, validation_alias="QUIZ_MCQ_COUNT")
    subjective_count: int = Field(3, validation_alias="QUIZ_SUBJECTIVE_COUNT")
    true_false_count: int = Field(5, validation_alias="QUIZ_TRUE_FALSE_COUNT")
    fill_blank_count: int = Field(5, validation_alias="QUIZ_FILL_BLANK_COUNT")
    difficulty: str = Field("medium", validation_alias="QUIZ_DIFFICULTY")
    temperature: float = Field(0.7, validation_alias="QUIZ_TEMPERATURE")
    max_tokens: int = Field(4096, validation_alias="QUIZ_MAX_TOKENS")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

class WhisperSettings(BaseSettings):
    model_size: str = Field("medium", validation_alias="WHISPER_MODEL")
    device: str = Field("cpu", validation_alias="WHISPER_DEVICE")
    compute_type: str = Field("int8", validation_alias="WHISPER_COMPUTE_TYPE")
    beam_size: int = Field(5, validation_alias="WHISPER_BEAM_SIZE")
    language: str = Field("auto", validation_alias="WHISPER_LANGUAGE")
    vad_enabled: bool = Field(True, validation_alias="WHISPER_VAD_ENABLED")
    word_timestamps: bool = Field(True, validation_alias="WHISPER_WORD_TIMESTAMPS")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

class FlashcardSettings(BaseSettings):
    flashcard_count: int = Field(20, validation_alias="FLASHCARD_COUNT")
    difficulty: str = Field("medium", validation_alias="FLASHCARD_DIFFICULTY")
    temperature: float = Field(0.7, validation_alias="FLASHCARD_TEMPERATURE")
    max_tokens: int = Field(4096, validation_alias="FLASHCARD_MAX_TOKENS")
    prompt_version: str = Field("1.0", validation_alias="FLASHCARD_PROMPT_VERSION")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

class AssignmentSettings(BaseSettings):
    assignment_type: str = Field("problem_set", validation_alias="ASSIGNMENT_TYPE")
    difficulty: str = Field("medium", validation_alias="ASSIGNMENT_DIFFICULTY")
    question_count: int = Field(5, validation_alias="ASSIGNMENT_QUESTION_COUNT")
    word_limit: int = Field(1000, validation_alias="ASSIGNMENT_WORD_LIMIT")
    temperature: float = Field(0.7, validation_alias="ASSIGNMENT_TEMPERATURE")
    max_tokens: int = Field(4096, validation_alias="ASSIGNMENT_MAX_TOKENS")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

class StudyPackSettings(BaseSettings):
    version: str = Field("1.0", validation_alias="STUDY_PACK_VERSION")
    include_notes: bool = Field(True, validation_alias="SP_INCLUDE_NOTES")
    include_quiz: bool = Field(True, validation_alias="SP_INCLUDE_QUIZ")
    include_flashcards: bool = Field(True, validation_alias="SP_INCLUDE_FLASHCARDS")
    include_assignment: bool = Field(True, validation_alias="SP_INCLUDE_ASSIGNMENT")
    include_attendance: bool = Field(True, validation_alias="SP_INCLUDE_ATTENDANCE")
    include_transcript: bool = Field(True, validation_alias="SP_INCLUDE_TRANSCRIPT")
    generate_readme: bool = Field(True, validation_alias="SP_GENERATE_README")
    generate_index: bool = Field(True, validation_alias="SP_GENERATE_INDEX")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

class BrowserSettings(BaseSettings):
    executable_path: Optional[str] = Field(None, validation_alias="BROWSER_EXECUTABLE_PATH")
    user_data_dir: str = Field("storage/browser_profile", validation_alias="USER_DATA_DIR")
    join_timeout: int = Field(30000, validation_alias="JOIN_TIMEOUT")
    retry_count: int = Field(3, validation_alias="RETRY_COUNT")
    retry_delay: int = Field(5, validation_alias="RETRY_DELAY")
    headless: bool = Field(False, validation_alias="HEADLESS_MODE")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

class AudioSettings(BaseSettings):
    sample_rate: int = Field(44100, validation_alias="AUDIO_SAMPLE_RATE")
    channels: int = Field(2, validation_alias="AUDIO_CHANNELS")
    format: str = Field("wav", validation_alias="AUDIO_FORMAT")
    chunk_size: int = Field(1024, validation_alias="AUDIO_CHUNK_SIZE")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

class AuthSettings(BaseSettings):
    jwt_secret: str = Field("super-secret-key-change-me-in-prod", validation_alias="JWT_SECRET")
    jwt_algorithm: str = Field("HS256", validation_alias="JWT_ALGORITHM")
    access_token_expire_minutes: int = Field(30, validation_alias="ACCESS_TOKEN_EXPIRE_MINUTES")
    refresh_token_expire_days: int = Field(7, validation_alias="REFRESH_TOKEN_EXPIRE_DAYS")
    bcrypt_rounds: int = Field(12, validation_alias="BCRYPT_ROUNDS")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

class Settings:
    """
    Main Configuration class that aggregates all settings categories.
    """
    def __init__(self):
        self.app = AppSettings()
        self.server = ServerSettings()
        self.database = DatabaseSettings()
        self.storage = StorageSettings()
        self.logging = LoggingSettings()
        self.ai = AISettings()
        self.notes = NotesSettings()
        self.quiz = QuizSettings()
        self.flashcards = FlashcardSettings()
        self.assignments = AssignmentSettings()
        self.study_pack = StudyPackSettings()
        self.whisper = WhisperSettings()
        self.browser = BrowserSettings()
        self.audio = AudioSettings()
        self.auth = AuthSettings()

# Global settings instance
settings = Settings()
