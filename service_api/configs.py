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
    base_dir: PosixPath = Path(__file__).resolve().parent

    # Cryptography
    jwt_secret_key: str = "e03d0fd0e0d69ebdd8b9556525ef7bf1803a57d0b4867a3dc519d1a1f57b5d1e"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

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

    # Assets
    challenge_backend_dir = base_dir.joinpath("assets", "challenge_backend")
    products_dir = challenge_backend_dir.joinpath("challenge_products")
    snapshots_dir = challenge_backend_dir.joinpath("challenge_snapshots")


RuntimeConfig = _AppConfig()
