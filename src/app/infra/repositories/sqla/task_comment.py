from uuid import UUID

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.application.entities.comment import TaskCommentEntity
from src.app.application.interfaces.repositories.rdbms.comment import (
    ITaskCommentRepository,
)
from src.app.infra.connection_engines.sqla.models.comment import TaskComment


class SQLATaskCommentRepository(ITaskCommentRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(
        self, task_id: UUID, author_id: UUID, content: str
    ) -> TaskCommentEntity:
        comment = TaskComment(
            task_id=task_id,
            author_id=author_id,
            content=content,
        )
        self._session.add(comment)
        await self._session.flush()
        await self._session.refresh(comment)
        return comment.to_entity()

    async def get_by_id(self, comment_id: UUID) -> TaskCommentEntity | None:
        result = await self._session.execute(
            select(TaskComment).where(TaskComment.id == comment_id)
        )
        comment = result.scalar_one_or_none()
        return comment.to_entity() if comment else None

    async def list_by_task(self, task_id: UUID) -> list[TaskCommentEntity]:
        result = await self._session.execute(
            select(TaskComment)
            .where(TaskComment.task_id == task_id)
            .order_by(TaskComment.created_at.asc())
        )
        return [item.to_entity() for item in result.scalars().all()]

    async def update(
        self, comment_id: UUID, content: str
    ) -> TaskCommentEntity | None:
        await self._session.execute(
            update(TaskComment)
            .where(TaskComment.id == comment_id)
            .values(content=content)
        )
        return await self.get_by_id(comment_id)

    async def delete(self, comment_id: UUID) -> None:
        await self._session.execute(
            delete(TaskComment).where(TaskComment.id == comment_id)
        )
