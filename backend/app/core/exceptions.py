from typing import Any, Optional, Generic, TypeVar
from pydantic import BaseModel
import logging

logger = logging.getLogger("ai_lecture_assistant.core.exceptions")

T = TypeVar("T")

class APIResponse(BaseModel, Generic[T]):
    """
    Standard wrapper for all successful API responses.
    """
    success: bool = True
    data: Optional[T] = None
    message: Optional[str] = None

class ErrorDetail(BaseModel):
    """
    Detailed error information.
    """
    code: str
    message: str
    details: Optional[Any] = None

class ErrorResponse(BaseModel):
    """
    Standard wrapper for all API error responses.
    """
    success: bool = False
    error: ErrorDetail

class AppException(Exception):
    """
    Base exception for all application-specific errors.
    """
    def __init__(self, status_code: int, error_code: str, message: str, details: Optional[Any] = None):
        self.status_code = status_code
        self.error_code = error_code
        self.message = message
        self.details = details
        super().__init__(self.message)

class EntityNotFoundException(AppException):
    """Raised when a requested resource is not found."""
    def __init__(self, entity: str, entity_id: str):
        super().__init__(
            status_code=404,
            error_code="ENTITY_NOT_FOUND",
            message=f"{entity} with ID {entity_id} not found"
        )

class ValidationException(AppException):
    """Raised when input validation fails."""
    def __init__(self, message: str, details: Optional[Any] = None):
        super().__init__(
            status_code=400,
            error_code="VALIDATION_ERROR",
            message=message,
            details=details
        )

class ExternalServiceException(AppException):
    """Raised when an external API (e.g., Google Meet) fails."""
    def __init__(self, service: str, message: str):
        super().__init__(
            status_code=502,
            error_code="EXTERNAL_SERVICE_ERROR",
            message=f"Error from {service}: {message}"
        )

def register_exception_handlers(app):
    """
    Registers global exception handlers for the application.
    """
    from fastapi import Request
    from fastapi.responses import JSONResponse

    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        logger.warning(f"Application error: {exc.error_code} - {exc.message}")
        return JSONResponse(
            status_code=exc.status_code,
            content=ErrorResponse(
                success=False,
                error=ErrorDetail(
                    code=exc.error_code,
                    message=exc.message,
                    details=exc.details
                )
            ).dict()
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        logger.error(f"Unhandled exception occurred: {exc}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content=ErrorResponse(
                success=False,
                error=ErrorDetail(
                    code="INTERNAL_SERVER_ERROR",
                    message="An unexpected error occurred on the server."
                )
            ).dict()
        )
