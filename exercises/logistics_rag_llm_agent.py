from smolagents import ToolCallingAgent, LiteLLMModel, tool

from logistics_tool_using_rag_agent import (
    get_shipment_details,
    search_logistics_policy,
)

from logistics_semantic_search_agent import (
    build_semantic_index,
    load_logistics_documents,
)


@tool
def lookup_shipment(shipment_id: str) -> dict:
    """
    Retrieve a shipment record by its shipment ID.

    Args:
        shipment_id: The shipment identifier, such as SHP-1045.

    Returns:
        Shipment information or an error if the shipment is not found.
    """
    shipment = get_shipment_details(shipment_id)

    validation = validate_shipment(shipment)

    if not validation["valid"]:
        return {
            "error": "Shipment validation failed.",
            "shipment_id": shipment_id,
            "details": validation["errors"],
        }

    return shipment


@tool
def search_policy(question: str) -> list[dict]:
    """
    Search logistics policies using semantic retrieval.

    Args:
        question: A logistics question used to find relevant policies.

    Returns:
        A list of relevant logistics policies.
    """
    documents = load_logistics_documents()
    index = build_semantic_index(documents)

    return search_logistics_policy(index, question)


def validate_shipment(shipment: dict) -> dict:
    """Validate shipment data before generating a logistics report."""

    if not isinstance(shipment, dict):
        return {
            "valid": False,
            "errors": ["Shipment data must be a dictionary."],
        }

    if shipment.get("error"):
        return {
            "valid": False,
            "errors": [str(shipment["error"])],
        }

    required_fields = [
        "shipment_id",
        "customer",
        "status",
        "issue_type",
        "priority",
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
            "valid": False,
            "errors": [f"Missing required fields: {', '.join(missing_fields)}"],
        }

    if not isinstance(shipment["delivery_confirmed"], bool):
        return {
            "valid": False,
            "errors": ["delivery_confirmed must be a boolean."],
        }

    return {
        "valid": True,
        "errors": [],
    }


def investigate_shipment(shipment_id: str) -> dict:
    """Investigate a shipment using validated data and retrieved policies."""

    shipment = get_shipment_details(shipment_id)
    validation = validate_shipment(shipment)

    if not validation["valid"]:
        return {
            "success": False,
            "shipment_id": shipment_id,
            "errors": validation["errors"],
        }

    documents = load_logistics_documents()
    index = build_semantic_index(documents)

    question = (
        f"Logistics procedures for {shipment['issue_type']}. "
        f"Shipment status: {shipment['status']}. "
        f"Priority: {shipment['priority']}. "
        "Find applicable handling and escalation policies."
    )

    policies = search_logistics_policy(index, question)

    return {
        "success": True,
        "shipment": shipment,
        "policy_query": question,
        "policies": policies,
    }


def generate_reliable_report(shipment_id: str) -> dict:
    """Generate a structured report using verified shipment data."""

    investigation = investigate_shipment(shipment_id)

    if not investigation["success"]:
        return {
            "success": False,
            "shipment_id": shipment_id,
            "errors": investigation["errors"],
        }

    shipment = investigation["shipment"]
    retrieved_policies = investigation["policies"]

    applicable_policies = []
    excluded_policies = []

    issue_type = shipment["issue_type"].strip().lower()
    status = shipment["status"].strip().lower()
    description = shipment.get("description", "").lower()

    delay_evidence = (
        "delay" in issue_type
        or "delayed" in status
        or "past the expected delivery" in description
    )

    for policy in retrieved_policies:
        filename = policy["policy"]

        if filename == "delayed_delivery_policy.txt" and not delay_evidence:
            excluded_policies.append(
                {
                    "policy": filename,
                    "reason": "No verified evidence of a delivery delay.",
                }
            )
            continue

        applicable_policies.append(
            {
                "policy": filename,
                "similarity_score": policy["similarity_score"],
            }
        )

    return {
        "success": True,
        "shipment_id": shipment["shipment_id"],
        "customer": shipment["customer"],
        "status": shipment["status"],
        "issue_type": shipment["issue_type"],
        "priority": shipment["priority"],
        "delivery_confirmed": shipment["delivery_confirmed"],
        "description": shipment.get("description", ""),
        "applicable_policies": applicable_policies,
        "excluded_policies": excluded_policies,
        "report_source": "Validated shipment data and retrieved policies",
    }


@tool
def get_reliable_shipment_report(shipment_id: str) -> dict:
    """
    Generate a validated, evidence-based shipment report.

    Args:
        shipment_id: The shipment identifier, such as SHP-1045.

    Returns:
        A structured shipment report with applicable and excluded policies,
        or validation errors when the shipment cannot be investigated.
    """
    return generate_reliable_report(shipment_id)


def create_agent():
    model = LiteLLMModel(
        model_id="ollama_chat/qwen2.5:3b",
        api_base="http://localhost:11434",
        api_key="ollama",
        num_ctx=4096,
    )

    return ToolCallingAgent(
        tools=[
            lookup_shipment,
            search_policy,
            get_reliable_shipment_report,
        ],
        model=model,
        max_steps=4,
    )


if __name__ == "__main__":
    agent = create_agent()

    response = agent.run(
        "Investigate shipment SHP-1045. "
        "First, call lookup_shipment to retrieve the shipment record. "
        "Then, call search_policy using the shipment's actual issue type, "
        "status, and priority to find relevant handling and escalation procedures. "
        "Report the customer, shipment status, issue type, priority, "
        "and delivery confirmation status. "
        "Identify which retrieved policies are applicable and explain "
        "the operational actions supported by those policies. "
        "Do not assume the shipment is delayed without evidence. "
        "Do not invent missing information."
    )

    print("\nFINAL AGENT RESPONSE")
    print(response)
