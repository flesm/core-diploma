from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.app.application.interfaces.unit_of_work.rdbms_uow import IUnitOfWork
from src.app.infra.repositories.sqla.mentor_intern_link import (
    SQLAMentorInternLinkRepository,
)
from src.app.infra.repositories.sqla.task import SQLATaskRepository
from src.app.infra.repositories.sqla.task_attachment import (
    SQLATaskAttachmentRepository,
)
from src.app.infra.repositories.sqla.task_comment import SQLATaskCommentRepository
from src.app.infra.repositories.sqla.task_link import SQLATaskLinkRepository
from src.app.infra.repositories.sqla.task_status import SQLATaskStatusRepository


class SQLAUnitOfWork(IUnitOfWork):
    def __init__(
        self, session_factory: async_sessionmaker[AsyncSession]
    ) -> None:
        self._session_factory = session_factory
        self._session: AsyncSession

    async def __aenter__(self) -> "SQLAUnitOfWork":
        self._session = self._session_factory()
        return await super().__aenter__()

    @property
    def mentor_intern_links(self) -> SQLAMentorInternLinkRepository:
        return SQLAMentorInternLinkRepository(self._session)

    @property
    def task_statuses(self) -> SQLATaskStatusRepository:
        return SQLATaskStatusRepository(self._session)

    @property
    def tasks(self) -> SQLATaskRepository:
        return SQLATaskRepository(self._session)

    @property
    def task_comments(self) -> SQLATaskCommentRepository:
        return SQLATaskCommentRepository(self._session)

    @property
    def task_links(self) -> SQLATaskLinkRepository:
        return SQLATaskLinkRepository(self._session)

    @property
    def task_attachments(self) -> SQLATaskAttachmentRepository:
        return SQLATaskAttachmentRepository(self._session)

    async def commit(self) -> None:
        await self._session.commit()

    async def rollback(self) -> None:
        await self._session.rollback()

    async def shutdown(self) -> None:
        await self._session.close()
