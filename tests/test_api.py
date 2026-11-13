import sys
import unittest
from pathlib import Path

from fastapi.testclient import TestClient

PROJECT_ROOT = Path(__file__).resolve().parents[1]
API_DIR = PROJECT_ROOT / "src" / "api"
ORCHESTRATION_DIR = PROJECT_ROOT / "src" / "orchestration"

sys.path.insert(0, str(API_DIR))
sys.path.insert(0, str(ORCHESTRATION_DIR))

from main import app


class TestSentinelAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_root_endpoint(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["application"], "Sentinel AI")

    def test_health_endpoint(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "OPERATIONAL")
        self.assertEqual(response.json()["domains_available"], 3)

    def test_domains_endpoint(self):
        response = self.client.get("/domains")
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(data["domains_total"], 3)

        self.assertEqual(
            set(data["domains"].keys()),
            {"cybersecurity", "climate", "economy"}
        )

    def test_cybersecurity_endpoint(self):
        response = self.client.get("/domains/cybersecurity")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["records"], 1768)

    def test_climate_endpoint(self):
        response = self.client.get("/domains/climate")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["records"], 297)

    def test_economy_endpoint(self):
        response = self.client.get("/domains/economy")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["records"], 297)

    def test_unknown_domain(self):
        response = self.client.get("/domains/unknown")
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
