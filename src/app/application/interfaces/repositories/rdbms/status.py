from abc import ABC, abstractmethod
from uuid import UUID

from src.app.application.entities.status import TaskStatusEntity


class ITaskStatusRepository(ABC):
    @abstractmethod
    async def create(
        self,
        name: str,
        code: str,
        order_index: int,
        is_default: bool,
        is_system: bool,
        created_by: UUID | None,
    ) -> TaskStatusEntity: ...

    @abstractmethod
    async def get_by_id(self, status_id: UUID) -> TaskStatusEntity | None: ...

    @abstractmethod
    async def get_by_code(self, code: str) -> TaskStatusEntity | None: ...

    @abstractmethod
    async def list_all(self) -> list[TaskStatusEntity]: ...

    @abstractmethod
    async def update(
        self,
        status_id: UUID,
        *,
        name: str,
        code: str,
        order_index: int,
        is_default: bool,
    ) -> TaskStatusEntity | None: ...

    @abstractmethod
    async def delete(self, status_id: UUID) -> None: ...
