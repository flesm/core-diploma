from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    String,
    UniqueConstraint,
    text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from src.app.application.entities.link import MentorInternLinkEntity, TaskLinkEntity
from src.app.infra.connection_engines.sqla.models.base import Base


class MentorInternLink(Base):
    __tablename__ = "mentor_intern_links"
    __table_args__ = (
        UniqueConstraint("intern_id", name="uq_intern_single_mentor"),
    )

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("uuid_generate_v4()"),
    )
    mentor_id = Column(UUID(as_uuid=True), nullable=False)
    intern_id = Column(UUID(as_uuid=True), nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    def to_entity(self) -> MentorInternLinkEntity:
        return MentorInternLinkEntity(
            id=self.id,
            mentor_id=self.mentor_id,
            intern_id=self.intern_id,
            created_at=self.created_at,
        )


class TaskLink(Base):
    __tablename__ = "task_links"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("uuid_generate_v4()"),
    )
    task_id = Column(UUID(as_uuid=True), ForeignKey("tasks.id"), nullable=False)
    author_id = Column(UUID(as_uuid=True), nullable=False)
    url = Column(String, nullable=False)
    title = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    def to_entity(self) -> TaskLinkEntity:
        return TaskLinkEntity(
            id=self.id,
            task_id=self.task_id,
            author_id=self.author_id,
            url=self.url,
            title=self.title,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
