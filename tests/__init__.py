from unittest import TestCase

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from service_api.app import fast_app
from service_api.configs import RuntimeConfig
from service_api.models import BaseModel


test_db_url = (
    "postgresql+psycopg2://"
    f"{RuntimeConfig.pg_user}:{RuntimeConfig.pg_pass}@"
    f"{RuntimeConfig.pg_host}:{RuntimeConfig.ph_port}/"
    f"{RuntimeConfig.pg_test_database}"
)

test_engine = create_engine(
    test_db_url,
    connect_args={"application_name": f"test::{RuntimeConfig.app_runtime_id}"},
)

TestingSession = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
test_db_conn = TestingSession()


class BaseTest(TestCase):
    client = TestClient(fast_app)

    def api_v1(self, path):
        return f"/api/v1{path}"

    def tearDown(self) -> None:
        for table in BaseModel.metadata.sorted_tables:
            test_db_conn.execute(table.delete())
