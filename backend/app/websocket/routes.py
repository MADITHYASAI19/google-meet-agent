from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query, status
from backend.app.websocket.manager import manager
from backend.app.websocket.events import WebSocketEvent
from backend.app.auth.jwt import jwt_handler
from backend.app.auth.dependencies import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.repositories.auth_repositories import UserRepository
import logging

logger = logging.getLogger("ai_lecture_assistant.websocket.routes")
router = APIRouter()

async def authenticate_websocket(websocket: WebSocket, token: str):
    """
    Validates the JWT token for WebSocket connections.
    Closes the connection with code 1008 if authentication fails.
    """
    try:
        # 1. Validate JWT
        payload = jwt_handler.decode_token(token)
        user_id = payload.get("sub")
        if not user_id:
            raise Exception("Token missing user identifier")

        # 2. Verify user exists and is active
        # Note: We need a DB session here. In a real FastAPI app, we might use a dependency
        # but for WS we often manually manage the session or use a global one.
        from backend.app.db.session import session_factory
        async with session_factory() as db:
            user_repo = UserRepository(db)
            user = await user_repo.get_by_id(int(user_id))
            if not user or not user.is_active:
                raise Exception("User not found or inactive")

        return True
    except Exception as e:
        logger.warning(f"WebSocket authentication failed: {e}")
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return False

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, token: str = Query(None)):
    """Global system notifications WebSocket."""
    if not token or not await authenticate_websocket(websocket, token):
        return

    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            logger.debug(f"Received message from global WS: {data}")
    except WebSocketDisconnect:
        await manager.disconnect(websocket)
        logger.info("Global WebSocket client disconnected")

@router.websocket("/ws/meetings/{meeting_id}")
async def meeting_websocket_endpoint(websocket: WebSocket, meeting_id: str, token: str = Query(None)):
    """Meeting-specific updates WebSocket."""
    if not token or not await authenticate_websocket(websocket, token):
        return

    await manager.connect(websocket, meeting_id=meeting_id)
    try:
        while True:
            data = await websocket.receive_text()
            logger.debug(f"Received message from meeting {meeting_id} WS: {data}")
    except WebSocketDisconnect:
        await manager.disconnect(websocket, meeting_id=meeting_id)
        logger.info(f"Meeting {meeting_id} WebSocket client disconnected")

@router.websocket("/ws/system")
async def system_websocket_endpoint(websocket: WebSocket, token: str = Query(None)):
    """System-wide health and status WebSocket."""
    if not token or not await authenticate_websocket(websocket, token):
        return

    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            logger.debug(f"Received message from system WS: {data}")
    except WebSocketDisconnect:
        await manager.disconnect(websocket)
        logger.info("System WebSocket client disconnected")
