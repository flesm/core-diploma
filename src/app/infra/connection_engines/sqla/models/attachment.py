from sqlalchemy import Column, DateTime, ForeignKey, String, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from src.app.application.entities.attachment import TaskAttachmentEntity
from src.app.infra.connection_engines.sqla.models.base import Base


class TaskAttachment(Base):
    __tablename__ = "task_attachments"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("uuid_generate_v4()"),
    )
    task_id = Column(UUID(as_uuid=True), ForeignKey("tasks.id"), nullable=False)
    author_id = Column(UUID(as_uuid=True), nullable=False)
    file_ref = Column(String, nullable=False)
    display_name = Column(String, nullable=False)
    source_type = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    def to_entity(self) -> TaskAttachmentEntity:
        return TaskAttachmentEntity(
            id=self.id,
            task_id=self.task_id,
            author_id=self.author_id,
            file_ref=self.file_ref,
            display_name=self.display_name,
            source_type=self.source_type,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
