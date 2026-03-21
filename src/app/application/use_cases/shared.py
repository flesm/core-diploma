from uuid import UUID

from src.app.application.entities.link import MentorInternLinkEntity
from src.app.application.entities.status import TaskStatusEntity
from src.app.application.entities.task import TaskEntity
from src.app.application.entities.viewer import AuthenticatedUser
from src.app.application.exceptions import (
    BadRequestException,
    ForbiddenException,
    NotFoundException,
)
from src.app.application.interfaces.unit_of_work.rdbms_uow import IUnitOfWork


def normalize_status_code(name: str) -> str:
    return name.strip().upper().replace(" ", "_")


class AccessService:
    def __init__(self, rdbms_uow: IUnitOfWork) -> None:
        self._uow = rdbms_uow

    @staticmethod
    def ensure_mentor(actor: AuthenticatedUser) -> None:
        if not actor.is_mentor:
            raise ForbiddenException("Only mentors can perform this action.")

    async def get_link_for_intern(
        self, intern_id: UUID
    ) -> MentorInternLinkEntity | None:
        return await self._uow.mentor_intern_links.get_by_intern(intern_id)

    async def require_link_for_mentor(
        self, mentor_id: UUID, intern_id: UUID
    ) -> MentorInternLinkEntity:
        link = await self._uow.mentor_intern_links.get_by_intern(intern_id)
        if not link or link.mentor_id != mentor_id:
            raise ForbiddenException("This intern is not assigned to the mentor.")
        return link

    async def require_status(self, status_id: UUID) -> TaskStatusEntity:
        status = await self._uow.task_statuses.get_by_id(status_id)
        if not status:
            raise NotFoundException("Task status not found.")
        return status

    async def get_default_status(self) -> TaskStatusEntity:
        statuses = await self._uow.task_statuses.list_all()
        for status in statuses:
            if status.is_default:
                return status
        raise BadRequestException("Default task status is not configured.")

    async def require_task(self, task_id: UUID) -> TaskEntity:
        task = await self._uow.tasks.get_by_id(task_id)
        if not task:
            raise NotFoundException("Task not found.")
        return task

    async def require_task_access(
        self, actor: AuthenticatedUser, task_id: UUID
    ) -> TaskEntity:
        task = await self.require_task(task_id)
        if actor.is_mentor and task.mentor_id == actor.user_id:
            return task
        if actor.is_intern and task.intern_id == actor.user_id:
            return task
        raise ForbiddenException("You do not have access to this task.")
