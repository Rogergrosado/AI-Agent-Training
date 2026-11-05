import sys
import unittest
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_DIR))

from shipment_analysis import (
    load_shipments,
    get_shipment_by_id,
    classify_shipment,
    generate_decision_report,
)


class TestShipmentAnalysis(unittest.TestCase):

    def test_dataset_contains_four_shipments(self):
        shipments = load_shipments()
        self.assertEqual(len(shipments), 4)

    def test_find_existing_shipment(self):
        shipment = get_shipment_by_id("SHP-002")
        self.assertIsNotNone(shipment)
        self.assertEqual(shipment["status"], "delayed")

    def test_missing_shipment(self):
        shipment = get_shipment_by_id("SHP-999")
        self.assertIsNone(shipment)

    def test_normal_shipment(self):
        shipment = get_shipment_by_id("SHP-001")
        result = classify_shipment(shipment)
        self.assertEqual(result["classification"], "normal")

    def test_delayed_shipment(self):
        shipment = get_shipment_by_id("SHP-002")
        result = classify_shipment(shipment)
        self.assertEqual(result["classification"], "delayed")

    def test_customs_hold(self):
        shipment = get_shipment_by_id("SHP-003")
        result = classify_shipment(shipment)
        self.assertEqual(result["classification"], "customs_hold")

    def test_critical_priority_overrides_delay(self):
        shipment = get_shipment_by_id("SHP-004")
        result = classify_shipment(shipment)
        self.assertEqual(result["classification"], "critical")

    def test_unknown_status_raises_error(self):
        shipment = {
            "status": "unknown",
            "priority": "low",
        }

        with self.assertRaises(ValueError):
            classify_shipment(shipment)

    def test_normal_report_requires_no_research(self):
        shipment = get_shipment_by_id("SHP-001")
        report = generate_decision_report(shipment)

        self.assertEqual(report["classification"], "normal")
        self.assertFalse(report["requires_external_research"])

    def test_delayed_report_requires_research(self):
        shipment = get_shipment_by_id("SHP-002")
        report = generate_decision_report(shipment)

        self.assertEqual(report["classification"], "delayed")
        self.assertTrue(report["requires_external_research"])
        self.assertEqual(
            report["evidence_source"],
            "local_shipment_dataset",
        )

    def test_critical_report_escalation(self):
        shipment = get_shipment_by_id("SHP-004")
        report = generate_decision_report(shipment)

        self.assertEqual(report["classification"], "critical")
        self.assertEqual(
            report["recommended_action"],
            "Escalate immediately",
        )
        self.assertTrue(report["requires_external_research"])


if __name__ == "__main__":
    unittest.main()
