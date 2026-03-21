from uuid import UUID

from src.app.application.entities.comment import TaskCommentEntity
from src.app.application.entities.viewer import AuthenticatedUser
from src.app.application.exceptions import ForbiddenException, NotFoundException
from src.app.application.interfaces.unit_of_work.rdbms_uow import IUnitOfWork
from src.app.application.use_cases.shared import AccessService


class TaskCommentService(AccessService):
    def __init__(self, rdbms_uow: IUnitOfWork) -> None:
        super().__init__(rdbms_uow)

    async def list(self, actor: AuthenticatedUser, task_id: UUID) -> list[TaskCommentEntity]:
        async with self._uow():
            await self.require_task_access(actor, task_id)
            return await self._uow.task_comments.list_by_task(task_id)

    async def create(
        self, actor: AuthenticatedUser, task_id: UUID, content: str
    ) -> TaskCommentEntity:
        async with self._uow():
            await self.require_task_access(actor, task_id)
            return await self._uow.task_comments.create(
                task_id=task_id,
                author_id=actor.user_id,
                content=content,
            )

    async def update(
        self, actor: AuthenticatedUser, task_id: UUID, comment_id: UUID, content: str
    ) -> TaskCommentEntity:
        async with self._uow():
            await self.require_task_access(actor, task_id)
            comment = await self._uow.task_comments.get_by_id(comment_id)
            if not comment or comment.task_id != task_id:
                raise NotFoundException("Comment not found.")
            if comment.author_id != actor.user_id:
                raise ForbiddenException("You can edit only your own comments.")
            updated = await self._uow.task_comments.update(comment_id, content)
            if not updated:
                raise NotFoundException("Comment not found.")
            return updated

    async def delete(
        self, actor: AuthenticatedUser, task_id: UUID, comment_id: UUID
    ) -> None:
        async with self._uow():
            await self.require_task_access(actor, task_id)
            comment = await self._uow.task_comments.get_by_id(comment_id)
            if not comment or comment.task_id != task_id:
                raise NotFoundException("Comment not found.")
            if comment.author_id != actor.user_id:
                raise ForbiddenException("You can delete only your own comments.")
            await self._uow.task_comments.delete(comment_id)
