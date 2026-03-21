from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.application.entities.attachment import TaskAttachmentEntity
from src.app.application.interfaces.repositories.rdbms.attachment import (
    ITaskAttachmentRepository,
)
from src.app.infra.connection_engines.sqla.models.attachment import TaskAttachment


class SQLATaskAttachmentRepository(ITaskAttachmentRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(
        self,
        task_id: UUID,
        author_id: UUID,
        file_ref: str,
        display_name: str,
        source_type: str,
    ) -> TaskAttachmentEntity:
        attachment = TaskAttachment(
            task_id=task_id,
            author_id=author_id,
            file_ref=file_ref,
            display_name=display_name,
            source_type=source_type,
        )
        self._session.add(attachment)
        await self._session.flush()
        await self._session.refresh(attachment)
        return attachment.to_entity()

    async def get_by_id(
        self, attachment_id: UUID
    ) -> TaskAttachmentEntity | None:
        result = await self._session.execute(
            select(TaskAttachment).where(TaskAttachment.id == attachment_id)
        )
        attachment = result.scalar_one_or_none()
        return attachment.to_entity() if attachment else None

    async def list_by_task(self, task_id: UUID) -> list[TaskAttachmentEntity]:
        result = await self._session.execute(
            select(TaskAttachment)
            .where(TaskAttachment.task_id == task_id)
            .order_by(TaskAttachment.created_at.asc())
        )
        return [item.to_entity() for item in result.scalars().all()]

    async def delete(self, attachment_id: UUID) -> None:
        await self._session.execute(
            delete(TaskAttachment).where(TaskAttachment.id == attachment_id)
        )
