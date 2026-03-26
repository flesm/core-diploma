import pytest

from src.app.application.entities.status import TaskStatusEntity
from src.app.application.exceptions import (
    BadRequestException,
    ForbiddenException,
    NotFoundException,
)
from src.app.application.use_cases.task_statuses.service import TaskStatusService


class TestTaskStatusService:
    async def test_list_all_returns_repository_data(
        self,
        fake_uow,
        mentor_user,
        task_status,
    ) -> None:
        fake_uow.task_statuses.list_all.return_value = [task_status]
        service = TaskStatusService(fake_uow)

        result = await service.list_all(mentor_user)

        assert result == [task_status]

    async def test_create_rejects_duplicate_status_code(
        self,
        fake_uow,
        mentor_user,
        task_status,
    ) -> None:
        fake_uow.task_statuses.get_by_code.return_value = task_status
        service = TaskStatusService(fake_uow)

        with pytest.raises(BadRequestException):
            await service.create(mentor_user, "To do", None, 1, True)

    async def test_update_rejects_system_status(
        self,
        fake_uow,
        mentor_user,
        task_status,
    ) -> None:
        fake_uow.task_statuses.get_by_id.return_value = TaskStatusEntity(
            **{**task_status.__dict__, "is_system": True}
        )
        service = TaskStatusService(fake_uow)

        with pytest.raises(ForbiddenException):
            await service.update(
                mentor_user,
                task_status.id,
                "Done",
                None,
                2,
                False,
            )

    async def test_delete_rejects_foreign_author(
        self,
        fake_uow,
        mentor_user,
        task_status,
    ) -> None:
        foreign_status = TaskStatusEntity(
            **{**task_status.__dict__, "created_by": None}
        )
        fake_uow.task_statuses.get_by_id.return_value = foreign_status
        service = TaskStatusService(fake_uow)

        with pytest.raises(ForbiddenException):
            await service.delete(mentor_user, task_status.id)

    async def test_update_raises_when_repository_returns_none(
        self,
        fake_uow,
        mentor_user,
        task_status,
    ) -> None:
        fake_uow.task_statuses.get_by_id.return_value = task_status
        fake_uow.task_statuses.get_by_code.return_value = None
        fake_uow.task_statuses.update.return_value = None
        service = TaskStatusService(fake_uow)

        with pytest.raises(NotFoundException):
            await service.update(
                mentor_user,
                task_status.id,
                task_status.name,
                task_status.code,
                task_status.order_index,
                task_status.is_default,
            )
