from dataclasses import dataclass
from uuid import UUID

from src.app.application.entities.status import TaskStatusEntity
from src.app.application.entities.task import TaskEntity
from src.app.application.entities.viewer import AuthenticatedUser
from src.app.application.exceptions import ForbiddenException
from src.app.application.interfaces.unit_of_work.rdbms_uow import IUnitOfWork
from src.app.application.use_cases.shared import AccessService


@dataclass
class TaskBoardColumn:
    status: TaskStatusEntity
    tasks: list[TaskEntity]


class TaskService(AccessService):
    def __init__(self, rdbms_uow: IUnitOfWork) -> None:
        super().__init__(rdbms_uow)

    async def create(
        self,
        actor: AuthenticatedUser,
        title: str,
        description: str,
        intern_id: UUID,
        status_id: UUID | None,
    ) -> TaskEntity:
        self.ensure_mentor(actor)
        async with self._uow():
            await self.require_link_for_mentor(actor.user_id, intern_id)
            status = (
                await self.require_status(status_id)
                if status_id
                else await self.get_default_status()
            )
            return await self._uow.tasks.create(
                title=title,
                description=description,
                mentor_id=actor.user_id,
                intern_id=intern_id,
                status_id=status.id,
            )

    async def list_tasks(
        self,
        actor: AuthenticatedUser,
        intern_id: UUID | None,
        status_id: UUID | None,
    ) -> list[TaskEntity]:
        async with self._uow():
            if actor.is_mentor:
                return await self._uow.tasks.list_for_mentor(
                    actor.user_id, intern_id=intern_id, status_id=status_id
                )
            return await self._uow.tasks.list_for_intern(
                actor.user_id, status_id=status_id
            )

    async def get(self, actor: AuthenticatedUser, task_id: UUID) -> TaskEntity:
        async with self._uow():
            return await self.require_task_access(actor, task_id)

    async def update(
        self,
        actor: AuthenticatedUser,
        task_id: UUID,
        title: str,
        description: str,
        intern_id: UUID | None,
        status_id: UUID,
    ) -> TaskEntity:
        async with self._uow():
            task = await self.require_task_access(actor, task_id)
            await self.require_status(status_id)

            next_intern_id = task.intern_id
            if actor.is_mentor:
                if intern_id is not None:
                    await self.require_link_for_mentor(actor.user_id, intern_id)
                    next_intern_id = intern_id
            else:
                if intern_id and intern_id != task.intern_id:
                    raise ForbiddenException("Intern cannot reassign tasks.")
                if task.intern_id != actor.user_id:
                    raise ForbiddenException("You can update only your own task.")

            updated = await self._uow.tasks.update(
                task_id,
                title=title,
                description=description,
                intern_id=next_intern_id,
                status_id=status_id,
            )
            if not updated:
                raise ForbiddenException("Task could not be updated.")
            return updated

    async def delete(self, actor: AuthenticatedUser, task_id: UUID) -> None:
        self.ensure_mentor(actor)
        async with self._uow():
            task = await self.require_task(task_id)
            if task.mentor_id != actor.user_id:
                raise ForbiddenException("You can delete only your own tasks.")
            await self._uow.tasks.delete(task_id)

    async def board(
        self,
        actor: AuthenticatedUser,
        intern_id: UUID | None,
        status_id: UUID | None,
    ) -> list[TaskBoardColumn]:
        async with self._uow():
            statuses = await self._uow.task_statuses.list_all()
            tasks = (
                await self._uow.tasks.list_for_mentor(
                    actor.user_id, intern_id=intern_id, status_id=status_id
                )
                if actor.is_mentor
                else await self._uow.tasks.list_for_intern(
                    actor.user_id, status_id=status_id
                )
            )
            grouped: dict[UUID, list[TaskEntity]] = {status.id: [] for status in statuses}
            for task in tasks:
                grouped.setdefault(task.status_id, []).append(task)
            return [
                TaskBoardColumn(status=status, tasks=grouped.get(status.id, []))
                for status in statuses
            ]
