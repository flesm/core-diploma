from uuid import UUID

from src.app.application.entities.link import TaskLinkEntity
from src.app.application.entities.viewer import AuthenticatedUser
from src.app.application.exceptions import ForbiddenException, NotFoundException
from src.app.application.interfaces.unit_of_work.rdbms_uow import IUnitOfWork
from src.app.application.use_cases.shared import AccessService


class TaskLinkService(AccessService):
    def __init__(self, rdbms_uow: IUnitOfWork) -> None:
        super().__init__(rdbms_uow)

    async def list(self, actor: AuthenticatedUser, task_id: UUID) -> list[TaskLinkEntity]:
        async with self._uow():
            await self.require_task_access(actor, task_id)
            return await self._uow.task_links.list_by_task(task_id)

    async def create(
        self, actor: AuthenticatedUser, task_id: UUID, url: str, title: str
    ) -> TaskLinkEntity:
        async with self._uow():
            await self.require_task_access(actor, task_id)
            return await self._uow.task_links.create(
                task_id=task_id,
                author_id=actor.user_id,
                url=url,
                title=title,
            )

    async def update(
        self,
        actor: AuthenticatedUser,
        task_id: UUID,
        link_id: UUID,
        url: str,
        title: str,
    ) -> TaskLinkEntity:
        async with self._uow():
            await self.require_task_access(actor, task_id)
            link = await self._uow.task_links.get_by_id(link_id)
            if not link or link.task_id != task_id:
                raise NotFoundException("Link not found.")
            if link.author_id != actor.user_id:
                raise ForbiddenException("You can edit only your own links.")
            updated = await self._uow.task_links.update(link_id, url, title)
            if not updated:
                raise NotFoundException("Link not found.")
            return updated

    async def delete(
        self, actor: AuthenticatedUser, task_id: UUID, link_id: UUID
    ) -> None:
        async with self._uow():
            await self.require_task_access(actor, task_id)
            link = await self._uow.task_links.get_by_id(link_id)
            if not link or link.task_id != task_id:
                raise NotFoundException("Link not found.")
            if link.author_id != actor.user_id:
                raise ForbiddenException("You can delete only your own links.")
            await self._uow.task_links.delete(link_id)
