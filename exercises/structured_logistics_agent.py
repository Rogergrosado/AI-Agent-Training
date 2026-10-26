import json
import re
import requests

# Exercise 003: Structured Logistics AI Agent
# Step 4: LLM-generated JSON actions

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2:1.5b"


def get_shipment_status(shipment_id):
    shipments = {
        "SHP-001": "In Transit",
        "SHP-002": "Delivered",
        "SHP-003": "Processing",
        "SHP-004": "Delayed",
    }

    return shipments.get(shipment_id, "Shipment not found")


def ask_llm(question):
    system_prompt = """
You are a logistics AI agent.

Your job is to select a tool to answer shipment questions.

Available tool:
get_shipment_status(shipment_id)

Respond ONLY with a valid JSON object in this format:
{
    "action": "get_shipment_status",
    "action_input": {
        "shipment_id": "SHP-001"
    }
}

Do not invent shipment statuses.
Do not include explanations or Markdown.
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": system_prompt + "\nUser: " + question,
            "stream": False,
            "format": "json",
        },
        timeout=120,
    )

    response.raise_for_status()
    return response.json()["response"]


def parse_action(llm_output):
    action = json.loads(llm_output)

    if not isinstance(action, dict):
        raise ValueError("Expected a JSON object")

    if action.get("action") != "get_shipment_status":
        raise ValueError("Unknown or unsupported tool")

    arguments = action.get("action_input")

    if not isinstance(arguments, dict):
        raise ValueError("Invalid tool arguments")

    shipment_id = arguments.get("shipment_id")

    if not isinstance(shipment_id, str):
        raise ValueError("Shipment ID must be a string")

    if not re.fullmatch(r"SHP-\d{3}", shipment_id):
        raise ValueError("Invalid shipment ID format")

    return action


def generate_final_answer(question, shipment_id, observation):
    # Missing records are handled deterministically.
    if observation == "Shipment not found":
        return (
            f"No tracking record was found for {shipment_id}. "
            "Please verify the shipment ID."
        )

    prompt = f"""
You are a logistics assistant.

Answer the user's question using ONLY the verified tool result.

User question: {question}
Shipment ID: {shipment_id}
Verified observation: {observation}

Rules:
- Do not invent shipment information.
- Do not change the verified shipment status.
- Answer in one short sentence.
"""

    response = requests.post(
        OLLAMA_URL,
        json={"model": MODEL, "prompt": prompt, "stream": False},
        timeout=120,
    )

    response.raise_for_status()
    return response.json()["response"].strip()


def main():
    question = "What is the status of shipment SHP-004?"

    print("USER QUESTION:")
    print(question)

    try:
        llm_output = ask_llm(question)

        print("\nLLM-GENERATED ACTION:")
        print(llm_output)

        action = parse_action(llm_output)

        print("\nPARSED ACTION:")
        print(json.dumps(action, indent=4))

        shipment_id = action["action_input"]["shipment_id"]
        observation = get_shipment_status(shipment_id)

        print("\nVERIFIED OBSERVATION:")
        print(observation)

        final_answer = generate_final_answer(question, shipment_id, observation)

        print("\nFINAL ANSWER:")
        print(final_answer)

    except (requests.RequestException, ValueError, KeyError) as error:
        print("\nAGENT ERROR:")
        print(error)


if __name__ == "__main__":
    main()
