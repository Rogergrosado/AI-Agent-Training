import json

from shipment_analysis import (
    get_shipment_by_id,
    generate_decision_report,
)
from research_tools import generate_research_query
from external_research import search_external_sources
from evidence_quality import evaluate_evidence


def run_research_workflow(shipment_id, max_results=3):
    """Combine shipment analysis with external research."""

    shipment = get_shipment_by_id(shipment_id)

    if shipment is None:
        raise ValueError(f"Shipment not found: {shipment_id}")

    decision_report = generate_decision_report(shipment)

    if not decision_report["requires_external_research"]:
        return {
            "shipment_id": shipment_id,
            "decision_report": decision_report,
            "research_status": "not_required",
            "research_query": None,
            "external_sources": [],
            "evidence_assessments": [],
            "research_error": None,
        }

    research_query = generate_research_query(shipment)

    research_response = search_external_sources(
        research_query,
        max_results=max_results,
    )

    evidence_assessments = [
        evaluate_evidence(source, research_query)
        for source in research_response["results"]
    ]

    return {
        "shipment_id": shipment_id,
        "decision_report": decision_report,
        "research_status": research_response["status"],
        "research_query": research_query,
        "external_sources": research_response["results"],
        "evidence_assessments": evidence_assessments,
        "research_error": research_response["error"],
    }


if __name__ == "__main__":
    print("=== Exercise 014: Integrated Research Workflow ===")

    for shipment_id in ["SHP-001", "SHP-002"]:
        report = run_research_workflow(shipment_id)

        print("\n" + "=" * 50)
        print(json.dumps(report, indent=2, ensure_ascii=False))
