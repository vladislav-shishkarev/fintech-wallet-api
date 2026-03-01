from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_port: int
    postgres_db: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @property
    def db_url(self):
        return (f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}"
                f":{self.postgres_port}/{self.postgres_db}")


settings = Settings()