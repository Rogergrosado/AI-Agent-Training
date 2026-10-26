# Exercise 002 — Logistics Dummy Agent

**Course:** Hugging Face AI Agents Course — Unit 1  
**Topic:** Dummy Agent Library and Thought–Action–Observation Cycle  
**Status:** Completed  
**Tools:** Python 3.12, Ollama, Qwen2 1.5B, Requests, Windows PowerShell

---

## 1. Objective

The objective of this exercise was to understand how an AI agent can combine language-model reasoning with external tools to complete a task.

Inspired by the Hugging Face Dummy Agent Library notebook, I developed a simplified logistics agent capable of identifying shipment IDs, retrieving shipment information, and explaining the results.

The exercise focuses on understanding the Thought–Action–Observation cycle rather than implementing a fully autonomous agent.

## 2. Project Overview

The Logistics Dummy Agent is a Python application that simulates shipment tracking using predefined records.

It integrates a locally hosted language model through Ollama and uses a Python function to retrieve shipment statuses.

The system follows four main stages:

1. **Thought:** The language model identifies the shipment ID from the user's question.
2. **Action:** Python executes the `get_shipment_status()` function.
3. **Observation:** The function retrieves the shipment's status from predefined data.
4. **Final Answer:** The language model generates an explanation using the retrieved information, or Python returns a predefined fallback message.

## 3. Technologies Used

- **Python 3.12:** Application logic and tool execution.
- **Ollama:** Local language-model runtime.
- **Qwen2 1.5B:** Shipment ID extraction and natural-language explanations.
- **Requests:** Communication with the local Ollama API.
- **Windows PowerShell:** Development and testing environment.
- **Git and GitHub:** Version control and portfolio documentation.

## 4. Implementation

The application was created in:

`exercises/logistics_dummy_agent.py`

The program uses a predefined shipment dataset and a Python lookup function.

The language model first processes the user's request to identify a shipment ID.

The program then calls `get_shipment_status()` to retrieve the corresponding shipment status.

Finally, the result is provided to the language model for a short explanation.

For missing shipment records, a deterministic fallback prevents the language model from generating unsupported explanations.

## 5. Testing and Results

Four shipment scenarios were tested.

| Shipment ID | Verified Status | Test Result |
|---|---|---|
| SHP-002 | Delivered | Passed |
| SHP-001 | In Transit | Passed |
| SHP-004 | Delayed | Passed |
| SHP-999 | Shipment not found | Passed |

All four scenarios produced the expected status in the final test.

### Missing Shipment Example

**User question:** Where is shipment SHP-999?

**Tool observation:** Shipment not found

**Final response:**

"No tracking record was found for SHP-999. Please verify the shipment ID."

This response avoids making unsupported claims about the shipment's actual existence or location.

## 6. Reliability Improvement

During initial testing, the language model sometimes added interpretations that were not directly supported by the tracking tool.

To improve reliability, I introduced a conditional statement that handles missing shipment records without requesting a language-model-generated explanation.

This change separates verified information from generated text and demonstrates the importance of controlling AI outputs in operational applications.

## 7. Limitations

The current prototype has several limitations:

- Shipment records are predefined rather than retrieved from a live logistics system.
- The language model does not autonomously select between multiple tools.
- The Thought–Action–Observation workflow is controlled by Python.
- Shipment ID extraction relies on a small local language model.
- The application does not yet support real-time tracking, databases, or carrier APIs.
- Testing covers four examples and does not establish reliability across all possible user inputs.

## 8. Lessons Learned

This exercise helped me understand how a language model can work with Python functions to perform a practical task.

I learned that a language model's response should not automatically be treated as verified information.

I also gained experience debugging Python indentation errors, testing multiple shipment scenarios, and introducing deterministic safeguards.

Most importantly, I learned how to separate tool-generated facts from AI-generated explanations.

## 9. Logistics Applications

The concepts explored in this exercise could eventually support:

- Shipment tracking assistants.
- Transportation monitoring.
- Delivery exception handling.
- Warehouse information retrieval.
- Logistics customer support.

A production implementation would require authenticated data sources, additional validation, error handling, and more extensive testing.

## 10. Next Steps

Future exercises will explore agent frameworks, dynamic tool selection, improved input validation, and more advanced workflows.

The long-term goal is to apply AI agent technologies to logistics, supply chain management, and industrial engineering.

---

**Reference:** Hugging Face AI Agents Course — Unit 1, Dummy Agent Library.

**Repository:** https://github.com/Rogergrosado/AI-Agent-Training