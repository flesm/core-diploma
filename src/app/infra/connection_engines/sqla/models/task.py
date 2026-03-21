from sqlalchemy import Column, DateTime, ForeignKey, String, Text, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.app.application.entities.task import TaskEntity
from src.app.infra.connection_engines.sqla.models.base import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("uuid_generate_v4()"),
    )
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False, server_default=text("''"))
    mentor_id = Column(UUID(as_uuid=True), nullable=False)
    intern_id = Column(UUID(as_uuid=True), nullable=False)
    status_id = Column(
        UUID(as_uuid=True), ForeignKey("task_statuses.id"), nullable=False
    )
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    status = relationship("TaskStatus", lazy="selectin")
    comments = relationship(
        "TaskComment",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    links = relationship(
        "TaskLink",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    attachments = relationship(
        "TaskAttachment",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    def to_entity(self) -> TaskEntity:
        return TaskEntity(
            id=self.id,
            title=self.title,
            description=self.description,
            mentor_id=self.mentor_id,
            intern_id=self.intern_id,
            status_id=self.status_id,
            created_at=self.created_at,
            updated_at=self.updated_at,
            status=self.status.to_entity() if self.status else None,
            comments=[comment.to_entity() for comment in self.comments],
            links=[link.to_entity() for link in self.links],
            attachments=[
                attachment.to_entity() for attachment in self.attachments
            ],
        )
