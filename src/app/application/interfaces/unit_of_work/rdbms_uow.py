from abc import ABC, abstractmethod
from typing import Any, Self

from src.app.application.interfaces.repositories.rdbms.attachment import (
    ITaskAttachmentRepository,
)
from src.app.application.interfaces.repositories.rdbms.comment import (
    ITaskCommentRepository,
)
from src.app.application.interfaces.repositories.rdbms.link import (
    IMentorInternLinkRepository,
    ITaskLinkRepository,
)
from src.app.application.interfaces.repositories.rdbms.status import (
    ITaskStatusRepository,
)
from src.app.application.interfaces.repositories.rdbms.task import ITaskRepository


class IUnitOfWork(ABC):
    def __call__(self, *args: Any, **kwargs: Any) -> Self:
        return self

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
        self, exc_type: type[BaseException] | None, *args: Any, **kwargs: Any
    ) -> None:
        if exc_type is not None:
            await self.rollback()
        else:
            await self.commit()

        await self.shutdown()

    @property
    @abstractmethod
    def mentor_intern_links(self) -> IMentorInternLinkRepository: ...

    @property
    @abstractmethod
    def task_statuses(self) -> ITaskStatusRepository: ...

    @property
    @abstractmethod
    def tasks(self) -> ITaskRepository: ...

    @property
    @abstractmethod
    def task_comments(self) -> ITaskCommentRepository: ...

    @property
    @abstractmethod
    def task_links(self) -> ITaskLinkRepository: ...

    @property
    @abstractmethod
    def task_attachments(self) -> ITaskAttachmentRepository: ...

    @abstractmethod
    async def commit(self) -> None: ...

    @abstractmethod
    async def rollback(self) -> None: ...

    @abstractmethod
    async def shutdown(self) -> None: ...
