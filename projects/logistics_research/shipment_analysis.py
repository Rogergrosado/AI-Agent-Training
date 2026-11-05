import json
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parent / "data" / "shipments.json"


def load_shipments():
    """Load shipment records from the local JSON dataset."""

    with DATA_PATH.open("r", encoding="utf-8") as file:
        shipments = json.load(file)

    if not isinstance(shipments, list):
        raise ValueError("Shipment dataset must contain a JSON list.")

    return shipments


def get_shipment_by_id(shipment_id):
    """Find a shipment using its unique identifier."""

    shipments = load_shipments()

    for shipment in shipments:
        if shipment["shipment_id"] == shipment_id:
            return shipment

    return None


def classify_shipment(shipment):
    """Classify a shipment using deterministic business rules."""

    status = shipment["status"]
    priority = shipment["priority"]

    if priority == "critical":
        return {
            "classification": "critical",
            "recommended_action": "Escalate immediately",
        }

    if status == "customs_hold":
        return {
            "classification": "customs_hold",
            "recommended_action": "Review customs documentation",
        }

    if status == "delayed":
        return {
            "classification": "delayed",
            "recommended_action": "Investigate shipment delay",
        }

    if status == "in_transit":
        return {
            "classification": "normal",
            "recommended_action": "Continue monitoring",
        }

    raise ValueError(f"Unsupported shipment status: {status}")


def generate_decision_report(shipment):
    """Generate an evidence-based operational report."""

    classification = classify_shipment(shipment)

    return {
        "shipment_id": shipment["shipment_id"],
        "origin": shipment["origin"],
        "destination": shipment["destination"],
        "status": shipment["status"],
        "priority": shipment["priority"],
        "classification": classification["classification"],
        "recommended_action": classification["recommended_action"],
        "exception": shipment["exception"],
        "evidence_source": "local_shipment_dataset",
        "requires_external_research": (classification["classification"] != "normal"),
    }


if __name__ == "__main__":

    print("=== Exercise 014: Decision Support Reports ===")

    shipments = load_shipments()

    for shipment in shipments:
        report = generate_decision_report(shipment)

        print("\n" + "=" * 50)
        print(json.dumps(report, indent=4))
