from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from uuid import UUID

from src.app.application.entities.viewer import AuthenticatedUser
from src.app.application.use_cases.task_attachments.service import (
    TaskAttachmentService,
)
from src.app.container import Container
from src.app.presentation.rest.dependencies.auth import get_current_user
from src.app.presentation.rest.routes.v1.common import (
    TaskAttachmentCreateViewModel,
    TaskAttachmentResponseViewModel,
)

router = APIRouter(prefix="/tasks/{task_id}/attachments")


@router.get("", response_model=list[TaskAttachmentResponseViewModel])
@inject
async def list_attachments(
    task_id: UUID,
    actor: AuthenticatedUser = Depends(get_current_user),
    service: TaskAttachmentService = Depends(
        Provide[Container.task_attachment_service]
    ),
) -> list[TaskAttachmentResponseViewModel]:
    entities = await service.list(actor, task_id)
    return [TaskAttachmentResponseViewModel.from_entity(item) for item in entities]


@router.post("", response_model=TaskAttachmentResponseViewModel)
@inject
async def create_attachment(
    task_id: UUID,
    payload: TaskAttachmentCreateViewModel,
    actor: AuthenticatedUser = Depends(get_current_user),
    service: TaskAttachmentService = Depends(
        Provide[Container.task_attachment_service]
    ),
) -> TaskAttachmentResponseViewModel:
    entity = await service.create(
        actor,
        task_id,
        payload.file_ref,
        payload.display_name,
        payload.source_type,
    )
    return TaskAttachmentResponseViewModel.from_entity(entity)


@router.delete("/{attachment_id}", status_code=204)
@inject
async def delete_attachment(
    task_id: UUID,
    attachment_id: UUID,
    actor: AuthenticatedUser = Depends(get_current_user),
    service: TaskAttachmentService = Depends(
        Provide[Container.task_attachment_service]
    ),
) -> None:
    await service.delete(actor, task_id, attachment_id)
