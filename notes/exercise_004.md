# Exercise 004 — Smolagents Logistics Agent

**Course:** Hugging Face AI Agents Course — Unit 1  
**Date:** October 26, 2026  
**Status:** Completed

## Objective

Build a logistics-focused AI agent using the Smolagents framework, allowing a local language model to select and execute Python tools to answer shipment-related questions.

## Technologies Used

- Python 3.12
- Ollama
- Qwen2 1.5B
- Hugging Face Smolagents
- LiteLLM
- Model Context Protocol (MCP) dependency
- Visual Studio Code
- Windows PowerShell

## Implementation

Developed `smolagents_logistics_agent.py`, which connects a local Qwen2 model to a Smolagents agent.

Two Python tools were implemented:

1. `get_shipment_status`: Retrieves a shipment's verified status from a simulated tracking database.
2. `list_delayed_shipments`: Identifies shipments currently marked as delayed.

The agent uses `ToolCallingAgent` to select the appropriate tool based on the user's request.

## Testing and Results

| Test | Expected Result | Actual Result |
|---|---|---|
| Status of SHP-999 | Shipment not found | Passed |
| Which shipments are delayed? | SHP-004 | Passed |

Both tests demonstrated successful tool selection, execution, and final-answer generation.

## Challenges and Solutions

The initial implementation used `CodeAgent`, but the local language model generated unsupported Python function calls and imports.

The implementation was changed to `ToolCallingAgent` to use structured tool calls.

A missing `mcp` dependency also caused an execution error. Installing the dependency resolved that issue.

## Lessons Learned

- AI agents can select tools based on natural-language questions.
- Tool execution must be distinguished from language-model-generated responses.
- Structured tool calling can improve compatibility with smaller local models.
- Dependency management and debugging are essential when integrating agent frameworks.
- Verified tracking data helps prevent unsupported logistics claims.

## Conclusion

Exercise 004 successfully demonstrated a local AI agent using two registered logistics tools. This completed the planned four-exercise progression for the Unit 1 training project.

**Note:** The agent uses simulated shipment data for educational purposes. It is not connected to a live carrier tracking system.