import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
from backend.app.config.settings import settings

def setup_logging():
    """
    Configures the application logging system.
    """
    log_level = getattr(logging, settings.logging.level.upper(), logging.INFO)
    log_format = logging.Formatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Ensure logs directory exists
    log_dir = Path(settings.logging.path)
    log_dir.mkdir(parents=True, exist_ok=True)

    handlers = []

    if settings.logging.enable_console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(log_format)
        handlers.append(console_handler)

    if settings.logging.enable_file:
        file_handler = RotatingFileHandler(
            filename=log_dir / "app.log",
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5
        )
        file_handler.setFormatter(log_format)
        handlers.append(file_handler)

    logging.basicConfig(
        level=log_level,
        handlers=handlers,
        force=True
    )

    logger = logging.getLogger("ai_lecture_assistant")
    logger.info("Logging system initialized successfully.")
    return logger

# Initialize logging on module import if not already done
logger = setup_logging()
