from typing import TypedDict
from langgraph.graph import StateGraph, START, END


class ShipmentState(TypedDict):
    shipment_id: str
    status: str
    exception_type: str
    description: str
    priority: str
    assigned_department: str
    recommended_action: str
    requires_human_review: bool


shipment_001: ShipmentState = {
    "shipment_id": "SHP-001",
    "status": "in_transit",
    "exception_type": "delay",
    "description": "Shipment delayed by 48 hours.",
    "priority": "pending",
    "assigned_department": "unassigned",
    "recommended_action": "pending",
    "requires_human_review": False,
}


def evaluate_shipment(state: ShipmentState) -> dict:
    exception_type = state["exception_type"]

    if exception_type == "delay":
        priority = "medium"
    elif exception_type == "documentation":
        priority = "high"
    elif exception_type == "damage":
        priority = "critical"
    elif exception_type == "none":
        priority = "low"
    else:
        priority = "unknown"

    return {"priority": priority}


def route_shipment(state: ShipmentState) -> str:
    exception_type = state["exception_type"]

    if exception_type == "delay":
        return "handle_delay"
    elif exception_type == "documentation":
        return "handle_documentation"
    elif exception_type == "damage":
        return "handle_damage"
    elif exception_type == "none":
        return "handle_normal"

    return "handle_unknown"


def handle_delay(state: ShipmentState) -> dict:
    return {
        "assigned_department": "Transportation Operations",
        "recommended_action": "Contact carrier and request updated ETA.",
        "requires_human_review": False,
    }


def handle_documentation(state: ShipmentState) -> dict:
    return {
        "assigned_department": "Documentation & Compliance",
        "recommended_action": "Verify missing or incorrect shipping documents.",
        "requires_human_review": True,
    }


def handle_damage(state: ShipmentState) -> dict:
    return {
        "assigned_department": "Claims & Quality Assurance",
        "recommended_action": "Document damage and initiate claims review.",
        "requires_human_review": True,
    }


def handle_normal(state: ShipmentState) -> dict:
    return {
        "assigned_department": "Logistics Operations",
        "recommended_action": "Continue standard shipment monitoring.",
        "requires_human_review": False,
    }


def handle_unknown(state: ShipmentState) -> dict:
    return {
        "assigned_department": "Operations Supervisor",
        "recommended_action": "Investigate unclassified shipment exception.",
        "requires_human_review": True,
    }


# Build the shipment exception workflow
builder = StateGraph(ShipmentState)

# Register workflow nodes
builder.add_node("evaluate", evaluate_shipment)
builder.add_node("handle_delay", handle_delay)
builder.add_node("handle_documentation", handle_documentation)
builder.add_node("handle_damage", handle_damage)
builder.add_node("handle_normal", handle_normal)
builder.add_node("handle_unknown", handle_unknown)

# Define the starting point
builder.add_edge(START, "evaluate")

# Route shipments based on exception type
builder.add_conditional_edges(
    "evaluate",
    route_shipment,
    {
        "handle_delay": "handle_delay",
        "handle_documentation": "handle_documentation",
        "handle_damage": "handle_damage",
        "handle_normal": "handle_normal",
        "handle_unknown": "handle_unknown",
    },
)

# Finish after the selected operational node
builder.add_edge("handle_delay", END)
builder.add_edge("handle_documentation", END)
builder.add_edge("handle_damage", END)
builder.add_edge("handle_normal", END)
builder.add_edge("handle_unknown", END)

# Compile the workflow
shipment_graph = builder.compile()

if __name__ == "__main__":
    print("Shipment loaded successfully!")
    print(shipment_001)

    result = evaluate_shipment(shipment_001)

    print("\nShipment evaluation:")
    print(result)

    route = route_shipment(shipment_001)

    print("\nSelected shipment route:")
    print(route)


    delay_result = handle_delay(shipment_001)

    print("\nDelay handling result:")
    print(delay_result)

    # Execute the complete LangGraph workflow
    final_state = shipment_graph.invoke(shipment_001)

    print("\nFinal shipment state:")
    print(final_state)

    # Validate the workflow with multiple shipment scenarios
    test_scenarios = [
        ("SHP-002", "documentation"),
        ("SHP-003", "damage"),
        ("SHP-004", "none"),
        ("SHP-005", "unknown"),
    ]

    for shipment_id, exception_type in test_scenarios:
        test_shipment = shipment_001.copy()
        test_shipment["shipment_id"] = shipment_id
        test_shipment["exception_type"] = exception_type

        # Reset workflow output fields
        test_shipment["priority"] = "pending"
        test_shipment["assigned_department"] = "unassigned"
        test_shipment["recommended_action"] = "pending"
        test_shipment["requires_human_review"] = False

        result = shipment_graph.invoke(test_shipment)

        print(f"\nShipment: {shipment_id}")
        print(f"Exception: {exception_type}")
        print(f"Priority: {result['priority']}")
        print(f"Department: {result['assigned_department']}")
        print(f"Action: {result['recommended_action']}")
        print(f"Human Review: {result['requires_human_review']}")
