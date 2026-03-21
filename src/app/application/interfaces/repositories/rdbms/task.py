from abc import ABC, abstractmethod
from uuid import UUID

from src.app.application.entities.task import TaskEntity


class ITaskRepository(ABC):
    @abstractmethod
    async def create(
        self,
        title: str,
        description: str,
        mentor_id: UUID,
        intern_id: UUID,
        status_id: UUID,
    ) -> TaskEntity: ...

    @abstractmethod
    async def get_by_id(self, task_id: UUID) -> TaskEntity | None: ...

    @abstractmethod
    async def list_for_mentor(
        self,
        mentor_id: UUID,
        intern_id: UUID | None = None,
        status_id: UUID | None = None,
    ) -> list[TaskEntity]: ...

    @abstractmethod
    async def list_for_intern(
        self, intern_id: UUID, status_id: UUID | None = None
    ) -> list[TaskEntity]: ...

    @abstractmethod
    async def update(
        self,
        task_id: UUID,
        *,
        title: str,
        description: str,
        intern_id: UUID,
        status_id: UUID,
    ) -> TaskEntity | None: ...

    @abstractmethod
    async def delete(self, task_id: UUID) -> None: ...
