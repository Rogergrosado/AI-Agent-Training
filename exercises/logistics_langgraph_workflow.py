from typing import TypedDict

from langgraph.graph import END, START, StateGraph
from logistics_tool_using_rag_agent import get_shipment_details
from logistics_semantic_search_agent import (
    load_logistics_documents,
    build_semantic_index,
)

# Exercise 011 - Reliable Logistics Workflows with LangGraph
# Phase 2: Workflow State and First Node


class ShipmentState(TypedDict):
    shipment_id: str
    status: str
    errors: list[str]
    shipment: dict
    policies: list[dict]
    decision: dict


def initialize_shipment(state: ShipmentState) -> dict:
    """Initialize the shipment investigation workflow."""

    shipment_id = state["shipment_id"]

    print(f"Initializing investigation for {shipment_id}")

    return {
        "status": "initialized",
        "errors": [],
        "policies": [],
        "decision": {},
    }


def lookup_shipment(state: ShipmentState) -> dict:
    """Retrieve shipment data from the Exercise 010 database."""

    shipment_id = state["shipment_id"]

    print(f"Looking up shipment: {shipment_id}")

    shipment = get_shipment_details(shipment_id)

    if "error" in shipment:
        return {
            "status": "not_found",
            "shipment": {},
            "errors": [shipment["error"]],
        }

    return {
        "status": "retrieved",
        "shipment": shipment,
        "errors": [],
    }


def route_after_lookup(state: ShipmentState) -> str:
    """Choose the next workflow path based on shipment retrieval."""

    if state["status"] == "retrieved":
        return "found"

    return "not_found"


def validate_shipment(state: ShipmentState) -> dict:
    """Validate required shipment fields before further processing."""

    print("Validating shipment data...")

    shipment = state.get("shipment", {})

    required_fields = [
        "shipment_id",
        "customer",
        "status",
        "issue_type",
        "priority",
        "description",
        "delivery_confirmed",
    ]

    missing_fields = [
        field
        for field in required_fields
        if field not in shipment
        or shipment[field] is None
        or (isinstance(shipment[field], str) and not shipment[field].strip())
    ]

    if missing_fields:
        return {
            "status": "validation_failed",
            "errors": [f"Missing required field: {field}" for field in missing_fields],
        }

    return {
        "status": "validated",
        "errors": [],
    }


def retrieve_policies(state: ShipmentState) -> dict:
    """Retrieve relevant logistics policies for a validated shipment."""
    print("Retrieving relevant logistics policies...")

    shipment = state["shipment"]

    question = (
        f"What logistics policies apply to a shipment with "
        f"issue type '{shipment['issue_type']}', "
        f"priority '{shipment['priority']}', "
        f"and description '{shipment['description']}'?"
    )

    try:
        documents = load_logistics_documents()
        index = build_semantic_index(documents)

        retriever = index.as_retriever(similarity_top_k=3)
        results = retriever.retrieve(question)

        policies = [
            {
                "filename": result.node.metadata.get("file_name", "Unknown"),
                "score": float(result.score) if result.score is not None else None,
                "excerpt": result.node.text[:500],
            }
            for result in results
        ]

        return {
            "status": "policies_retrieved",
            "policies": policies,
            "errors": [],
        }

    except Exception as exc:
        return {
            "status": "retrieval_failed",
            "policies": [],
            "errors": [str(exc)],
        }


def evaluate_shipment(state: ShipmentState) -> dict:
    """Evaluate the shipment using retrieved logistics policies."""
    print("Evaluating shipment and retrieved policies...")

    shipment = state["shipment"]
    policies = state.get("policies", [])

    if not policies:
        return {
            "status": "evaluation_failed",
            "decision": {},
            "errors": ["No logistics policies were retrieved."],
        }

    decision = {
        "shipment_id": shipment["shipment_id"],
        "issue_type": shipment["issue_type"],
        "priority": shipment["priority"],
        "recommended_action": "Review retrieved policies and escalate for operational assessment.",
        "supporting_policies": [policy["filename"] for policy in policies],
        "requires_human_review": True,
    }

    return {
        "status": "evaluated",
        "decision": decision,
        "errors": [],
    }


def route_after_validation(state: ShipmentState) -> str:
    """Continue only when shipment data is valid."""
    if state["status"] == "validated":
        return "valid"

    return "invalid"


def test_incomplete_shipment():
    """Test shipment validation with missing required fields."""

    test_state = {
        "shipment_id": "SHP-TEST",
        "status": "retrieved",
        "errors": [],
        "shipment": {
            "shipment_id": "SHP-TEST",
            "customer": "Test Customer",
        },
        "policies": [],
        "decision": {},
    }

    result = validate_shipment(test_state)

    print("\nIncomplete shipment validation result:")
    print(result)


