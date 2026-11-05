import sys
import unittest
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_DIR))

from research_tools import generate_research_query


class TestResearchTools(unittest.TestCase):

    def setUp(self):
        self.shipment = {
            "shipment_id": "SHP-002",
            "origin": "Shanghai, China",
            "destination": "San Juan, Puerto Rico",
            "transport_mode": "ocean",
            "status": "delayed",
            "exception": "Port congestion causing shipment delays",
        }

    def test_generates_research_query(self):
        query = generate_research_query(self.shipment)

        self.assertIsInstance(query, str)
        self.assertIn("Shanghai, China", query)
        self.assertIn("San Juan, Puerto Rico", query)
        self.assertIn("Port congestion", query)

    def test_missing_required_field(self):
        shipment = self.shipment.copy()
        del shipment["origin"]

        with self.assertRaises(ValueError):
            generate_research_query(shipment)

    def test_empty_exception(self):
        shipment = self.shipment.copy()
        shipment["exception"] = ""

        with self.assertRaises(ValueError):
            generate_research_query(shipment)

    def test_invalid_field_type(self):
        shipment = self.shipment.copy()
        shipment["destination"] = None

        with self.assertRaises(ValueError):
            generate_research_query(shipment)

    def test_deterministic_output(self):
        first = generate_research_query(self.shipment)
        second = generate_research_query(self.shipment)

        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()
