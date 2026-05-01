from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="APP_")
    
    host: str
    port: int
    api_url: str
    
    environment: str
    allowed_origins: list[str]
    jwt_secret: str
    jwt_access_ttl_minutes: int = 15
    jwt_refresh_ttl_days: int = 14
    auth_cookie_secure: bool = False