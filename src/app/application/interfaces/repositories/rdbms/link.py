from abc import ABC, abstractmethod
from uuid import UUID

from src.app.application.entities.link import MentorInternLinkEntity, TaskLinkEntity


class IMentorInternLinkRepository(ABC):
    @abstractmethod
    async def create(
        self, mentor_id: UUID, intern_id: UUID
    ) -> MentorInternLinkEntity: ...

    @abstractmethod
    async def get_by_id(self, link_id: UUID) -> MentorInternLinkEntity | None: ...

    @abstractmethod
    async def get_by_intern(
        self, intern_id: UUID
    ) -> MentorInternLinkEntity | None: ...

    @abstractmethod
    async def list_by_mentor(
        self, mentor_id: UUID
    ) -> list[MentorInternLinkEntity]: ...

    @abstractmethod
    async def delete(self, link_id: UUID) -> None: ...


class ITaskLinkRepository(ABC):
    @abstractmethod
    async def create(
        self, task_id: UUID, author_id: UUID, url: str, title: str
    ) -> TaskLinkEntity: ...

    @abstractmethod
    async def get_by_id(self, link_id: UUID) -> TaskLinkEntity | None: ...

    @abstractmethod
    async def list_by_task(self, task_id: UUID) -> list[TaskLinkEntity]: ...

    @abstractmethod
    async def update(
        self, link_id: UUID, url: str, title: str
    ) -> TaskLinkEntity | None: ...

    @abstractmethod
    async def delete(self, link_id: UUID) -> None: ...
