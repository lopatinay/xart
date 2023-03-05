from http import HTTPStatus

from tests import BaseTest


class CommonTest(BaseTest):
    def test_health(self):
        resp = self.client.get("/health")
        self.assertEqual(HTTPStatus.OK, resp.status_code)
