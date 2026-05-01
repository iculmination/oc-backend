from pydantic_settings import BaseSettings, SettingsConfigDict


class DbSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="DB_")
    
    user: str
    password: str
    name: str
    host: str
    port: int
    pool_size: int = 100
    max_overflow: int = 10
    pool_recycle: int = 1800

    @property
    def url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"
