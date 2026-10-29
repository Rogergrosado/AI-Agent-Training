# Exercise 007 - Logistics Policy Decision Agent
# Hugging Face AI Agents Course - Unit 2.1: smolagents

import json

from logistics_exception_agent import generate_exception_report
from logistics_knowledge_agent import rank_policies
from smolagents import ToolCallingAgent, LiteLLMModel, tool


def validate_policy_decision(shipment, selected_policy):
    """
    Validate a shipment recommendation against
    the selected logistics policy.
    """

    if selected_policy["policy_id"] != "POL-001":
        return False

    delay_days = shipment["delay_days"]
    recommended_action = shipment["recommended_action"]

    if delay_days <= 0:
        return recommended_action == "No action required"

    if 1 <= delay_days <= 2:
        return recommended_action == "Monitor shipment"

    if 3 <= delay_days <= 4:
        return recommended_action == "Contact carrier"

    if delay_days >= 5:
        return recommended_action == "Escalate to logistics manager"

    return False


def generate_policy_decision(shipment_id):
    shipment = generate_exception_report(shipment_id)

    if "error" in shipment:
        return {
            "shipment_id": shipment_id,
            "status": "not_found",
            "message": shipment["error"],
            "delay_days": None,
            "recommended_action": "Verify shipment ID",
            "policy_id": None,
            "decision_supported": False,
        }

    delay_days = shipment["delay_days"]

    if delay_days == 0:
        policy_query = "shipment delayed"
    else:
        policy_query = "delayed shipment"

    policies = rank_policies(policy_query)

    if not policies:
        return {
            "shipment_id": shipment_id,
            "status": "policy_not_found",
            "shipment_analysis": shipment,
            "message": "No relevant company policy found.",
        }

    selected_policy = policies[0]

    return {
        "shipment_id": shipment_id,
        "shipment_status": shipment["status"],
        "delay_days": delay_days,
        "priority": shipment["priority"],
        "recommended_action": shipment["recommended_action"],
        "policy_id": selected_policy["policy_id"],
        "policy_title": selected_policy["title"],
        "policy_content": selected_policy["content"],
        "decision_supported": validate_policy_decision(shipment, selected_policy),
    }


def format_policy_decision(decision):
    """Create a reliable response from validated logistics data."""

    shipment_id = decision.get("shipment_id", "Unknown")
    status = decision.get("status")

    if status == "not_found":
        return (
            f"Shipment ID: {shipment_id}\n"
            "Status: Not found\n"
            "Recommended action: Verify shipment ID\n"
            "Policy ID: Not available\n"
            "Decision supported: False"
        )

    if status == "policy_not_found":
        return (
            f"Shipment ID: {shipment_id}\n"
            "Status: Policy not found\n"
            "Recommended action: Manual review required\n"
            "Policy ID: Not available\n"
            "Decision supported: False"
        )

    return (
        f"Shipment ID: {shipment_id}\n"
        f"Status: {decision['shipment_status']}\n"
        f"Delay: {decision['delay_days']} days\n"
        f"Priority: {decision['priority']}\n"
        f"Recommended action: {decision['recommended_action']}\n"
        f"Policy ID: {decision['policy_id']}\n"
        f"Decision supported: {decision['decision_supported']}"
    )


def run_reliable_policy_decision(shipment_id):
    """
    Produce a reliable operational report.

    The existing AI agent remains available for
    natural-language reasoning and tool calling.
    """
    decision = generate_policy_decision(shipment_id)

    return format_policy_decision(decision)


@tool
def evaluate_logistics_decision(shipment_id: str) -> str:
    """
    Evaluate a shipment against company logistics policies.

    Args:
        shipment_id: The shipment identifier, such as SHP-004.

    Returns:
        A JSON report containing the shipment analysis,
        relevant policy, and decision validation.
    """
    import json

    decision = generate_policy_decision(shipment_id)

    return json.dumps(decision, indent=2)


def create_policy_decision_agent():
    model = LiteLLMModel(
        model_id="ollama/qwen2:1.5b",
        api_base="http://localhost:11434",
        num_ctx=4096,
    )

    agent = ToolCallingAgent(
        tools=[evaluate_logistics_decision],
        model=model,
        max_steps=3,
    )

    return agent


if __name__ == "__main__":
    print("=== EXERCISE 007: POLICY DECISION TEST ===")

    for shipment_id in [
        "SHP-001",
        "SHP-002",
        "SHP-003",
        "SHP-004",
        "SHP-005",
        "SHP-999",
    ]:
        print(f"\n=== TESTING {shipment_id} ===")

        report = generate_policy_decision(shipment_id)
        print(json.dumps(report, indent=4))

    print("\n=== EXERCISE 007: AI RELIABILITY TEST ===")

    test_cases = [
        {
            "shipment_id": "SHP-001",
            "expected_action": "No action required",
        },
        {
            "shipment_id": "SHP-004",
            "expected_action": "Escalate to logistics manager",
        },
        {
            "shipment_id": "SHP-999",
            "expected_action": "Verify shipment ID",
        },
    ]

    for test in test_cases:
        shipment_id = test["shipment_id"]

        print(f"\n=== AI TESTING {shipment_id} ===")

        agent = create_policy_decision_agent()

        try:
            response = agent.run(
                f"Use evaluate_logistics_decision to analyze {shipment_id}. "
                "After the tool returns, provide a final answer with "
                "shipment_id, delay_days, recommended_action, "
                "policy_id, and decision_supported when available. "
                "If the shipment is not found, state that clearly "
                "and recommend verifying the shipment ID. "
                "Do not invent missing information. "
                "Do not call the tool again after receiving its result."
            )

            print("\n=== FINAL AI RESPONSE ===")
            print(response)

        except Exception as error:
            print(f"\nAI TEST ERROR: {error}")

print("\n=== EXERCISE 007: RELIABLE OUTPUT TEST ===")

for shipment_id in ["SHP-001", "SHP-004", "SHP-999"]:
    print(f"\n--- {shipment_id} ---")
    print(run_reliable_policy_decision(shipment_id))
