from pathlib import Path, PosixPath
from uuid import uuid4

from pydantic import BaseSettings

from service_api.constants import AppEnvs


class _AppConfig(BaseSettings):
    class Config:
        env_file = ".env"

    # Application
    app_name: str = "xart_test_api"
    app_runtime_id: str = f"{app_name}::{uuid4()})"
    app_env: str = AppEnvs.localhost
    debug: bool = True
    base_dir: PosixPath = Path(__file__).resolve().parent.parent

    # Database
    pg_host: str = "localhost"
    ph_port: str = "5435"
    pg_user: str = "postgres"
    pg_pass: str = "postgres"
    pg_name: str = "postgres"
    pg_test_database: str = "test_postgres"
    pg_echo: bool = True
    pg_pool_size: int = 5
    pg_max_overflow: int = 10
    pg_pool_recycle: int = 3600

    # Tools
    log_level: str = "DEBUG"


RuntimeConfig = _AppConfig()
