import sys
import unittest
from pathlib import Path
from unittest.mock import patch
from urllib.error import URLError

PROJECT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_DIR))

from external_research import search_external_sources


class TestExternalResearch(unittest.TestCase):

    @patch("external_research.urlopen")
    def test_successful_search(self, mock_urlopen):
        payload = b"""{
            "results": [
                {
                    "display_name": "Port Congestion Research",
                    "doi": "https://doi.org/10.1234/example",
                    "publication_date": "2026-01-01",
                    "primary_location": {
                        "source": {
                            "display_name": "Logistics Journal"
                        }
                    }
                }
            ]
        }"""

        mock_urlopen.return_value.__enter__.return_value.read.return_value = payload

        result = search_external_sources("port congestion")

        self.assertEqual(result["status"], "success")
        self.assertEqual(len(result["results"]), 1)
        self.assertEqual(result["results"][0]["title"], "Port Congestion Research")
        self.assertEqual(result["results"][0]["evidence_type"], "research_metadata")

    @patch("external_research.urlopen")
    def test_empty_results(self, mock_urlopen):
        mock_urlopen.return_value.__enter__.return_value.read.return_value = (
            b'{"results": []}'
        )

        result = search_external_sources("unknown research topic")

        self.assertEqual(result["status"], "success")
        self.assertEqual(result["results"], [])

    @patch("external_research.urlopen")
    def test_connection_error(self, mock_urlopen):
        mock_urlopen.side_effect = URLError("Connection failed")

        result = search_external_sources("port congestion")

        self.assertEqual(result["status"], "error")
        self.assertEqual(result["results"], [])
        self.assertIsNotNone(result["error"])

    def test_empty_query(self):
        with self.assertRaises(ValueError):
            search_external_sources("")

    def test_invalid_max_results(self):
        with self.assertRaises(ValueError):
            search_external_sources("port congestion", max_results=0)


if __name__ == "__main__":
    unittest.main()
