from datetime import datetime
from typing import Self
from uuid import UUID

from pydantic import BaseModel, HttpUrl

from src.app.application.entities.attachment import TaskAttachmentEntity
from src.app.application.entities.comment import TaskCommentEntity
from src.app.application.entities.link import MentorInternLinkEntity, TaskLinkEntity
from src.app.application.entities.status import TaskStatusEntity
from src.app.application.entities.task import TaskEntity
from src.app.application.use_cases.tasks.service import TaskBoardColumn


class MentorInternLinkCreateViewModel(BaseModel):
    intern_id: UUID


class MentorInternLinkResponseViewModel(BaseModel):
    id: UUID
    mentor_id: UUID
    intern_id: UUID
    created_at: datetime

    @classmethod
    def from_entity(cls, entity: MentorInternLinkEntity) -> Self:
        return cls(**entity.__dict__)


class TaskStatusCreateViewModel(BaseModel):
    name: str
    code: str | None = None
    order_index: int
    is_default: bool = False


class TaskStatusResponseViewModel(BaseModel):
    id: UUID
    name: str
    code: str
    order_index: int
    is_default: bool
    is_system: bool
    created_by: UUID | None
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_entity(cls, entity: TaskStatusEntity) -> Self:
        return cls(**entity.__dict__)


class TaskCreateViewModel(BaseModel):
    title: str
    description: str
    intern_id: UUID
    status_id: UUID | None = None


class TaskUpdateViewModel(BaseModel):
    title: str
    description: str
    status_id: UUID
    intern_id: UUID | None = None


class TaskResponseViewModel(BaseModel):
    id: UUID
    title: str
    description: str
    mentor_id: UUID
    intern_id: UUID
    status_id: UUID
    created_at: datetime
    updated_at: datetime
    status: TaskStatusResponseViewModel | None = None

    @classmethod
    def from_entity(cls, entity: TaskEntity) -> Self:
        return cls(
            id=entity.id,
            title=entity.title,
            description=entity.description,
            mentor_id=entity.mentor_id,
            intern_id=entity.intern_id,
            status_id=entity.status_id,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            status=TaskStatusResponseViewModel.from_entity(entity.status)
            if entity.status
            else None,
        )


class TaskBoardColumnResponseViewModel(BaseModel):
    status: TaskStatusResponseViewModel
    tasks: list[TaskResponseViewModel]

    @classmethod
    def from_entity(cls, entity: TaskBoardColumn) -> Self:
        return cls(
            status=TaskStatusResponseViewModel.from_entity(entity.status),
            tasks=[TaskResponseViewModel.from_entity(task) for task in entity.tasks],
        )


class TaskCommentCreateViewModel(BaseModel):
    content: str


class TaskCommentResponseViewModel(BaseModel):
    id: UUID
    task_id: UUID
    author_id: UUID
    content: str
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_entity(cls, entity: TaskCommentEntity) -> Self:
        return cls(**entity.__dict__)


class TaskLinkCreateViewModel(BaseModel):
    url: HttpUrl
    title: str


class TaskLinkResponseViewModel(BaseModel):
    id: UUID
    task_id: UUID
    author_id: UUID
    url: str
    title: str
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_entity(cls, entity: TaskLinkEntity) -> Self:
        return cls(**entity.__dict__)


class TaskAttachmentCreateViewModel(BaseModel):
    file_ref: str
    display_name: str
    source_type: str


class TaskAttachmentResponseViewModel(BaseModel):
    id: UUID
    task_id: UUID
    author_id: UUID
    file_ref: str
    display_name: str
    source_type: str
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_entity(cls, entity: TaskAttachmentEntity) -> Self:
        return cls(**entity.__dict__)
