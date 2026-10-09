from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import logging
from backend.app.core.exceptions import AppException, ErrorResponse

logger = logging.getLogger("ai_lecture_assistant.core.exceptions")

def register_exception_handlers(app: FastAPI):
    """
    Registers global exception handlers for the application.
    """
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
