from typing import TypedDict
from logistics_tool_using_rag_agent import get_shipment_details
from langgraph.graph import StateGraph, START, END


from logistics_semantic_search_agent import (
    load_logistics_documents,
    build_semantic_index,
)

# Exercise 012 — Multi-Agent Freight Operations System
# Phase 1: Shared State and Agent Contracts


class FreightState(TypedDict):
    shipment_id: str
    status: str
    errors: list[str]

    shipment: dict
    policies: list[dict]

    exception_analysis: dict
    decision: dict

    agent_history: list[str]


def create_initial_state(shipment_id: str) -> FreightState:
    """Create a consistent initial state for the freight workflow."""

    return {
        "shipment_id": shipment_id,
        "status": "pending",
        "errors": [],
        "shipment": {},
        "policies": [],
        "exception_analysis": {},
        "decision": {},
        "agent_history": [],
    }


def shipment_agent(state: FreightState) -> dict:
    """Retrieve shipment information from the existing database."""

    shipment_id = state["shipment_id"]

    print(f"Shipment Agent: Looking up {shipment_id}...")

    try:
        shipment = get_shipment_details(shipment_id)

        if "error" in shipment:
            return {
                "status": "not_found",
                "shipment": {},
                "errors": [shipment["error"]],
                "agent_history": ["Shipment Agent: shipment not found"],
            }

        return {
            "status": "retrieved",
            "shipment": shipment,
            "errors": [],
            "agent_history": ["Shipment Agent: shipment retrieved"],
        }

    except Exception as exc:
        return {
            "status": "lookup_failed",
            "shipment": {},
            "errors": [str(exc)],
            "agent_history": ["Shipment Agent: lookup failed"],
        }


def validate_shipment_agent(state: FreightState) -> dict:
    """Validate required shipment information before further processing."""

    print("Shipment Validation Agent: Checking shipment data...")

    shipment = state.get("shipment", {})

    required_fields = [
        "shipment_id",
        "status",
        "issue_type",
        "priority",
        "description",
        "delivery_confirmed",
    ]

    missing_fields = []

    for field in required_fields:
        if field not in shipment or shipment[field] is None:
            missing_fields.append(field)
        elif isinstance(shipment[field], str) and not shipment[field].strip():
            missing_fields.append(field)

    if missing_fields:
        return {
            "status": "validation_failed",
            "errors": [f"Missing required field: {field}" for field in missing_fields],
            "agent_history": state["agent_history"] + ["Shipment Validation: failed"],
        }

    return {
        "status": "validated",
        "errors": [],
        "agent_history": state["agent_history"] + ["Shipment Validation: passed"],
    }


def policy_agent(state: FreightState) -> dict:
    """Retrieve relevant logistics policies using semantic search."""

    print("Policy Agent: Retrieving relevant logistics policies...")

    if state.get("status") != "validated":
        return {
            "errors": state.get("errors", [])
            + ["Policy retrieval requires a validated shipment."],
            "agent_history": state["agent_history"]
            + ["Policy Agent: skipped - shipment not validated"],
        }

    shipment = state["shipment"]

    question = (
        f"Logistics procedures for {shipment['issue_type']}. "
        f"Priority: {shipment['priority']}. "
        f"Shipment details: {shipment['description']}"
    )

    try:
        documents = load_logistics_documents()
        index = build_semantic_index(documents)

        retriever = index.as_retriever(similarity_top_k=3)
        results = retriever.retrieve(question)

        policies = [
            {
                "filename": result.node.metadata.get("file_name", "Unknown"),
                "score": (float(result.score) if result.score is not None else None),
                "excerpt": result.node.text[:500],
            }
            for result in results
        ]

        if not policies:
            return {
                "status": "policy_not_found",
                "policies": [],
                "errors": ["No relevant logistics policies were retrieved."],
                "agent_history": state["agent_history"]
                + ["Policy Agent: no policies retrieved"],
            }

        return {
            "status": "policies_retrieved",
            "policies": policies,
            "errors": [],
            "agent_history": state["agent_history"]
            + [f"Policy Agent: retrieved {len(policies)} policies"],
        }

    except Exception as exc:
        return {
            "status": "policy_retrieval_failed",
            "policies": [],
            "errors": [str(exc)],
            "agent_history": state["agent_history"]
            + ["Policy Agent: retrieval failed"],
        }


