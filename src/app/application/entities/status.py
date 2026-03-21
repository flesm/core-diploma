from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class TaskStatusEntity:
    id: UUID
    name: str
    code: str
    order_index: int
    is_default: bool
    is_system: bool
    created_by: UUID | None
    created_at: datetime
    updated_at: datetime
