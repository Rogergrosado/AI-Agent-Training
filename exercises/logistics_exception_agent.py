from datetime import date
import json

from smolagents import tool, ToolCallingAgent, LiteLLMModel

# Simulated logistics database
shipments = {
    "SHP-001": {
        "status": "In Transit",
        "expected_delivery": "2026-10-30",
        "actual_delivery": None,
    },
    "SHP-002": {
        "status": "Delivered",
        "expected_delivery": "2026-10-25",
        "actual_delivery": "2026-10-25",
    },
    "SHP-003": {
        "status": "Delayed",
        "expected_delivery": "2026-10-26",
        "actual_delivery": None,
    },
    "SHP-004": {
        "status": "Delayed",
        "expected_delivery": "2026-10-23",
        "actual_delivery": None,
    },
    "SHP-005": {
        "status": "Delayed",
        "expected_delivery": "2026-10-24",
        "actual_delivery": None,
    },
}


def get_shipment(shipment_id):
    """Retrieve shipment information from our database."""
    return shipments.get(shipment_id)


def calculate_delay(shipment_id):
    """Calculate how many days a shipment is overdue."""

    shipment = get_shipment(shipment_id)

    if shipment is None:
        return "Shipment not found"

    if shipment["status"] == "Delivered":
        return 0

    expected_date = date.fromisoformat(shipment["expected_delivery"])
    reference_date = date(2026, 10, 28)

    delay_days = (reference_date - expected_date).days

    return max(0, delay_days)


def classify_priority(shipment_id):
    """Classify shipment exception priority."""

    delay = calculate_delay(shipment_id)

    if delay == "Shipment not found":
        return "UNKNOWN"

    if delay == 0:
        return "NONE"

    if delay <= 2:
        return "LOW"

    if delay <= 4:
        return "MEDIUM"

    return "HIGH"


def recommend_action(shipment_id):
    """Recommend an operational action based on shipment priority."""

    priority = classify_priority(shipment_id)

    actions = {
        "NONE": "No action required",
        "LOW": "Monitor shipment",
        "MEDIUM": "Contact carrier",
        "HIGH": "Escalate to logistics manager",
        "UNKNOWN": "Verify shipment ID",
    }

    return actions[priority]


def generate_exception_report(shipment_id):
    """Generate a structured logistics exception report."""

    shipment = get_shipment(shipment_id)

    if shipment is None:
        return {
            "shipment_id": shipment_id,
            "error": "Shipment not found",
            "recommended_action": "Verify shipment ID",
        }

    return {
        "shipment_id": shipment_id,
        "status": shipment["status"],
        "expected_delivery": shipment["expected_delivery"],
        "actual_delivery": shipment["actual_delivery"],
        "delay_days": calculate_delay(shipment_id),
        "priority": classify_priority(shipment_id),
        "recommended_action": recommend_action(shipment_id),
    }


@tool
def analyze_shipment_exception(shipment_id: str) -> str:
    """
    Analyze a shipment and return its operational exception report.

    Args:
        shipment_id: The shipment tracking ID, such as SHP-004.
    """
    report = generate_exception_report(shipment_id)

    return json.dumps(report, indent=2)


def create_logistics_agent():
    """Create a local AI agent for logistics exception analysis."""

    model = LiteLLMModel(
        model_id="ollama/qwen2:1.5b",
        api_base="http://localhost:11434",
        api_key="ollama",
    )

    agent = ToolCallingAgent(
        tools=[analyze_shipment_exception],
        model=model,
        max_steps=3,
    )

    return agent


# Test AI-powered shipment exception analysis

if __name__ == "__main__":
    print("\n=== AI LOGISTICS EXCEPTION TESTS ===")

    test_shipments = ["SHP-003", "SHP-004", "SHP-005", "SHP-999"]

    for shipment_id in test_shipments:
        print(f"\n=== TESTING {shipment_id} ===")

        # Create a fresh agent for each independent test
        agent = create_logistics_agent()

        response = agent.run(
            f"Analyze shipment {shipment_id}. "
            "Use the analyze_shipment_exception tool. "
            "Report the shipment ID, delay in days, "
            "priority, and recommended action. "
            "If the shipment is not found, say so clearly. "
            "Do not invent any information."
        )

        print(f"\n=== FINAL RESPONSE: {shipment_id} ===")
        print(response)
