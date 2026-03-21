from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from uuid import UUID

from src.app.application.entities.viewer import AuthenticatedUser
from src.app.application.use_cases.tasks.service import TaskService
from src.app.container import Container
from src.app.presentation.rest.dependencies.auth import get_current_user
from src.app.presentation.rest.routes.v1.common import (
    TaskBoardColumnResponseViewModel,
    TaskCreateViewModel,
    TaskResponseViewModel,
    TaskUpdateViewModel,
)

router = APIRouter(prefix="/tasks")


@router.get("", response_model=list[TaskResponseViewModel])
@inject
async def list_tasks(
    intern_id: UUID | None = None,
    status_id: UUID | None = None,
    actor: AuthenticatedUser = Depends(get_current_user),
    service: TaskService = Depends(Provide[Container.task_service]),
) -> list[TaskResponseViewModel]:
    entities = await service.list_tasks(
        actor, intern_id=intern_id, status_id=status_id
    )
    return [TaskResponseViewModel.from_entity(item) for item in entities]


@router.get("/board", response_model=list[TaskBoardColumnResponseViewModel])
@inject
async def get_board(
    intern_id: UUID | None = None,
    status_id: UUID | None = None,
    actor: AuthenticatedUser = Depends(get_current_user),
    service: TaskService = Depends(Provide[Container.task_service]),
) -> list[TaskBoardColumnResponseViewModel]:
    columns = await service.board(actor, intern_id=intern_id, status_id=status_id)
    return [TaskBoardColumnResponseViewModel.from_entity(item) for item in columns]


@router.get("/{task_id}", response_model=TaskResponseViewModel)
@inject
async def get_task(
    task_id: UUID,
    actor: AuthenticatedUser = Depends(get_current_user),
    service: TaskService = Depends(Provide[Container.task_service]),
) -> TaskResponseViewModel:
    entity = await service.get(actor, task_id)
    return TaskResponseViewModel.from_entity(entity)


@router.post("", response_model=TaskResponseViewModel)
@inject
async def create_task(
    payload: TaskCreateViewModel,
    actor: AuthenticatedUser = Depends(get_current_user),
    service: TaskService = Depends(Provide[Container.task_service]),
) -> TaskResponseViewModel:
    entity = await service.create(
        actor,
        title=payload.title,
        description=payload.description,
        intern_id=payload.intern_id,
        status_id=payload.status_id,
    )
    return TaskResponseViewModel.from_entity(entity)


@router.patch("/{task_id}", response_model=TaskResponseViewModel)
@inject
async def update_task(
    task_id: UUID,
    payload: TaskUpdateViewModel,
    actor: AuthenticatedUser = Depends(get_current_user),
    service: TaskService = Depends(Provide[Container.task_service]),
) -> TaskResponseViewModel:
    entity = await service.update(
        actor,
        task_id=task_id,
        title=payload.title,
        description=payload.description,
        intern_id=payload.intern_id,
        status_id=payload.status_id,
    )
    return TaskResponseViewModel.from_entity(entity)


@router.delete("/{task_id}", status_code=204)
@inject
async def delete_task(
    task_id: UUID,
    actor: AuthenticatedUser = Depends(get_current_user),
    service: TaskService = Depends(Provide[Container.task_service]),
) -> None:
    await service.delete(actor, task_id)
