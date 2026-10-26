# Exercise 003 – Structured Logistics Agent

**Course:** Hugging Face AI Agents Course – Unit 1  
**Project:** AI-Agent-Training  
**Status:** Completed

## Objective

Develop a structured logistics agent that converts a natural-language shipment inquiry into a JSON-formatted tool action, executes a Python function, processes the verified observation, and produces a final answer.

## Technologies Used

- Python 3.12
- Ollama
- Qwen2 1.5B
- Requests
- Visual Studio Code
- Windows PowerShell

## Agent Workflow

1. **User Question:** The user requests the status of a shipment.
2. **Action Generation:** The local language model generates a JSON action containing the tool name and shipment ID.
3. **Action Parsing:** Python interprets the JSON and extracts the requested tool and arguments.
4. **Tool Execution:** The shipment-tracking function retrieves the corresponding mock shipment status.
5. **Observation:** The verified result is returned to the agent.
6. **Final Answer:** The agent communicates the shipment status in natural language.

## Testing Results

| Shipment ID | Expected Observation | Result |
|---|---|---|
| SHP-001 | In Transit | Passed |
| SHP-002 | Delivered | Passed |
| SHP-004 | Delayed | Passed |
| SHP-999 | Shipment not found | Passed |

## Key Concepts Learned

- Structured JSON tool calls
- Parsing model-generated actions
- Separating language-model decisions from Python tool execution
- Using verified observations as the source of truth
- Generating natural-language final answers
- Handling missing shipment records without inventing information

## Reliability

The agent was tested against four shipment scenarios, including a missing shipment record. The observed outputs matched the expected mock data.

These tests demonstrate the basic workflow but do not establish reliability across arbitrary user inputs or malformed model-generated JSON.

## Conclusion

Exercise 003 builds upon the previous exercises by introducing structured actions and a more explicit agent execution process.

The project demonstrates how a local language model can interact with deterministic Python tools to answer logistics-related questions using verified information.