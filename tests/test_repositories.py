import pytest
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.db.database import AsyncSessionLocal, init_db
from backend.app.db.models import Meeting, Transcript, Notes
from backend.app.repositories.meeting_repository import MeetingRepository
from backend.app.repositories.artifact_repositories import TranscriptRepository, NotesRepository
from backend.app.core.exceptions import EntityNotFoundException

@pytest.fixture
async def db_session():
    """Provides a clean async session for each test."""
    await init_db()
    async with AsyncSessionLocal() as session:
        yield session
        await session.rollback()
        await session.close()

@pytest.mark.asyncio
async def test_meeting_repository_crud(db_session: AsyncSession):
    repo = MeetingRepository(db_session)

    # Create
    meeting = await repo.create(uuid="test-uuid-123", title="Test Lecture")
    assert meeting.uuid == "test-uuid-123"
    assert meeting.id is not None

    # Read
    fetched = await repo.get_by_uuid("test-uuid-123")
    assert fetched.id == meeting.id

    # Update
    await repo.update(meeting.id, {"title": "Updated Title"})
    updated = await repo.get_by_id(meeting.id)
    assert updated.title == "Updated Title"

    # Delete
    await repo.delete(meeting.id)
    with pytest.raises(EntityNotFoundException):
        await repo.get_by_id(meeting.id)

@pytest.mark.asyncio
async def test_cascade_delete(db_session: AsyncSession):
    """Verify that deleting a meeting deletes its associated artifacts."""
    m_repo = MeetingRepository(db_session)
    t_repo = TranscriptRepository(db_session)
    n_repo = NotesRepository(db_session)

    meeting = await m_repo.create(uuid="cascade-test", title="Cascade Lecture")
    await t_repo.create(meeting_id=meeting.id, file_path="/tmp/t.json")
    await n_repo.create(meeting_id=meeting.id, file_path="/tmp/n.json")

    # Delete meeting
    await m_repo.delete(meeting.id)

    # Verify artifacts are gone
    with pytest.raises(EntityNotFoundException):
        await t_repo.get_by_meeting(meeting.id)
    with pytest.raises(EntityNotFoundException):
        await n_repo.get_by_meeting(meeting.id)

@pytest.mark.asyncio
async def test_transaction_rollback(db_session: AsyncSession):
    """Verify that errors cause transaction rollback."""
    m_repo = MeetingRepository(db_session)

    try:
        async with db_session.begin():
            await m_repo.create(uuid="rollback-1", title="Rollback Lecture")
            # Force an error
            raise ValueError("Simulated failure")
    except ValueError:
        pass

    # Verify nothing was persisted
    result = await m_repo.get_by_uuid("rollback-1") # Should raise EntityNotFound
    assert False # if it reaches here it didn't raise