def exception_analysis_agent(state: FreightState) -> dict:
    """Analyze a validated shipment exception using available evidence."""

    print("Exception Analysis Agent: Analyzing shipment exception...")

    if state.get("status") != "policies_retrieved":
        return {
            "errors": state.get("errors", [])
            + ["Exception analysis requires retrieved policies."],
            "agent_history": state["agent_history"]
            + ["Exception Analysis Agent: skipped - policies unavailable"],
        }

    shipment = state["shipment"]
    policies = state.get("policies", [])

    issue_type = shipment["issue_type"]
    priority = shipment["priority"]
    delivery_confirmed = shipment["delivery_confirmed"]

    issue_normalized = issue_type.lower()

    if "damag" in issue_normalized:
        operational_concern = "Possible shipment damage"
        suggested_action = (
            "Inspect the shipment, document visible damage, "
            "and request operational review before release."
        )
    elif "delay" in issue_normalized:
        operational_concern = "Delivery delay"
        suggested_action = (
            "Verify shipment tracking and carrier updates, "
            "then communicate a confirmed delivery estimate."
        )
    else:
        operational_concern = "Shipment exception requiring assessment"
        suggested_action = (
            "Review shipment details and relevant policies "
            "before determining the next action."
        )

    requires_human_review = (
        priority.lower() in ("high", "critical") or "damag" in issue_normalized
    )

    analysis = {
        "shipment_id": shipment["shipment_id"],
        "issue_type": issue_type,
        "priority": priority,
        "delivery_confirmed": delivery_confirmed,
        "operational_concern": operational_concern,
        "suggested_action": suggested_action,
        "supporting_policies": [policy["filename"] for policy in policies],
        "requires_human_review": requires_human_review,
    }

    return {
        "status": "exception_analyzed",
        "exception_analysis": analysis,
        "errors": [],
        "agent_history": state["agent_history"]
        + ["Exception Analysis Agent: analysis completed"],
    }


def operational_decision_agent(state: FreightState) -> dict:
    """Generate a structured operational recommendation."""

    print("Operational Decision Agent: Preparing recommendation...")

    if state.get("status") != "exception_analyzed":
        return {
            "errors": state.get("errors", [])
            + ["Operational decision requires exception analysis."],
            "agent_history": state["agent_history"]
            + ["Operational Decision Agent: skipped - analysis unavailable"],
        }

    analysis = state["exception_analysis"]

    requires_review = analysis["requires_human_review"]

    decision = {
        "shipment_id": analysis["shipment_id"],
        "issue_type": analysis["issue_type"],
        "priority": analysis["priority"],
        "recommended_action": analysis["suggested_action"],
        "supporting_policies": analysis["supporting_policies"],
        "requires_human_review": requires_review,
        "approval_status": (
            "pending_human_review" if requires_review else "recommendation_only"
        ),
        "execution_authorized": False,
    }

    return {
        "status": "decision_prepared",
        "decision": decision,
        "errors": [],
        "agent_history": state["agent_history"]
        + ["Operational Decision Agent: recommendation prepared"],
    }


def route_after_shipment(state: FreightState) -> str:
    """Continue only if shipment retrieval succeeded."""
    return "found" if state["status"] == "retrieved" else "stop"


def route_after_validation(state: FreightState) -> str:
    """Continue only if shipment validation succeeded."""
    return "valid" if state["status"] == "validated" else "stop"


def route_after_policies(state: FreightState) -> str:
    """Continue only if relevant policies were retrieved."""
    return "ready" if state["status"] == "policies_retrieved" else "stop"


def build_multi_agent_workflow():
    """Build and compile the freight operations workflow."""

    workflow = StateGraph(FreightState)

    workflow.add_node("shipment", shipment_agent)
    workflow.add_node("validation", validate_shipment_agent)
    workflow.add_node("policies", policy_agent)
    workflow.add_node("analysis", exception_analysis_agent)
    workflow.add_node("decision", operational_decision_agent)

    workflow.add_edge(START, "shipment")

    workflow.add_conditional_edges(
        "shipment",
        route_after_shipment,
        {
            "found": "validation",
            "stop": END,
        },
    )

    workflow.add_conditional_edges(
        "validation",
        route_after_validation,
        {
            "valid": "policies",
            "stop": END,
        },
    )

    workflow.add_conditional_edges(
        "policies",
        route_after_policies,
        {
            "ready": "analysis",
            "stop": END,
        },
    )

    workflow.add_conditional_edges(
        "analysis",
        route_after_analysis,
        {
            "analyzed": "decision",
            "stop": END,
        },
    )

    workflow.add_edge("decision", END)

    return workflow.compile()


