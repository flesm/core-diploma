from sqlalchemy import Boolean, Column, DateTime, Integer, String, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from src.app.application.entities.status import TaskStatusEntity
from src.app.infra.connection_engines.sqla.models.base import Base


class TaskStatus(Base):
    __tablename__ = "task_statuses"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("uuid_generate_v4()"),
    )
    name = Column(String, nullable=False)
    code = Column(String, unique=True, nullable=False)
    order_index = Column(Integer, nullable=False)
    is_default = Column(Boolean, nullable=False, server_default=text("false"))
    is_system = Column(Boolean, nullable=False, server_default=text("false"))
    created_by = Column(UUID(as_uuid=True), nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    def to_entity(self) -> TaskStatusEntity:
        return TaskStatusEntity(
            id=self.id,
            name=self.name,
            code=self.code,
            order_index=self.order_index,
            is_default=self.is_default,
            is_system=self.is_system,
            created_by=self.created_by,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
