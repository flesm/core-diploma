from abc import ABC, abstractmethod
from uuid import UUID

from src.app.application.entities.attachment import TaskAttachmentEntity


class ITaskAttachmentRepository(ABC):
    @abstractmethod
    async def create(
        self,
        task_id: UUID,
        author_id: UUID,
        file_ref: str,
        display_name: str,
        source_type: str,
    ) -> TaskAttachmentEntity: ...

    @abstractmethod
    async def get_by_id(
        self, attachment_id: UUID
    ) -> TaskAttachmentEntity | None: ...

    @abstractmethod
    async def list_by_task(self, task_id: UUID) -> list[TaskAttachmentEntity]: ...

    @abstractmethod
    async def delete(self, attachment_id: UUID) -> None: ...
