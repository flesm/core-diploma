from sqlalchemy import Column, DateTime, ForeignKey, Text, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from src.app.application.entities.comment import TaskCommentEntity
from src.app.infra.connection_engines.sqla.models.base import Base


class TaskComment(Base):
    __tablename__ = "task_comments"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("uuid_generate_v4()"),
    )
    task_id = Column(UUID(as_uuid=True), ForeignKey("tasks.id"), nullable=False)
    author_id = Column(UUID(as_uuid=True), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    def to_entity(self) -> TaskCommentEntity:
        return TaskCommentEntity(
            id=self.id,
            task_id=self.task_id,
            author_id=self.author_id,
            content=self.content,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
