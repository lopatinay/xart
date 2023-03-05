import os

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy_utils import database_exists, create_database, drop_database

from service_api.app import fast_app
from service_api.configs import RuntimeConfig
from service_api.services.database import db_conn
from tests import test_db_url, test_engine, TestingSession


@pytest.fixture(scope="session", autouse=True)
def db_fixture():
    if database_exists(test_engine.url):
        drop_database(test_db_url)
    create_database(test_engine.url)

    alembic_cfg = Config()
    alembic_cfg.set_main_option(
        "script_location", os.path.join(RuntimeConfig.base_dir, "alembic")
    )
    alembic_cfg.set_main_option("sqlalchemy.url", test_db_url)
    command.upgrade(alembic_cfg, "head")

    yield

    if database_exists(test_engine.url):
        drop_database(test_db_url)


def test_db_conn():
    session = TestingSession()
    try:
        yield session
    finally:
        session.close()


fast_app.dependency_overrides[db_conn] = test_db_conn
