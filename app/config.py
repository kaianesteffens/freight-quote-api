from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "freight-quote-api"

    database_url: str = "sqlite+pysqlite:///./freight.db"

    jwt_secret: str = "insecure-default-change-me"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60

    freight_base_price: float = 20.0
    freight_price_per_kg: float = 1.5
    freight_price_per_m3: float = 8.0
    freight_distance_factor: float = 0.5


@lru_cache
def get_settings() -> Settings:
    return Settings()
