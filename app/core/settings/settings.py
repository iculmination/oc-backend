from pydantic_settings import BaseSettings, SettingsConfigDict

from app.core.settings.app import AppSettings
from app.core.settings.db import DbSettings


class Settings(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore")
    
    app: AppSettings = AppSettings()
    db: DbSettings = DbSettings()


settings = Settings(_env_file=".env")
