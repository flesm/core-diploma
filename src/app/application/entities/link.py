from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class MentorInternLinkEntity:
    id: UUID
    mentor_id: UUID
    intern_id: UUID
    created_at: datetime


@dataclass
class TaskLinkEntity:
    id: UUID
    task_id: UUID
    author_id: UUID
    url: str
    title: str
    created_at: datetime
    updated_at: datetime
