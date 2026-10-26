# Exercise 002 - Logistics Dummy Agent
# Hugging Face Agents Course - Unit 1

import json
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2:1.5b"

# Simulated shipment database
shipments = {
    "SHP-001": "In Transit",
    "SHP-002": "Delivered",
    "SHP-003": "Pending",
    "SHP-004": "Delayed"
}


# Tool: Retrieve shipment status
def get_shipment_status(shipment_id):
    return shipments.get(shipment_id, "Shipment not found")


# Communicate with our local LLM
def ask_llm(prompt):
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        },
        timeout=120
    )

    response.raise_for_status()
    return response.json()["response"].strip()


# Agent workflow
def logistics_agent(question):
    print("\nUSER QUESTION:", question)

    # THOUGHT: Identify which shipment to investigate
    prompt = f"""
You are a logistics assistant.

Identify the shipment ID in the following question.

Valid shipment IDs:
SHP-001, SHP-002, SHP-003, SHP-004

Return ONLY the shipment ID.
Do not include explanations.

Question: {question}
"""

    shipment_id = ask_llm(prompt).strip().upper()

    print("THOUGHT - Identified shipment:", shipment_id)

    # ACTION: Execute our Python tool
    status = get_shipment_status(shipment_id)

    print("ACTION - get_shipment_status()")
    print("OBSERVATION -", status)

    # FINAL ANSWER: Generate a response using the observation
    final_prompt = f"""
You are a logistics assistant.

A shipment tracking tool returned this information:

Shipment ID: {shipment_id}
Shipment status: {status}

Explain the result in one short sentence.
Use only the provided information.
Do not invent delivery dates or locations.
"""

    if status == "Shipment not found":
        final_answer = (
            f"No tracking record was found for {shipment_id}. "
            "Please verify the shipment ID."
         )
    else:
        final_answer = ask_llm(final_prompt)

    print("VERIFIED STATUS:", status)
    print("AI EXPLANATION:", final_answer)


# Run our first agent
if __name__ == "__main__":
    logistics_agent("What is the status of shipment SHP-002?")
    logistics_agent("What is the status of shipment SHP-001?")
    logistics_agent("Can you check shipment SHP-004?")
    logistics_agent("Where is shipment SHP-999?")