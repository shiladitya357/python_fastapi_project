"""
Edit History:
| Person | Date | Comment |
| --- | --- | --- |
| Shiladitya | 07/10/2026 | Created |
"""

from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "FastAPI E-Commerce Demo"
    log_level: str = "INFO"
    log_dir: str = "./log"
    log_file_name: str = "app.log"

    mysql_host: str = "localhost"
    mysql_port: int = 3306
    mysql_database: str = "ecommerce"
    mysql_user: str = "ecommerce_user"
    mysql_password: str = "ecommerce_password"

    default_user_balance: float = Field(default=100000.00, ge=0)

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @property
    def database_url(self) -> str:
        return (
            "mysql+pymysql://"
            f"{self.mysql_user}:{self.mysql_password}"
            f"@{self.mysql_host}:{self.mysql_port}/{self.mysql_database}"
        )

    @property
    def log_file_path(self) -> str:
        return f"{self.log_dir.rstrip('/')}/{self.log_file_name}"


@lru_cache
def get_settings() -> Settings:
    return Settings()
