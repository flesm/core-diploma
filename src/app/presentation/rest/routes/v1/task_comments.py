from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from uuid import UUID

from src.app.application.entities.viewer import AuthenticatedUser
from src.app.application.use_cases.task_comments.service import TaskCommentService
from src.app.container import Container
from src.app.presentation.rest.dependencies.auth import get_current_user
from src.app.presentation.rest.routes.v1.common import (
    TaskCommentCreateViewModel,
    TaskCommentResponseViewModel,
)

router = APIRouter(prefix="/tasks/{task_id}/comments")


@router.get("", response_model=list[TaskCommentResponseViewModel])
@inject
async def list_comments(
    task_id: UUID,
    actor: AuthenticatedUser = Depends(get_current_user),
    service: TaskCommentService = Depends(
        Provide[Container.task_comment_service]
    ),
) -> list[TaskCommentResponseViewModel]:
    entities = await service.list(actor, task_id)
    return [TaskCommentResponseViewModel.from_entity(item) for item in entities]


@router.post("", response_model=TaskCommentResponseViewModel)
@inject
async def create_comment(
    task_id: UUID,
    payload: TaskCommentCreateViewModel,
    actor: AuthenticatedUser = Depends(get_current_user),
    service: TaskCommentService = Depends(
        Provide[Container.task_comment_service]
    ),
) -> TaskCommentResponseViewModel:
    entity = await service.create(actor, task_id, payload.content)
    return TaskCommentResponseViewModel.from_entity(entity)


@router.patch("/{comment_id}", response_model=TaskCommentResponseViewModel)
@inject
async def update_comment(
    task_id: UUID,
    comment_id: UUID,
    payload: TaskCommentCreateViewModel,
    actor: AuthenticatedUser = Depends(get_current_user),
    service: TaskCommentService = Depends(
        Provide[Container.task_comment_service]
    ),
) -> TaskCommentResponseViewModel:
    entity = await service.update(actor, task_id, comment_id, payload.content)
    return TaskCommentResponseViewModel.from_entity(entity)


@router.delete("/{comment_id}", status_code=204)
@inject
async def delete_comment(
    task_id: UUID,
    comment_id: UUID,
    actor: AuthenticatedUser = Depends(get_current_user),
    service: TaskCommentService = Depends(
        Provide[Container.task_comment_service]
    ),
) -> None:
    await service.delete(actor, task_id, comment_id)
