from abc import ABC, abstractmethod
from uuid import UUID

from src.app.application.entities.comment import TaskCommentEntity


class ITaskCommentRepository(ABC):
    @abstractmethod
    async def create(
        self, task_id: UUID, author_id: UUID, content: str
    ) -> TaskCommentEntity: ...

    @abstractmethod
    async def get_by_id(self, comment_id: UUID) -> TaskCommentEntity | None: ...

    @abstractmethod
    async def list_by_task(self, task_id: UUID) -> list[TaskCommentEntity]: ...

    @abstractmethod
    async def update(
        self, comment_id: UUID, content: str
    ) -> TaskCommentEntity | None: ...

    @abstractmethod
    async def delete(self, comment_id: UUID) -> None: ...
