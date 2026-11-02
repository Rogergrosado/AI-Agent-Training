import json
from pathlib import Path
from logistics_semantic_search_agent import (
    build_semantic_index,
    load_logistics_documents,
)

# Exercise 010 - Logistics Tool-Using RAG Agent
# Phase 2: Shipment Data Retrieval

BASE_DIR = Path(__file__).resolve().parent.parent
SHIPMENTS_FILE = BASE_DIR / "data" / "exercise_010" / "shipments.json"


def get_shipment_details(shipment_id: str) -> dict:
    """Retrieve shipment details using a shipment identifier."""

    if not SHIPMENTS_FILE.is_file():
        return {"error": "Shipment database not found."}

    try:
        with SHIPMENTS_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except (OSError, json.JSONDecodeError) as error:
        return {"error": f"Unable to read shipment database: {error}"}

    for shipment in data.get("shipments", []):
        if shipment.get("shipment_id") == shipment_id:
            return shipment

    return {"error": f"Shipment {shipment_id} not found."}


def search_logistics_policy(index, question: str) -> list[dict]:
    """Retrieve relevant logistics policies using semantic search."""

    retriever = index.as_retriever(similarity_top_k=3)
    results = retriever.retrieve(question)

    policies = []

    for result in results:
        policies.append(
            {
                "policy": result.node.metadata.get("file_name", "Unknown"),
                "similarity_score": (
                    round(float(result.score), 4) if result.score is not None else None
                ),
                "content": result.node.get_content(),
            }
        )

    return policies


def prioritize_policies(shipment: dict, policies: list[dict]) -> list[dict]:
    """Prioritize escalation policy for critical escalation incidents."""

    is_critical = str(shipment.get("priority", "")).strip().lower() == "critical"
    requires_escalation = (
        str(shipment.get("status", "")).strip().lower() == "escalation required"
    )

    if not (is_critical and requires_escalation):
        return policies

    escalation_policy = "shipment_escalation_policy.txt"

    return sorted(
        policies,
        key=lambda policy: (policy.get("policy") != escalation_policy),
    )


def investigate_shipment(index, shipment_id: str) -> dict:
    """Combine shipment lookup with semantic policy retrieval."""

    shipment = get_shipment_details(shipment_id)

    if "error" in shipment:
        return {
            "shipment_id": shipment_id,
            "status": "not_found",
            "error": shipment["error"],
            "policies": [],
        }

    question = (
        f"Logistics policy for {shipment['issue_type']}. "
        f"Incident description: {shipment['description']}"
    )

    policies = search_logistics_policy(index, question)
    policies = prioritize_policies(shipment, policies)

    return {
        "shipment_id": shipment_id,
        "status": "investigated",
        "shipment": shipment,
        "policy_query": question,
        "policies": policies,
    }


if __name__ == "__main__":
    print("=" * 55)
    print("EXERCISE 010 - SHIPMENT LOOKUP TEST")
    print("=" * 55)

    test_ids = ["SHP-1045", "SHP-2087", "SHP-3092", "SHP-9999"]

    for shipment_id in test_ids:
        print(f"\nLooking up shipment: {shipment_id}")

        result = get_shipment_details(shipment_id)

        print(json.dumps(result, indent=2))

    print("\n" + "=" * 55)
    print("EXERCISE 010 - SEMANTIC POLICY RETRIEVAL TEST")
    print("=" * 55)

    documents = load_logistics_documents()
    index = build_semantic_index(documents)

    question = (
        "A shipment arrived with damaged packaging. "
        "What procedures should the team follow?"
    )

    print(f"\nQuestion: {question}")

    policies = search_logistics_policy(index, question)

    for rank, policy in enumerate(policies, start=1):
        print(f"\nResult {rank}")
        print(f"Policy: {policy['policy']}")
        print(f"Similarity score: {policy['similarity_score']}")
        print(f"Content preview: {policy['content'][:200]}...")

    print("\n" + "=" * 55)
    print("EXERCISE 010 - INTEGRATED SHIPMENT INVESTIGATION")
    print("=" * 55)

    for shipment_id in ["SHP-1045", "SHP-2087", "SHP-3092", "SHP-9999"]:
        print(f"\nInvestigating shipment: {shipment_id}")
        if shipment_id == "SHP-3092":
            print("\nDEBUG - All retrieved policies:")
            for policy in report["policies"]:
                print(
                    f"{policy['policy']} | " f"Similarity: {policy['similarity_score']}"
                )

        report = investigate_shipment(index, shipment_id)

        print(f"Status: {report['status']}")

        if report["status"] == "not_found":
            print(f"Error: {report['error']}")
            continue

        shipment = report["shipment"]
        print(f"Customer: {shipment['customer']}")
        print(f"Issue: {shipment['issue_type']}")
        print(f"Priority: {shipment['priority']}")

        if report["policies"]:
            top_policy = report["policies"][0]
            print(f"Top policy: {top_policy['policy']}")
            print(f"Similarity: {top_policy['similarity_score']}")
        else:
            print("No relevant policies retrieved.")