def test_validation_failure_workflow():
    """Test that invalid shipment data stops the workflow."""

    def incomplete_lookup(state: ShipmentState) -> dict:
        return {
            "status": "retrieved",
            "shipment": {
                "shipment_id": state["shipment_id"],
                "customer": "Test Customer",
            },
            "errors": [],
        }

    workflow = StateGraph(ShipmentState)

    workflow.add_node("initialize", initialize_shipment)
    workflow.add_node("lookup", incomplete_lookup)
    workflow.add_node("validate", validate_shipment)
    workflow.add_node("retrieve_policies", retrieve_policies)
    workflow.add_node("evaluate", evaluate_shipment)

    workflow.add_edge(START, "initialize")
    workflow.add_edge("initialize", "lookup")
    workflow.add_edge("lookup", "validate")

    workflow.add_conditional_edges(
        "validate",
        route_after_validation,
        {
            "valid": "retrieve_policies",
            "invalid": END,
        },
    )

    workflow.add_edge("retrieve_policies", "evaluate")
    workflow.add_edge("evaluate", END)

    app = workflow.compile()

    result = app.invoke(
        {
            "shipment_id": "SHP-TEST",
            "status": "pending",
            "errors": [],
            "shipment": {},
            "policies": [],
            "decision": {},
        }
    )

    print("\nValidation failure workflow result:")
    print(result)


def build_workflow():
    """Build and compile the shipment lookup workflow."""

    workflow = StateGraph(ShipmentState)

    workflow.add_node("initialize", initialize_shipment)
    workflow.add_node("lookup", lookup_shipment)
    workflow.add_node("validate", validate_shipment)
    workflow.add_node("retrieve_policies", retrieve_policies)

    workflow.add_edge(START, "initialize")
    workflow.add_edge("initialize", "lookup")

    workflow.add_conditional_edges(
        "lookup",
        route_after_lookup,
        {
            "found": "validate",
            "not_found": END,
        },
    )

    workflow.add_conditional_edges(
        "validate",
        route_after_validation,
        {
            "valid": "retrieve_policies",
            "invalid": END,
        },
    )

    workflow.add_node("evaluate", evaluate_shipment)
    workflow.add_conditional_edges(
        "retrieve_policies",
        lambda state: (
            "ready" if state["status"] == "policies_retrieved" else "failed"
        ),
        {
            "ready": "evaluate",
            "failed": END,
        },
    )

    workflow.add_edge("evaluate", END)

    return workflow.compile()


def run_workflow_tests():
    """Run automated assertions for the logistics workflow."""

    print("\nRunning Exercise 011 workflow tests...")

    app = build_workflow()

    # Test 1: Existing shipment
    valid_result = app.invoke(
        {
            "shipment_id": "SHP-1045",
            "status": "pending",
            "errors": [],
            "shipment": {},
            "policies": [],
            "decision": {},
        }
    )

    assert valid_result["status"] == "evaluated"
    assert valid_result["policies"]
    assert valid_result["decision"]["requires_human_review"] is True

    print("PASS: Valid shipment workflow")

    # Test 2: Nonexistent shipment
    missing_result = app.invoke(
        {
            "shipment_id": "SHP-9999",
            "status": "pending",
            "errors": [],
            "shipment": {},
            "policies": [],
            "decision": {},
        }
    )

    assert missing_result["status"] == "not_found"
    assert missing_result["errors"]
    assert missing_result["policies"] == []
    assert missing_result["decision"] == {}

    print("PASS: Missing shipment workflow")

    # Test 3: Incomplete shipment validation
    incomplete_result = validate_shipment(
        {
            "shipment_id": "SHP-TEST",
            "status": "retrieved",
            "shipment": {
                "shipment_id": "SHP-TEST",
                "customer": "Test Customer",
            },
            "errors": [],
            "policies": [],
            "decision": {},
        }
    )

    assert incomplete_result["status"] == "validation_failed"
    assert len(incomplete_result["errors"]) == 5

    print("PASS: Incomplete shipment validation")
    print("\nAll automated workflow tests passed.")


if __name__ == "__main__":
    app = build_workflow()

    initial_state = {
        "shipment_id": "SHP-9999",
        "status": "pending",
        "errors": [],
        "shipment": {},
        "policies": [],
    }

    result = app.invoke(initial_state)

    print("\nWorkflow result:")
    print(result)
