from uuid import UUID

from src.app.application.entities.attachment import TaskAttachmentEntity
from src.app.application.entities.viewer import AuthenticatedUser
from src.app.application.exceptions import ForbiddenException, NotFoundException
from src.app.application.interfaces.unit_of_work.rdbms_uow import IUnitOfWork
from src.app.application.use_cases.shared import AccessService


class TaskAttachmentService(AccessService):
    def __init__(self, rdbms_uow: IUnitOfWork) -> None:
        super().__init__(rdbms_uow)

    async def list(
        self, actor: AuthenticatedUser, task_id: UUID
    ) -> list[TaskAttachmentEntity]:
        async with self._uow():
            await self.require_task_access(actor, task_id)
            return await self._uow.task_attachments.list_by_task(task_id)

    async def create(
        self,
        actor: AuthenticatedUser,
        task_id: UUID,
        file_ref: str,
        display_name: str,
        source_type: str,
    ) -> TaskAttachmentEntity:
        async with self._uow():
            await self.require_task_access(actor, task_id)
            return await self._uow.task_attachments.create(
                task_id=task_id,
                author_id=actor.user_id,
                file_ref=file_ref,
                display_name=display_name,
                source_type=source_type,
            )

    async def delete(
        self, actor: AuthenticatedUser, task_id: UUID, attachment_id: UUID
    ) -> None:
        async with self._uow():
            await self.require_task_access(actor, task_id)
            attachment = await self._uow.task_attachments.get_by_id(attachment_id)
            if not attachment or attachment.task_id != task_id:
                raise NotFoundException("Attachment not found.")
            if attachment.author_id != actor.user_id and not actor.is_mentor:
                raise ForbiddenException(
                    "You can delete only your own attachments."
                )
            await self._uow.task_attachments.delete(attachment_id)
