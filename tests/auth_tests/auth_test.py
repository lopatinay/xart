from fastapi import status

from service_api.models import UserModel, UserRoles
from tests import BaseTest
from tests import test_db_conn as db


class AuthTest(BaseTest):
    def setUp(self):
        self.test_user = UserModel(email="test@test.com", role=UserRoles.QA, password="password")
        db.add(self.test_user)
        db.commit()

    def test_successful_loging(self):
        resp = self.client.post(
            self.api_v1("/auth/token"),
            json={"email": "test@test.com", "password": "password"}
        )

        self.assertEqual(status.HTTP_200_OK, resp.status_code)

    def test_wrong_password(self):
        resp = self.client.post(
            self.api_v1("/auth/token"),
            json={"email": "test@test.com", "password": "foobar"}
        )

        self.assertEqual(status.HTTP_403_FORBIDDEN, resp.status_code)

    def test_non_existent_user(self):
        resp = self.client.post(
            self.api_v1("/auth/token"),
            json={"email": "foo@bar.com", "password": "password"}
        )

        self.assertEqual(status.HTTP_403_FORBIDDEN, resp.status_code)
