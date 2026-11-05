"""
Exercise 014 — Logistics Research Tools

Generate research queries from shipment information.
This module does not perform live web searches yet.
"""


def generate_research_query(shipment: dict) -> str:
    """Generate a research query for a shipment exception."""

    required_fields = (
        "shipment_id",
        "origin",
        "destination",
        "transport_mode",
        "status",
        "exception",
    )

    for field in required_fields:
        value = shipment.get(field)

        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"Missing or invalid field: {field}")

    shipment_id = shipment["shipment_id"]
    origin = shipment["origin"]
    destination = shipment["destination"]
    transport_mode = shipment["transport_mode"]
    status = shipment["status"]
    exception = shipment["exception"]

    query = (
        f"Logistics disruption {transport_mode} shipment "
        f"from {origin} to {destination}: "
        f"{exception}. Current operational updates "
        f"and potential impact on shipment delays."
    )

    return query


if __name__ == "__main__":
    example_shipment = {
        "shipment_id": "SHP-002",
        "origin": "Shanghai, China",
        "destination": "San Juan, Puerto Rico",
        "transport_mode": "ocean",
        "status": "delayed",
        "exception": "Port congestion causing shipment delays",
    }

    print("=== Exercise 014: Research Query Generator ===")
    print(f"Shipment: {example_shipment['shipment_id']}")
    print(f"Research query: {generate_research_query(example_shipment)}")
