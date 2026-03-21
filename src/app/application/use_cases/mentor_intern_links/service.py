from uuid import UUID

from src.app.application.entities.link import MentorInternLinkEntity
from src.app.application.entities.viewer import AuthenticatedUser
from src.app.application.exceptions import (
    BadRequestException,
    ForbiddenException,
    NotFoundException,
)
from src.app.application.interfaces.unit_of_work.rdbms_uow import IUnitOfWork
from src.app.application.use_cases.shared import AccessService


class MentorInternLinkService(AccessService):
    def __init__(self, rdbms_uow: IUnitOfWork) -> None:
        super().__init__(rdbms_uow)

    async def create(
        self, actor: AuthenticatedUser, intern_id: UUID
    ) -> MentorInternLinkEntity:
        self.ensure_mentor(actor)
        async with self._uow():
            existing = await self._uow.mentor_intern_links.get_by_intern(intern_id)
            if existing:
                raise BadRequestException("Intern is already assigned to a mentor.")
            return await self._uow.mentor_intern_links.create(
                mentor_id=actor.user_id,
                intern_id=intern_id,
            )

    async def list_my_interns(
        self, actor: AuthenticatedUser
    ) -> list[MentorInternLinkEntity]:
        self.ensure_mentor(actor)
        async with self._uow():
            return await self._uow.mentor_intern_links.list_by_mentor(actor.user_id)

    async def get_my_mentor(
        self, actor: AuthenticatedUser
    ) -> MentorInternLinkEntity:
        async with self._uow():
            link = await self._uow.mentor_intern_links.get_by_intern(actor.user_id)
            if not link:
                raise NotFoundException("Mentor is not assigned for this intern.")
            return link

    async def get_by_id(
        self, actor: AuthenticatedUser, link_id: UUID
    ) -> MentorInternLinkEntity:
        async with self._uow():
            link = await self._uow.mentor_intern_links.get_by_id(link_id)
            if not link:
                raise NotFoundException("Mentor-intern link not found.")
            if actor.is_mentor and link.mentor_id == actor.user_id:
                return link
            if actor.is_intern and link.intern_id == actor.user_id:
                return link
            raise ForbiddenException("You cannot view this mentor-intern link.")

    async def delete(self, actor: AuthenticatedUser, link_id: UUID) -> None:
        self.ensure_mentor(actor)
        async with self._uow():
            link = await self._uow.mentor_intern_links.get_by_id(link_id)
            if not link:
                raise NotFoundException("Mentor-intern link not found.")
            if link.mentor_id != actor.user_id:
                raise BadRequestException("You can delete only your own intern links.")
            await self._uow.mentor_intern_links.delete(link_id)
