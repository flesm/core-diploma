from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from uuid import UUID

from src.app.application.entities.viewer import AuthenticatedUser
from src.app.application.use_cases.task_links.service import TaskLinkService
from src.app.container import Container
from src.app.presentation.rest.dependencies.auth import get_current_user
from src.app.presentation.rest.routes.v1.common import (
    TaskLinkCreateViewModel,
    TaskLinkResponseViewModel,
)

router = APIRouter(prefix="/tasks/{task_id}/links")


@router.get("", response_model=list[TaskLinkResponseViewModel])
@inject
async def list_links(
    task_id: UUID,
    actor: AuthenticatedUser = Depends(get_current_user),
    service: TaskLinkService = Depends(Provide[Container.task_link_service]),
) -> list[TaskLinkResponseViewModel]:
    entities = await service.list(actor, task_id)
    return [TaskLinkResponseViewModel.from_entity(item) for item in entities]


@router.post("", response_model=TaskLinkResponseViewModel)
@inject
async def create_link(
    task_id: UUID,
    payload: TaskLinkCreateViewModel,
    actor: AuthenticatedUser = Depends(get_current_user),
    service: TaskLinkService = Depends(Provide[Container.task_link_service]),
) -> TaskLinkResponseViewModel:
    entity = await service.create(actor, task_id, str(payload.url), payload.title)
    return TaskLinkResponseViewModel.from_entity(entity)


@router.patch("/{link_id}", response_model=TaskLinkResponseViewModel)
@inject
async def update_link(
    task_id: UUID,
    link_id: UUID,
    payload: TaskLinkCreateViewModel,
    actor: AuthenticatedUser = Depends(get_current_user),
    service: TaskLinkService = Depends(Provide[Container.task_link_service]),
) -> TaskLinkResponseViewModel:
    entity = await service.update(
        actor, task_id, link_id, str(payload.url), payload.title
    )
    return TaskLinkResponseViewModel.from_entity(entity)


@router.delete("/{link_id}", status_code=204)
@inject
async def delete_link(
    task_id: UUID,
    link_id: UUID,
    actor: AuthenticatedUser = Depends(get_current_user),
    service: TaskLinkService = Depends(Provide[Container.task_link_service]),
) -> None:
    await service.delete(actor, task_id, link_id)
