from uuid import UUID

from src.app.application.entities.status import TaskStatusEntity
from src.app.application.entities.viewer import AuthenticatedUser
from src.app.application.exceptions import BadRequestException, ForbiddenException, NotFoundException
from src.app.application.interfaces.unit_of_work.rdbms_uow import IUnitOfWork
from src.app.application.use_cases.shared import AccessService, normalize_status_code


class TaskStatusService(AccessService):
    def __init__(self, rdbms_uow: IUnitOfWork) -> None:
        super().__init__(rdbms_uow)

    async def list_all(self, actor: AuthenticatedUser) -> list[TaskStatusEntity]:
        async with self._uow():
            return await self._uow.task_statuses.list_all()

    async def create(
        self,
        actor: AuthenticatedUser,
        name: str,
        code: str | None,
        order_index: int,
        is_default: bool,
    ) -> TaskStatusEntity:
        self.ensure_mentor(actor)
        status_code = normalize_status_code(code or name)
        async with self._uow():
            existing = await self._uow.task_statuses.get_by_code(status_code)
            if existing:
                raise BadRequestException("Task status code already exists.")
            return await self._uow.task_statuses.create(
                name=name,
                code=status_code,
                order_index=order_index,
                is_default=is_default,
                is_system=False,
                created_by=actor.user_id,
            )

    async def update(
        self,
        actor: AuthenticatedUser,
        status_id: UUID,
        name: str,
        code: str | None,
        order_index: int,
        is_default: bool,
    ) -> TaskStatusEntity:
        self.ensure_mentor(actor)
        status_code = normalize_status_code(code or name)
        async with self._uow():
            status = await self._uow.task_statuses.get_by_id(status_id)
            if not status:
                raise NotFoundException("Task status not found.")
            if status.is_system:
                raise ForbiddenException("System statuses cannot be modified.")
            if status.created_by != actor.user_id:
                raise ForbiddenException("Only the author can update this status.")

            existing = await self._uow.task_statuses.get_by_code(status_code)
            if existing and existing.id != status_id:
                raise BadRequestException("Task status code already exists.")

            updated = await self._uow.task_statuses.update(
                status_id,
                name=name,
                code=status_code,
                order_index=order_index,
                is_default=is_default,
            )
            if not updated:
                raise NotFoundException("Task status not found.")
            return updated

    async def delete(self, actor: AuthenticatedUser, status_id: UUID) -> None:
        self.ensure_mentor(actor)
        async with self._uow():
            status = await self._uow.task_statuses.get_by_id(status_id)
            if not status:
                raise NotFoundException("Task status not found.")
            if status.is_system:
                raise ForbiddenException("System statuses cannot be deleted.")
            if status.created_by != actor.user_id:
                raise ForbiddenException("Only the author can delete this status.")
            await self._uow.task_statuses.delete(status_id)
