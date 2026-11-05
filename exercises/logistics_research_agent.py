"""Exercise 014 — Logistics Research & Decision Support Agent."""

import json
import sys
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent / "projects" / "logistics_research"

sys.path.insert(0, str(PROJECT_DIR))

from research_workflow import run_research_workflow


def main():
    """Run the integrated logistics research workflow."""
    print("=== Exercise 014: Logistics Research & Decision Support ===")

    for shipment_id in ("SHP-001", "SHP-002"):
        print(f"\n--- Shipment: {shipment_id} ---")

        report = run_research_workflow(shipment_id)

        print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
