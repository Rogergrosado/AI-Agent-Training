from smolagents import ToolCallingAgent, LiteLLMModel, tool

# Mock shipment database for training
SHIPMENTS = {
    "SHP-001": "In Transit",
    "SHP-002": "Delivered",
    "SHP-003": "Processing",
    "SHP-004": "Delayed",
}


@tool
def get_shipment_status(shipment_id: str) -> str:
    """
    Retrieve the verified status of a shipment.

    Args:
        shipment_id: The shipment tracking ID, such as SHP-004.
    """
    return SHIPMENTS.get(shipment_id.upper(), "Shipment not found")


@tool
def list_delayed_shipments() -> str:
    """
    Return the tracking IDs of all delayed shipments.
    """
    delayed = [
        shipment_id for shipment_id, status in SHIPMENTS.items() if status == "Delayed"
    ]

    if not delayed:
        return "No delayed shipments."

    return ", ".join(delayed)


if __name__ == "__main__":
    model = LiteLLMModel(
        model_id="ollama/qwen2:1.5b",
        api_base="http://localhost:11434",
        num_ctx=4096,
    )

    agent = ToolCallingAgent(
        tools=[
            get_shipment_status,
            list_delayed_shipments,
        ],
        model=model,
        max_steps=3,
        verbosity_level=1,
    )

    question = "Which shipments are currently delayed?"

    print("\nUSER QUESTION:")
    print(question)

    result = agent.run(question)

    print("\nFINAL ANSWER:")
    print(result)
