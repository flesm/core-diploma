import pytest

from src.app.application.exceptions import ForbiddenException
from src.app.application.use_cases.tasks.service import TaskService


class TestTaskService:
    async def test_create_uses_default_status_when_status_is_not_provided(
        self,
        fake_uow,
        mentor_user,
        intern_user,
        mentor_intern_link,
        task_status,
        task_entity,
    ) -> None:
        fake_uow.mentor_intern_links.get_by_intern.return_value = mentor_intern_link
        fake_uow.task_statuses.list_all.return_value = [task_status]
        fake_uow.tasks.create.return_value = task_entity
        service = TaskService(fake_uow)

        result = await service.create(
            actor=mentor_user,
            title=task_entity.title,
            description=task_entity.description,
            intern_id=intern_user.user_id,
            status_id=None,
        )

        assert result == task_entity
        fake_uow.tasks.create.assert_awaited_once()

    async def test_list_tasks_for_intern_uses_intern_repository(
        self,
        fake_uow,
        intern_user,
        task_entity,
    ) -> None:
        fake_uow.tasks.list_for_intern.return_value = [task_entity]
        service = TaskService(fake_uow)

        result = await service.list_tasks(intern_user, None, task_entity.status_id)

        assert result == [task_entity]
        fake_uow.tasks.list_for_intern.assert_awaited_once_with(
            intern_user.user_id,
            status_id=task_entity.status_id,
        )

    async def test_update_allows_mentor_to_reassign_task(
        self,
        fake_uow,
        mentor_user,
        mentor_intern_link,
        task_entity,
        task_status,
    ) -> None:
        fake_uow.tasks.get_by_id.return_value = task_entity
        fake_uow.task_statuses.get_by_id.return_value = task_status
        fake_uow.mentor_intern_links.get_by_intern.return_value = mentor_intern_link
        fake_uow.tasks.update.return_value = task_entity
        service = TaskService(fake_uow)

        result = await service.update(
            actor=mentor_user,
            task_id=task_entity.id,
            title="Updated",
            description="Updated description",
            intern_id=task_entity.intern_id,
            status_id=task_status.id,
        )

        assert result == task_entity
        fake_uow.tasks.update.assert_awaited_once()

    async def test_update_forbids_intern_reassign(
        self,
        fake_uow,
        intern_user,
        task_entity,
        task_status,
    ) -> None:
        fake_uow.tasks.get_by_id.return_value = task_entity
        fake_uow.task_statuses.get_by_id.return_value = task_status
        service = TaskService(fake_uow)

        with pytest.raises(ForbiddenException):
            await service.update(
                actor=intern_user,
                task_id=task_entity.id,
                title=task_entity.title,
                description=task_entity.description,
                intern_id=intern_user.user_id,
                status_id=task_status.id,
            )

    async def test_board_groups_tasks_by_status(
        self,
        fake_uow,
        mentor_user,
        task_status,
        task_entity,
    ) -> None:
        fake_uow.task_statuses.list_all.return_value = [task_status]
        fake_uow.tasks.list_for_mentor.return_value = [task_entity]
        service = TaskService(fake_uow)

        result = await service.board(mentor_user, None, None)

        assert len(result) == 1
        assert result[0].status == task_status
        assert result[0].tasks == [task_entity]
