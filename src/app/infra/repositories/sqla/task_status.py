from uuid import UUID

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.application.entities.status import TaskStatusEntity
from src.app.application.interfaces.repositories.rdbms.status import (
    ITaskStatusRepository,
)
from src.app.infra.connection_engines.sqla.models.status import TaskStatus


class SQLATaskStatusRepository(ITaskStatusRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(
        self,
        name: str,
        code: str,
        order_index: int,
        is_default: bool,
        is_system: bool,
        created_by: UUID | None,
    ) -> TaskStatusEntity:
        status = TaskStatus(
            name=name,
            code=code,
            order_index=order_index,
            is_default=is_default,
            is_system=is_system,
            created_by=created_by,
        )
        self._session.add(status)
        await self._session.flush()
        await self._session.refresh(status)
        return status.to_entity()

    async def get_by_id(self, status_id: UUID) -> TaskStatusEntity | None:
        result = await self._session.execute(
            select(TaskStatus).where(TaskStatus.id == status_id)
        )
        status = result.scalar_one_or_none()
        return status.to_entity() if status else None

    async def get_by_code(self, code: str) -> TaskStatusEntity | None:
        result = await self._session.execute(
            select(TaskStatus).where(TaskStatus.code == code)
        )
        status = result.scalar_one_or_none()
        return status.to_entity() if status else None

    async def list_all(self) -> list[TaskStatusEntity]:
        result = await self._session.execute(
            select(TaskStatus).order_by(TaskStatus.order_index, TaskStatus.name)
        )
        return [item.to_entity() for item in result.scalars().all()]

    async def update(
        self,
        status_id: UUID,
        *,
        name: str,
        code: str,
        order_index: int,
        is_default: bool,
    ) -> TaskStatusEntity | None:
        await self._session.execute(
            update(TaskStatus)
            .where(TaskStatus.id == status_id)
            .values(
                name=name,
                code=code,
                order_index=order_index,
                is_default=is_default,
            )
        )
        return await self.get_by_id(status_id)

    async def delete(self, status_id: UUID) -> None:
        await self._session.execute(
            delete(TaskStatus).where(TaskStatus.id == status_id)
        )
