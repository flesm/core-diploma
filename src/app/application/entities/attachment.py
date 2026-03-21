from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class TaskAttachmentEntity:
    id: UUID
    task_id: UUID
    author_id: UUID
    file_ref: str
    display_name: str
    source_type: str
    created_at: datetime
    updated_at: datetime
