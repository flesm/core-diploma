from dependency_injector import containers, providers

from src.app.application.use_cases.mentor_intern_links.service import (
    MentorInternLinkService,
)
from src.app.application.use_cases.task_attachments.service import (
    TaskAttachmentService,
)
from src.app.application.use_cases.task_comments.service import TaskCommentService
from src.app.application.use_cases.task_links.service import TaskLinkService
from src.app.application.use_cases.task_statuses.service import TaskStatusService
from src.app.application.use_cases.tasks.service import TaskService
from src.app.config import Config
from src.app.infra.connection_engines.sqla.db import Database
from src.app.infra.jwt.jwt_service import JwtService
from src.app.infra.unit_of_work.sqla import SQLAUnitOfWork


class DBContainer(containers.DeclarativeContainer):
    config = providers.Dependency(instance_of=Config)
    db = providers.Resource(Database, config=config.provided.DB)
    uow = providers.Factory(
        SQLAUnitOfWork,
        session_factory=db.provided.session_factory,
    )


class Container(containers.DeclarativeContainer):
    config = providers.Singleton(Config)

    db = providers.Container(DBContainer, config=config)
    jwt_service = providers.Singleton(JwtService, config=config)
    mentor_intern_link_service = providers.Factory(
        MentorInternLinkService, rdbms_uow=db.container.uow
    )
    task_status_service = providers.Factory(
        TaskStatusService, rdbms_uow=db.container.uow
    )
    task_service = providers.Factory(TaskService, rdbms_uow=db.container.uow)
    task_comment_service = providers.Factory(
        TaskCommentService, rdbms_uow=db.container.uow
    )
    task_link_service = providers.Factory(
        TaskLinkService, rdbms_uow=db.container.uow
    )
    task_attachment_service = providers.Factory(
        TaskAttachmentService, rdbms_uow=db.container.uow
    )
