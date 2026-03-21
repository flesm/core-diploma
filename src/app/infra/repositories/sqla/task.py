from uuid import UUID

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.application.entities.task import TaskEntity
from src.app.application.interfaces.repositories.rdbms.task import ITaskRepository
from src.app.infra.connection_engines.sqla.models.task import Task


class SQLATaskRepository(ITaskRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(
        self,
        title: str,
        description: str,
        mentor_id: UUID,
        intern_id: UUID,
        status_id: UUID,
    ) -> TaskEntity:
        task = Task(
            title=title,
            description=description,
            mentor_id=mentor_id,
            intern_id=intern_id,
            status_id=status_id,
        )
        self._session.add(task)
        await self._session.flush()
        await self._session.refresh(task)
        return task.to_entity()

    async def get_by_id(self, task_id: UUID) -> TaskEntity | None:
        result = await self._session.execute(select(Task).where(Task.id == task_id))
        task = result.scalar_one_or_none()
        return task.to_entity() if task else None

    async def list_for_mentor(
        self,
        mentor_id: UUID,
        intern_id: UUID | None = None,
        status_id: UUID | None = None,
    ) -> list[TaskEntity]:
        query = select(Task).where(Task.mentor_id == mentor_id)
        if intern_id:
            query = query.where(Task.intern_id == intern_id)
        if status_id:
            query = query.where(Task.status_id == status_id)
        query = query.order_by(Task.created_at.desc())
        result = await self._session.execute(query)
        return [task.to_entity() for task in result.scalars().all()]

    async def list_for_intern(
        self, intern_id: UUID, status_id: UUID | None = None
    ) -> list[TaskEntity]:
        query = select(Task).where(Task.intern_id == intern_id)
        if status_id:
            query = query.where(Task.status_id == status_id)
        query = query.order_by(Task.created_at.desc())
        result = await self._session.execute(query)
        return [task.to_entity() for task in result.scalars().all()]

    async def update(
        self,
        task_id: UUID,
        *,
        title: str,
        description: str,
        intern_id: UUID,
        status_id: UUID,
    ) -> TaskEntity | None:
        await self._session.execute(
            update(Task)
            .where(Task.id == task_id)
            .values(
                title=title,
                description=description,
                intern_id=intern_id,
                status_id=status_id,
            )
        )
        return await self.get_by_id(task_id)

    async def delete(self, task_id: UUID) -> None:
        await self._session.execute(delete(Task).where(Task.id == task_id))
