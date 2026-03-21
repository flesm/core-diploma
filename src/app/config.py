from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings


class DBConfig(BaseModel):
    host: str
    port: int
    db: str
    user: str
    password: str
    dsn: PostgresDsn
    test_dsn: PostgresDsn | None = None


class JWTConfig(BaseModel):
    access_secret_key: str
    algorithm: str


class AppConfig(BaseModel):
    host: str


class Config(BaseSettings):
    class Config:
        env_file = ".env"
        env_nested_delimiter = "__"
        extra = "ignore"

    DB: DBConfig
    JWT: JWTConfig
    APP: AppConfig
