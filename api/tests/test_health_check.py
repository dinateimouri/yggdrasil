import unittest
from api.main import app
from fastapi.testclient import TestClient


client = TestClient(app)


class TestHealthCheck(unittest.TestCase):
    def test_health_check(self):
        """
        Test health check api endpoint with both status and response
        """
        response = client.get("/healthz")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})


if __name__ == '__main__':
    unittest.main()
