from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.application.entities.link import MentorInternLinkEntity
from src.app.application.interfaces.repositories.rdbms.link import (
    IMentorInternLinkRepository,
)
from src.app.infra.connection_engines.sqla.models.link import MentorInternLink


class SQLAMentorInternLinkRepository(IMentorInternLinkRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(
        self, mentor_id: UUID, intern_id: UUID
    ) -> MentorInternLinkEntity:
        link = MentorInternLink(mentor_id=mentor_id, intern_id=intern_id)
        self._session.add(link)
        await self._session.flush()
        await self._session.refresh(link)
        return link.to_entity()

    async def get_by_id(self, link_id: UUID) -> MentorInternLinkEntity | None:
        result = await self._session.execute(
            select(MentorInternLink).where(MentorInternLink.id == link_id)
        )
        link = result.scalar_one_or_none()
        return link.to_entity() if link else None

    async def get_by_intern(
        self, intern_id: UUID
    ) -> MentorInternLinkEntity | None:
        result = await self._session.execute(
            select(MentorInternLink).where(
                MentorInternLink.intern_id == intern_id
            )
        )
        link = result.scalar_one_or_none()
        return link.to_entity() if link else None

    async def list_by_mentor(
        self, mentor_id: UUID
    ) -> list[MentorInternLinkEntity]:
        result = await self._session.execute(
            select(MentorInternLink).where(
                MentorInternLink.mentor_id == mentor_id
            )
        )
        return [item.to_entity() for item in result.scalars().all()]

    async def delete(self, link_id: UUID) -> None:
        await self._session.execute(
            delete(MentorInternLink).where(MentorInternLink.id == link_id)
        )
