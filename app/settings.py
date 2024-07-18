from loguru import logger
from pydantic import BaseModel, ConfigDict
from pydantic_settings import BaseSettings, SettingsConfigDict


class ApplicationSettings(BaseModel):
    model_config = ConfigDict(extra="ignore")

    host: str = "127.0.0.1"
    port: int = 8000
    workers: int | None = None


class DatabaseSettings(BaseModel):
    model_config = ConfigDict(extra="ignore")

    host: str = "db"
    port: int = 5432
    username: str = "depthimages"
    pwd: str = "depthimages"
    database: str = "depthimages"

    def get_dsn(self, async_schema: bool = True) -> str:
        return (
            f"{'postgresql+asyncpg' if async_schema else 'postgresql'}://"
            f"{self.username}:{self.pwd}@"
            f"{self.host}:{self.port}/{self.database}"
        )


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_nested_delimiter="__",
        env_file_encoding="utf-8",
        env_file=".env",
        yaml_file="config.yml",
        yaml_file_encoding="utf-8",
        extra="ignore",
    )

    app: ApplicationSettings = ApplicationSettings()
    db: DatabaseSettings = DatabaseSettings()


try:
    SETTINGS = Settings()
except Exception as e:
    logger.exception(f"Error on settings initialization: {e}")
    raise e
