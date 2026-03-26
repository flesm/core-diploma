import pytest

from src.app.application.exceptions import (
    BadRequestException,
    ForbiddenException,
)
from src.app.application.use_cases.shared import AccessService, normalize_status_code


class TestNormalizeStatusCode:
    def test_normalizes_spaces_and_case(self) -> None:
        assert normalize_status_code(" In progress ") == "IN_PROGRESS"


class TestAccessService:
    async def test_get_default_status_returns_default(
        self,
        fake_uow,
        task_status,
    ) -> None:
        fake_uow.task_statuses.list_all.return_value = [task_status]

        service = AccessService(fake_uow)

        result = await service.get_default_status()

        assert result == task_status

    async def test_get_default_status_raises_when_missing(self, fake_uow) -> None:
        fake_uow.task_statuses.list_all.return_value = []

        service = AccessService(fake_uow)

        with pytest.raises(BadRequestException):
            await service.get_default_status()

    async def test_require_task_access_forbids_foreign_intern(
        self,
        fake_uow,
        mentor_user,
        intern_user,
        task_entity,
    ) -> None:
        fake_uow.tasks.get_by_id.return_value = task_entity
        service = AccessService(fake_uow)
        foreign_intern = intern_user.__class__(
            user_id=mentor_user.user_id,
            email="other@example.com",
            role="intern",
            is_staff=False,
        )

        with pytest.raises(ForbiddenException):
            await service.require_task_access(foreign_intern, task_entity.id)

