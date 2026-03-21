from uuid import UUID

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.application.entities.link import TaskLinkEntity
from src.app.application.interfaces.repositories.rdbms.link import ITaskLinkRepository
from src.app.infra.connection_engines.sqla.models.link import TaskLink


class SQLATaskLinkRepository(ITaskLinkRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(
        self, task_id: UUID, author_id: UUID, url: str, title: str
    ) -> TaskLinkEntity:
        link = TaskLink(task_id=task_id, author_id=author_id, url=url, title=title)
        self._session.add(link)
        await self._session.flush()
        await self._session.refresh(link)
        return link.to_entity()

    async def get_by_id(self, link_id: UUID) -> TaskLinkEntity | None:
        result = await self._session.execute(
            select(TaskLink).where(TaskLink.id == link_id)
        )
        link = result.scalar_one_or_none()
        return link.to_entity() if link else None

    async def list_by_task(self, task_id: UUID) -> list[TaskLinkEntity]:
        result = await self._session.execute(
            select(TaskLink)
            .where(TaskLink.task_id == task_id)
            .order_by(TaskLink.created_at.asc())
        )
        return [item.to_entity() for item in result.scalars().all()]

    async def update(
        self, link_id: UUID, url: str, title: str
    ) -> TaskLinkEntity | None:
        await self._session.execute(
            update(TaskLink)
            .where(TaskLink.id == link_id)
            .values(url=url, title=title)
        )
        return await self.get_by_id(link_id)

    async def delete(self, link_id: UUID) -> None:
        await self._session.execute(delete(TaskLink).where(TaskLink.id == link_id))
