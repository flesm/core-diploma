from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID

from src.app.application.entities.attachment import TaskAttachmentEntity
from src.app.application.entities.comment import TaskCommentEntity
from src.app.application.entities.link import TaskLinkEntity
from src.app.application.entities.status import TaskStatusEntity


@dataclass
class TaskEntity:
    id: UUID
    title: str
    description: str
    mentor_id: UUID
    intern_id: UUID
    status_id: UUID
    created_at: datetime
    updated_at: datetime
    status: TaskStatusEntity | None = None
    comments: list[TaskCommentEntity] = field(default_factory=list)
    links: list[TaskLinkEntity] = field(default_factory=list)
    attachments: list[TaskAttachmentEntity] = field(default_factory=list)
