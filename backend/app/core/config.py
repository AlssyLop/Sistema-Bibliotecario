from typing import List, Any
from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "Sistema Bibliotecario PCA"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # MySQL Database Config
    DB_HOST: str = "localhost"
    DB_PORT: int = 3307
    DB_USER: str = "root"
    DB_PASSWORD: str = "123456"
    DB_NAME: str = "biblioteca_pca"
    DATABASE_URL_OVERRIDE: str | None = None

    # CORS Configuration — se acepta como string separado por comas
    # Ejemplo: "http://localhost:8001,http://localhost"
    CORS_ORIGINS: str = "*"

    @property
    def cors_origins_list(self) -> List[str]:
        """Convierte CORS_ORIGINS (str separado por comas) a lista."""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]

    @computed_field
    @property
    def DATABASE_URL(self) -> str:
        if self.DATABASE_URL_OVERRIDE:
            return self.DATABASE_URL_OVERRIDE
        user_pass = f"{self.DB_USER}:{self.DB_PASSWORD}" if self.DB_PASSWORD else self.DB_USER
        return f"mysql+pymysql://{user_pass}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}?charset=utf8mb4"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()
