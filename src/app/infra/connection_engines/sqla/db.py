import json
from collections.abc import Callable
from typing import Any, Self

from pydantic.v1.json import pydantic_encoder
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.app.config import DBConfig


def json_dumps(
    value: Any, *, default: Callable[[Any], Any] = pydantic_encoder
) -> str:
    return json.dumps(value, default=default)


class Database:
    def __init__(self, config: DBConfig) -> None:
        self._engine: AsyncEngine = create_async_engine(
            url=str(config.dsn),
            echo=True,
        )
        self._session_factory = async_sessionmaker(
            bind=self._engine, expire_on_commit=False
        )

    @classmethod
    def from_engine(cls, engine: AsyncEngine) -> Self:
        obj = cls.__new__(cls)
        obj._engine = engine
        obj._session_factory = async_sessionmaker(
            bind=engine, expire_on_commit=False
        )
        return obj

    @property
    def engine(self) -> AsyncEngine:
        return self._engine

    @property
    def session_factory(self) -> async_sessionmaker[AsyncSession]:
        return self._session_factory
