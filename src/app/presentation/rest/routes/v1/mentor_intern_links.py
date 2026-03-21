from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from uuid import UUID

from src.app.application.entities.viewer import AuthenticatedUser
from src.app.application.use_cases.mentor_intern_links.service import (
    MentorInternLinkService,
)
from src.app.container import Container
from src.app.presentation.rest.dependencies.auth import get_current_user
from src.app.presentation.rest.routes.v1.common import (
    MentorInternLinkCreateViewModel,
    MentorInternLinkResponseViewModel,
)

router = APIRouter(prefix="/mentor-intern-links")


@router.post("", response_model=MentorInternLinkResponseViewModel)
@inject
async def create_link(
    payload: MentorInternLinkCreateViewModel,
    actor: AuthenticatedUser = Depends(get_current_user),
    service: MentorInternLinkService = Depends(
        Provide[Container.mentor_intern_link_service]
    ),
) -> MentorInternLinkResponseViewModel:
    entity = await service.create(actor, payload.intern_id)
    return MentorInternLinkResponseViewModel.from_entity(entity)


@router.get("", response_model=list[MentorInternLinkResponseViewModel])
@inject
async def list_links(
    actor: AuthenticatedUser = Depends(get_current_user),
    service: MentorInternLinkService = Depends(
        Provide[Container.mentor_intern_link_service]
    ),
) -> list[MentorInternLinkResponseViewModel]:
    entities = await service.list_my_interns(actor)
    return [MentorInternLinkResponseViewModel.from_entity(item) for item in entities]


@router.get("/{link_id}", response_model=MentorInternLinkResponseViewModel)
@inject
async def get_link(
    link_id: UUID,
    actor: AuthenticatedUser = Depends(get_current_user),
    service: MentorInternLinkService = Depends(
        Provide[Container.mentor_intern_link_service]
    ),
) -> MentorInternLinkResponseViewModel:
    entity = await service.get_by_id(actor, link_id)
    return MentorInternLinkResponseViewModel.from_entity(entity)


@router.get("/my-mentor", response_model=MentorInternLinkResponseViewModel)
@inject
async def get_my_mentor(
    actor: AuthenticatedUser = Depends(get_current_user),
    service: MentorInternLinkService = Depends(
        Provide[Container.mentor_intern_link_service]
    ),
) -> MentorInternLinkResponseViewModel:
    entity = await service.get_my_mentor(actor)
    return MentorInternLinkResponseViewModel.from_entity(entity)


@router.delete("/{link_id}", status_code=204)
@inject
async def delete_link(
    link_id: UUID,
    actor: AuthenticatedUser = Depends(get_current_user),
    service: MentorInternLinkService = Depends(
        Provide[Container.mentor_intern_link_service]
    ),
) -> None:
    await service.delete(actor, link_id)
