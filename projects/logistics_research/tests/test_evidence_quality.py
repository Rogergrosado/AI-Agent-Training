import sys
import unittest
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_DIR))

from evidence_quality import evaluate_evidence


class TestEvidenceQuality(unittest.TestCase):

    def setUp(self):
        self.source = {
            "title": "Supply Chains and Port Congestion Around the World",
            "url": "https://doi.org/10.5089/9798400202957.001",
            "source": "IMF Working Papers",
        }
        self.query = "port congestion supply chain shipping delays"

    def test_related_source(self):
        result = evaluate_evidence(self.source, self.query)
        self.assertEqual(result["relevance"], "related")

    def test_traceable_source(self):
        result = evaluate_evidence(self.source, self.query)
        self.assertTrue(result["traceable"])

    def test_unverified_content(self):
        result = evaluate_evidence(self.source, self.query)
        self.assertFalse(result["content_verified"])
        self.assertFalse(result["supports_specific_shipment_claim"])

    def test_unrelated_source(self):
        source = {
            "title": "Agricultural Irrigation Methods",
            "url": "https://example.org/agriculture",
            "source": "Research Journal",
        }
        result = evaluate_evidence(source, self.query)
        self.assertEqual(result["relevance"], "not_established")

    def test_missing_publisher(self):
        source = dict(self.source)
        source["source"] = ""

        result = evaluate_evidence(source, self.query)
        self.assertFalse(result["traceable"])

    def test_invalid_url(self):
        source = dict(self.source)
        source["url"] = "not-a-valid-url"

        result = evaluate_evidence(source, self.query)
        self.assertFalse(result["traceable"])

    def test_invalid_source_type(self):
        with self.assertRaises(ValueError):
            evaluate_evidence("invalid source", self.query)

    def test_invalid_query_type(self):
        with self.assertRaises(ValueError):
            evaluate_evidence(self.source, None)


if __name__ == "__main__":
    unittest.main()
