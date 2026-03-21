from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from uuid import UUID

from src.app.application.entities.viewer import AuthenticatedUser
from src.app.application.use_cases.task_statuses.service import TaskStatusService
from src.app.container import Container
from src.app.presentation.rest.dependencies.auth import get_current_user
from src.app.presentation.rest.routes.v1.common import (
    TaskStatusCreateViewModel,
    TaskStatusResponseViewModel,
)

router = APIRouter(prefix="/task-statuses")


@router.get("", response_model=list[TaskStatusResponseViewModel])
@inject
async def list_statuses(
    actor: AuthenticatedUser = Depends(get_current_user),
    service: TaskStatusService = Depends(Provide[Container.task_status_service]),
) -> list[TaskStatusResponseViewModel]:
    entities = await service.list_all(actor)
    return [TaskStatusResponseViewModel.from_entity(item) for item in entities]


@router.post("", response_model=TaskStatusResponseViewModel)
@inject
async def create_status(
    payload: TaskStatusCreateViewModel,
    actor: AuthenticatedUser = Depends(get_current_user),
    service: TaskStatusService = Depends(Provide[Container.task_status_service]),
) -> TaskStatusResponseViewModel:
    entity = await service.create(
        actor,
        name=payload.name,
        code=payload.code,
        order_index=payload.order_index,
        is_default=payload.is_default,
    )
    return TaskStatusResponseViewModel.from_entity(entity)


@router.patch("/{status_id}", response_model=TaskStatusResponseViewModel)
@inject
async def update_status(
    status_id: UUID,
    payload: TaskStatusCreateViewModel,
    actor: AuthenticatedUser = Depends(get_current_user),
    service: TaskStatusService = Depends(Provide[Container.task_status_service]),
) -> TaskStatusResponseViewModel:
    entity = await service.update(
        actor,
        status_id=status_id,
        name=payload.name,
        code=payload.code,
        order_index=payload.order_index,
        is_default=payload.is_default,
    )
    return TaskStatusResponseViewModel.from_entity(entity)


@router.delete("/{status_id}", status_code=204)
@inject
async def delete_status(
    status_id: UUID,
    actor: AuthenticatedUser = Depends(get_current_user),
    service: TaskStatusService = Depends(Provide[Container.task_status_service]),
) -> None:
    await service.delete(actor, status_id)
