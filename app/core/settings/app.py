from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="APP_")
    
    host: str
    port: int
    api_url: str
    
    environment: str
    allowed_origins: list[str]