from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.app.config import Config
from src.app.container import Container
from src.app.presentation.rest.exception_handlers.exception_handlers import (
    setup_exception_handlers,
)
from src.app.presentation.rest.routes.v1 import v1_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, Any]:
    container = Container()
    container.config.override(Config())
    container.init_resources()
    container.wire(
        modules=[
            "src.app.presentation.rest.dependencies.auth",
            "src.app.presentation.rest.routes.v1.mentor_intern_links",
            "src.app.presentation.rest.routes.v1.task_attachments",
            "src.app.presentation.rest.routes.v1.task_comments",
            "src.app.presentation.rest.routes.v1.task_links",
            "src.app.presentation.rest.routes.v1.task_statuses",
            "src.app.presentation.rest.routes.v1.tasks",
        ]
    )
    app.container = container
    yield
    container.unwire()
    await container.shutdown_resources()


app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
setup_exception_handlers(app)
app.include_router(v1_router, prefix="/api/v1", tags=["v1"])


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Hello World"}
