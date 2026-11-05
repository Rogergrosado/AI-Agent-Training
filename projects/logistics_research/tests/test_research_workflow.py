import sys
import unittest
from pathlib import Path
from unittest.mock import patch

PROJECT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_DIR))

from research_workflow import run_research_workflow


class TestResearchWorkflow(unittest.TestCase):

    def test_normal_shipment_skips_research(self):
        with patch("research_workflow.search_external_sources") as mock_search:
            report = run_research_workflow("SHP-001")

        self.assertEqual(report["research_status"], "not_required")
        self.assertIsNone(report["research_query"])
        self.assertEqual(report["external_sources"], [])
        self.assertIsNone(report["research_error"])
        mock_search.assert_not_called()

    def test_delayed_shipment_uses_external_research(self):
        fake_response = {
            "status": "success",
            "results": [
                {
                    "title": "Port Congestion Research",
                    "url": "https://example.org/research",
                    "source": "Example Journal",
                    "publication_date": "2026-01-01",
                    "evidence_type": "research_metadata",
                }
            ],
            "error": None,
        }

        with patch(
            "research_workflow.search_external_sources",
            return_value=fake_response,
        ) as mock_search:
            report = run_research_workflow("SHP-002")

        self.assertEqual(report["research_status"], "success")
        self.assertEqual(len(report["external_sources"]), 1)
        self.assertEqual(
            report["external_sources"][0]["title"],
            "Port Congestion Research",
        )
        self.assertIn("port congestion", report["research_query"].lower())
        mock_search.assert_called_once()

    def test_external_research_failure(self):
        fake_response = {
            "status": "error",
            "results": [],
            "error": "Simulated connection failure",
        }

        with patch(
            "research_workflow.search_external_sources",
            return_value=fake_response,
        ):
            report = run_research_workflow("SHP-002")

        self.assertEqual(report["research_status"], "error")
        self.assertEqual(report["external_sources"], [])
        self.assertEqual(
            report["research_error"],
            "Simulated connection failure",
        )
        self.assertEqual(
            report["decision_report"]["classification"],
            "delayed",
        )

    def test_missing_shipment(self):
        with self.assertRaises(ValueError):
            run_research_workflow("SHP-999")

    def test_successful_research_assesses_evidence(self):
        fake_response = {
            "status": "success",
            "results": [
                {
                    "title": "Port Congestion Research",
                    "url": "https://example.org/research",
                    "source": "Example Journal",
                    "publication_date": "2026-01-01",
                    "evidence_type": "research_metadata",
                }
            ],
            "error": None,
        }

        with patch(
            "research_workflow.search_external_sources",
            return_value=fake_response,
        ):
            report = run_research_workflow("SHP-002")

        self.assertEqual(report["research_status"], "success")
        self.assertEqual(len(report["external_sources"]), 1)
        self.assertEqual(len(report["evidence_assessments"]), 1)

        assessment = report["evidence_assessments"][0]

        self.assertEqual(
            assessment["title"],
            "Port Congestion Research",
        )
        self.assertFalse(assessment["content_verified"])

    def test_empty_research_has_no_assessments(self):
        fake_response = {
            "status": "success",
            "results": [],
            "error": None,
        }

        with patch(
            "research_workflow.search_external_sources",
            return_value=fake_response,
        ):
            report = run_research_workflow("SHP-002")

        self.assertEqual(report["external_sources"], [])
        self.assertEqual(report["evidence_assessments"], [])

    def test_failed_research_has_no_assessments(self):
        fake_response = {
            "status": "error",
            "results": [],
            "error": "Simulated connection failure",
        }

        with patch(
            "research_workflow.search_external_sources",
            return_value=fake_response,
        ):
            report = run_research_workflow("SHP-002")

        self.assertEqual(report["research_status"], "error")
        self.assertEqual(report["external_sources"], [])
        self.assertEqual(report["evidence_assessments"], [])
        self.assertEqual(
            report["research_error"],
            "Simulated connection failure",
        )


if __name__ == "__main__":
    unittest.main()
