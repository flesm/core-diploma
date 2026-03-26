from datetime import datetime
from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from src.app.application.entities.link import MentorInternLinkEntity
from src.app.application.entities.status import TaskStatusEntity
from src.app.application.entities.task import TaskEntity
from src.app.application.entities.viewer import AuthenticatedUser


class FakeUnitOfWork:
    def __init__(self) -> None:
        self.mentor_intern_links = SimpleNamespace(
            get_by_intern=AsyncMock(),
            list_by_mentor=AsyncMock(),
        )
        self.task_statuses = SimpleNamespace(
            get_by_id=AsyncMock(),
            get_by_code=AsyncMock(),
            list_all=AsyncMock(),
            create=AsyncMock(),
            update=AsyncMock(),
            delete=AsyncMock(),
        )
        self.tasks = SimpleNamespace(
            create=AsyncMock(),
            get_by_id=AsyncMock(),
            list_for_mentor=AsyncMock(),
            list_for_intern=AsyncMock(),
            update=AsyncMock(),
            delete=AsyncMock(),
        )
        self.task_comments = SimpleNamespace()
        self.task_links = SimpleNamespace()
        self.task_attachments = SimpleNamespace()
        self.commit = AsyncMock()
        self.rollback = AsyncMock()
        self.shutdown = AsyncMock()

    def __call__(self, *args, **kwargs):
        return self

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, *args, **kwargs):
        if exc_type is not None:
            await self.rollback()
        else:
            await self.commit()
        await self.shutdown()


@pytest.fixture
def mentor_user() -> AuthenticatedUser:
    return AuthenticatedUser(
        user_id=uuid4(),
        email="mentor@example.com",
        role="mentor",
        is_staff=False,
    )


@pytest.fixture
def intern_user() -> AuthenticatedUser:
    return AuthenticatedUser(
        user_id=uuid4(),
        email="intern@example.com",
        role="intern",
        is_staff=False,
    )


@pytest.fixture
def task_status(mentor_user: AuthenticatedUser) -> TaskStatusEntity:
    now = datetime.utcnow()
    return TaskStatusEntity(
        id=uuid4(),
        name="To do",
        code="TO_DO",
        order_index=1,
        is_default=True,
        is_system=False,
        created_by=mentor_user.user_id,
        created_at=now,
        updated_at=now,
    )


@pytest.fixture
def mentor_intern_link(
    mentor_user: AuthenticatedUser,
    intern_user: AuthenticatedUser,
) -> MentorInternLinkEntity:
    return MentorInternLinkEntity(
        id=uuid4(),
        mentor_id=mentor_user.user_id,
        intern_id=intern_user.user_id,
        created_at=datetime.utcnow(),
    )


@pytest.fixture
def task_entity(
    mentor_user: AuthenticatedUser,
    intern_user: AuthenticatedUser,
    task_status: TaskStatusEntity,
) -> TaskEntity:
    now = datetime.utcnow()
    return TaskEntity(
        id=uuid4(),
        title="Prepare roadmap",
        description="Draft internship plan",
        mentor_id=mentor_user.user_id,
        intern_id=intern_user.user_id,
        status_id=task_status.id,
        created_at=now,
        updated_at=now,
        status=task_status,
    )


@pytest.fixture
def fake_uow() -> FakeUnitOfWork:
    return FakeUnitOfWork()
