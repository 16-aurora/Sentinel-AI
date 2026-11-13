import csv
import tempfile
import unittest
from pathlib import Path

from multidomain_orchestrator import (
    MultidomainOrchestrator,
    DOMAIN_CONFIG
)


class TestMultidomainOrchestrator(unittest.TestCase):

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

        for domain, config in DOMAIN_CONFIG.items():

            path = self.root / config["file"]
            path.parent.mkdir(parents=True, exist_ok=True)

            with open(path, "w", encoding="utf-8", newline="") as file:
                writer = csv.DictWriter(
                    file,
                    fieldnames=config["required_columns"]
                )
                writer.writeheader()

                for index in range(config["expected_rows"]):

                    row = {
                        column: "TEST"
                        for column in config["required_columns"]
                    }

                    row[config["score_column"]] = "50"
                    row[config["category_column"]] = "MODERATE"

                    if domain == "cybersecurity":
                        row["cveID"] = f"CVE-TEST-{index}"
                    else:
                        row["country_code"] = f"C{index:02d}"
                        row["year"] = str(2000 + index)

                    writer.writerow(row)

        self.orchestrator = MultidomainOrchestrator(self.root)

    def tearDown(self):
        self.temp.cleanup()

    def test_all_domains_available(self):
        report = self.orchestrator.run()
        self.assertEqual(report["system_status"], "OPERATIONAL")
        self.assertEqual(report["domains_available"], 3)

    def test_missing_domain(self):
        path = self.root / DOMAIN_CONFIG["climate"]["file"]
        path.unlink()

        result = self.orchestrator.run()

        self.assertEqual(result["system_status"], "PARTIAL")
        self.assertEqual(
            result["domains"]["climate"]["status"],
            "UNAVAILABLE"
        )

    def test_invalid_schema(self):
        config = DOMAIN_CONFIG["climate"]
        path = self.root / config["file"]

        with open(path, "w", encoding="utf-8", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["wrong_column"])
            writer.writerow(["TEST"])

        result = self.orchestrator._load_domain("climate")
        self.assertEqual(result["status"], "SCHEMA_ERROR")

    def test_unexpected_record_count(self):
        config = DOMAIN_CONFIG["economy"]
        path = self.root / config["file"]

        with open(path, "w", encoding="utf-8", newline="") as file:
            writer = csv.DictWriter(
                file,
                fieldnames=config["required_columns"]
            )
            writer.writeheader()
            writer.writerow({
                column: "TEST"
                for column in config["required_columns"]
            })

        result = self.orchestrator._load_domain("economy")
        self.assertEqual(result["status"], "REVIEW")

    def test_duplicate_key(self):
        config = DOMAIN_CONFIG["climate"]
        path = self.root / config["file"]

        with open(path, encoding="utf-8", newline="") as file:
            reader = csv.DictReader(file)
            columns = reader.fieldnames
            rows = list(reader)

        rows[1]["country_code"] = rows[0]["country_code"]
        rows[1]["year"] = rows[0]["year"]

        with open(path, "w", encoding="utf-8", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=columns)
            writer.writeheader()
            writer.writerows(rows)

        result = self.orchestrator._load_domain("climate")
        self.assertEqual(result["status"], "DATA_ERROR")
        self.assertIn("Duplicate", result["error"])

    def test_invalid_score(self):
        config = DOMAIN_CONFIG["cybersecurity"]
        path = self.root / config["file"]

        with open(path, encoding="utf-8", newline="") as file:
            reader = csv.DictReader(file)
            columns = reader.fieldnames
            rows = list(reader)

        rows[0]["risk_score"] = "NaN"

        with open(path, "w", encoding="utf-8", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=columns)
            writer.writeheader()
            writer.writerows(rows)

        result = self.orchestrator._load_domain("cybersecurity")
        self.assertEqual(result["status"], "DATA_ERROR")
        self.assertIn("Non-finite", result["error"])


if __name__ == "__main__":
    unittest.main()