def route_after_analysis(state: FreightState) -> str:
    """Continue only if exception analysis succeeded."""
    return "analyzed" if state["status"] == "exception_analyzed" else "stop"


if __name__ == "__main__":
    print("EXERCISE 012 — SHIPMENT AGENT VALIDATION")
    print("-" * 55)

    for shipment_id in ["SHP-1045", "SHP-9999"]:
        print(f"\nTesting shipment: {shipment_id}")

        state = create_initial_state(shipment_id)

        lookup_result = shipment_agent(state)
        state.update(lookup_result)

        print(f"Lookup status: {state['status']}")

        if state["status"] == "retrieved":
            validation_result = validate_shipment_agent(state)
            state.update(validation_result)

            print(f"Validation status: {state['status']}")
        else:
            print("Validation skipped: shipment not available.")

        print(f"Errors: {state['errors']}")
        print(f"Agent history: {state['agent_history']}")

    print("\nTesting incomplete shipment:")

    incomplete_state = create_initial_state("SHP-TEST")
    incomplete_state["shipment"] = {
        "shipment_id": "SHP-TEST",
        "status": "On Hold",
    }

    validation_result = validate_shipment_agent(incomplete_state)
    incomplete_state.update(validation_result)

    print(f"Validation status: {incomplete_state['status']}")
    print(f"Errors: {incomplete_state['errors']}")
    print(f"Agent history: {incomplete_state['agent_history']}")

    print("\nTesting Policy Agent:")

    state = create_initial_state("SHP-1045")
    state.update(shipment_agent(state))

    if state["status"] == "retrieved":
        state.update(validate_shipment_agent(state))

    if state["status"] == "validated":
        state.update(policy_agent(state))

    print(f"Final status: {state['status']}")
    print(f"Policies retrieved: {len(state['policies'])}")

    for policy in state["policies"]:
        print(f"Filename: {policy['filename']}")
        print(f"Similarity score: {policy['score']}")

    print(f"Errors: {state['errors']}")
    print(f"Agent history: {state['agent_history']}")

    print("\nTesting Exception Analysis Agent:")

    state = create_initial_state("SHP-1045")
    state.update(shipment_agent(state))

    if state["status"] == "retrieved":
        state.update(validate_shipment_agent(state))

    if state["status"] == "validated":
        state.update(policy_agent(state))

    if state["status"] == "policies_retrieved":
        state.update(exception_analysis_agent(state))

    print(f"Final status: {state['status']}")
    print(f"Exception analysis: {state['exception_analysis']}")
    print(f"Errors: {state['errors']}")
    print(f"Agent history: {state['agent_history']}")

    print("\nTesting Operational Decision Agent:")

    state = create_initial_state("SHP-1045")
    state.update(shipment_agent(state))

    if state["status"] == "retrieved":
        state.update(validate_shipment_agent(state))

    if state["status"] == "validated":
        state.update(policy_agent(state))

    if state["status"] == "policies_retrieved":
        state.update(exception_analysis_agent(state))

    if state["status"] == "exception_analyzed":
        state.update(operational_decision_agent(state))

    print(f"Final status: {state['status']}")
    print(f"Decision: {state['decision']}")
    print(f"Errors: {state['errors']}")
    print(f"Agent history: {state['agent_history']}")

    print("\nEXERCISE 012 - MULTI-AGENT WORKFLOW")

    app = build_multi_agent_workflow()

    for shipment_id in ["SHP-1045", "SHP-9999"]:
        print(f"\nTesting workflow: {shipment_id}")

        initial_state = create_initial_state(shipment_id)
        result = app.invoke(initial_state)

        print(f"Final status: {result['status']}")
        print(f"Errors: {result['errors']}")
        print(f"Agent history: {result['agent_history']}")
        print(f"Decision: {result['decision']}")
