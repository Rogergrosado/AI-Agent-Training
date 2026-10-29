"""
Exercise 006 — Logistics Knowledge Retrieval Agent
Hugging Face AI Agents Course — Unit 2.1: smolagents

Stage 1: Simulated logistics knowledge base.
"""

import json
from smolagents import tool, ToolCallingAgent, LiteLLMModel

KNOWLEDGE_BASE = {
    "POL-001": {
        "title": "Delayed Shipment Procedure",
        "category": "Shipment Delays",
        "content": (
            "Shipments delayed by 1 to 2 days should be monitored. "
            "Shipments delayed by 3 to 4 days require contacting "
            "the carrier. Shipments delayed by 5 or more days "
            "must be escalated to the logistics manager."
        ),
    },
    "POL-002": {
        "title": "Damaged Goods Procedure",
        "category": "Damaged Shipments",
        "content": (
            "When damaged goods are reported, employees must "
            "document the damage, photograph the affected items, "
            "notify the carrier, and open an incident report."
        ),
    },
    "POL-003": {
        "title": "Missing Shipment Procedure",
        "category": "Missing Shipments",
        "content": (
            "If a shipment cannot be located, employees must "
            "verify the tracking number, contact the carrier, "
            "and initiate an internal investigation."
        ),
    },
    "POL-004": {
        "title": "Customer Notification Guidelines",
        "category": "Customer Service",
        "content": (
            "Customers should be informed when a significant "
            "delivery exception is confirmed. Notifications "
            "must include the shipment reference, current "
            "status, and next expected update."
        ),
    },
}


def get_policy(policy_id):
    """Retrieve a logistics policy using its ID."""
    return KNOWLEDGE_BASE.get(policy_id)


def search_policies(keyword):
    """Search logistics policies using a keyword."""

    results = []

    keyword = keyword.lower().strip()

    for policy_id, policy in KNOWLEDGE_BASE.items():

        searchable_text = (
            policy["title"] + " " + policy["category"] + " " + policy["content"]
        ).lower()

        if keyword in searchable_text:
            results.append(
                {
                    "policy_id": policy_id,
                    "title": policy["title"],
                    "category": policy["category"],
                    "content": policy["content"],
                }
            )

    return results


def rank_policies(query):
    """Rank logistics policies using individual query words."""

    stop_words = {
        "a",
        "an",
        "the",
        "and",
        "or",
        "to",
        "for",
        "of",
        "in",
        "on",
        "with",
        "what",
        "how",
        "should",
        "do",
        "does",
        "our",
        "company",
        "policy",
        "policies",
        "about",
        "when",
        "is",
        "are",
        "was",
        "were",
        "my",
        "your",
        "we",
        "i",
        "if",
        "from",
        "at",
        "by",
    }

    synonyms = {
        "broken": "damaged",
        "damage": "damaged",
        "late": "delayed",
        "delay": "delayed",
        "lost": "missing",
        "package": "shipment",
        "packages": "shipments",
    }

    words = query.lower().split()

    keywords = []

    for word in words:
        word = word.strip(".,?!:;\"'()")

        if not word or word in stop_words:
            continue

        normalized_word = synonyms.get(word, word)

        if normalized_word not in keywords:
            keywords.append(normalized_word)

    ranked_results = []

    if not keywords:
        return ranked_results

    for policy_id, policy in KNOWLEDGE_BASE.items():
        score = 0

        title = policy["title"].lower()
        category = policy["category"].lower()
        content = policy["content"].lower()

        for keyword in keywords:
            if keyword in title:
                score += 3

            if keyword in category:
                score += 2

            if keyword in content:
                score += 1

        if score > 0:
            ranked_results.append(
                {
                    "policy_id": policy_id,
                    "title": policy["title"],
                    "relevance_score": score,
                    "content": policy["content"],
                }
            )

    ranked_results.sort(key=lambda policy: policy["relevance_score"], reverse=True)

    return ranked_results


@tool
def search_logistics_knowledge(query: str) -> str:
    """
    Search the company logistics knowledge base.

    Args:
        query: A keyword or phrase describing the logistics
            policy or procedure to retrieve.
    """

    results = rank_policies(query)

    if not results:
        return json.dumps(
            {
                "query": query,
                "status": "no_results",
                "message": "No relevant logistics policies found.",
            }
        )

    return json.dumps(
        {"query": query, "status": "success", "results": results}, indent=2
    )


def create_knowledge_agent():
    """Create a local AI agent for logistics policy retrieval."""

    model = LiteLLMModel(
        model_id="ollama/qwen2:1.5b",
        api_base="http://localhost:11434",
        api_key="ollama",
    )

    agent = ToolCallingAgent(
        tools=[search_logistics_knowledge],
        model=model,
        max_steps=5,
    )

    return agent


if __name__ == "__main__":
    print("=== AI LOGISTICS KNOWLEDGE TESTS ===")

    agent = create_knowledge_agent()

    test_questions = {
        "DAMAGED GOODS": (
            "A customer received a package with broken products. "
            "What does company policy require employees to do?"
        ),
        "DELAYED SHIPMENT": (
            "A shipment is 5 days late. "
            "According to company policy, what should happen?"
        ),
        "UNKNOWN POLICY": ("What is our company's insurance reimbursement policy?"),
    }

    for test_name, question in test_questions.items():
        print(f"\n=== TESTING: {test_name} ===")

        task = (
            f"{question}\n\n"
            "You must call the search_logistics_knowledge tool "
            "before answering. "
            "Search using relevant logistics terms or a short "
            "description of the issue. "
            "Read the retrieved policy content carefully. "
            "Include the policy ID in your final answer. "
            "Only state procedures explicitly supported by "
            "the retrieved policies. "
            "If the retrieved policies do not answer the "
            "question, say that the information is unavailable. "
            "Never invent company procedures."
        )

        try:
            response = agent.run(task, reset=True)

            print(f"\n=== FINAL RESPONSE: {test_name} ===")
            print(response)

        except Exception as error:
            print(f"\nTest failed: {error}")
