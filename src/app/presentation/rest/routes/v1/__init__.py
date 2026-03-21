from fastapi import APIRouter

from src.app.presentation.rest.routes.v1.mentor_intern_links import router as mentor_intern_router
from src.app.presentation.rest.routes.v1.task_attachments import router as task_attachments_router
from src.app.presentation.rest.routes.v1.task_comments import router as task_comments_router
from src.app.presentation.rest.routes.v1.task_links import router as task_links_router
from src.app.presentation.rest.routes.v1.task_statuses import router as task_statuses_router
from src.app.presentation.rest.routes.v1.tasks import router as tasks_router

v1_router = APIRouter()
v1_router.include_router(mentor_intern_router, tags=["MentorInternLinks"])
v1_router.include_router(task_statuses_router, tags=["TaskStatuses"])
v1_router.include_router(tasks_router, tags=["Tasks"])
v1_router.include_router(task_comments_router, tags=["TaskComments"])
v1_router.include_router(task_links_router, tags=["TaskLinks"])
v1_router.include_router(task_attachments_router, tags=["TaskAttachments"])
