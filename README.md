# AI Agent Training — From Foundations to Logistics Applications

## Overview

This repository documents my hands-on journey into Artificial Intelligence, Large Language Models (LLMs), and AI agent development.

Building upon my Computer Science Foundations training at Holberton School and my current studies in Industrial Engineering, my objective is to explore how AI technologies can improve logistics, supply chain management, and operational decision-making.

This repository combines structured learning, independent programming exercises, technical documentation, and practical projects.

## Learning Objectives

- Understand the fundamentals of AI agents and LLMs.
- Develop Python applications that interact with language models.
- Experiment with local AI models using Ollama.
- Learn AI agent frameworks, including Hugging Face smolagents.
- Explore practical applications in logistics and industrial engineering.
- Build a documented technical portfolio through GitHub.

## Technologies

- Python
- Ollama
- Qwen2:1.5b
- Hugging Face
- smolagents
- Git and GitHub
- Windows PowerShell

Additional technologies will be documented as they are introduced.

## Repository Structure

```text

AI-Agent-Training/
├── exercises/
│   ├── first_local_llm.py
│   ├── logistics_dummy_agent.py
│   ├── structured_logistics_agent.py
│   ├── smolagents_logistics_agent.py
│   └── logistics_exception_agent.py
├── notes/
│   ├── exercise_001.md
│   ├── exercise_002.md
│   ├── exercise_003.md
│   ├── exercise_004.md
│   └── exercise_005.md
├── projects/
├── README.md
└── .gitignore
```

## Training Progress

| Exercise | Description | Status |
|---|---|---|
| 001 | Running My First Local LLM | Completed |
| 002 | Logistics Dummy Agent - Thought-Action-Observation Cycle | Completed |
| 003 | Structured Logistics Agent - JSON Tool Calling | Completed |
| 004 | Smolagents Logistics Agent - Framework-Based Tool Calling | Completed |
005 | Logistics Exception Management Agent | Smolagents-Based Tool Calling | Completed

## Exercise 001 — Running My First Local LLM

**Date:** October 25, 2026

For my first exercise, I configured a local language model using Ollama and Python.

I successfully executed Qwen2:1.5b and developed a Python script that communicated with the local model.

The application explored how AI technologies could support logistics operations, including route optimization, inventory management, and supply chain visibility.

**Source code:** [first_local_llm.py](exercises/first_local_llm.py)

**Technical documentation:** [Exercise 001](notes/exercise_001.md)


## Exercise 002 — Logistics Dummy Agent

**Date:** October 2026

### Objective

Develop a basic logistics AI agent that demonstrates the Thought–Action–Observation cycle using a locally running language model and a Python shipment-tracking tool.

### Technologies

- Python 3.12
- Ollama
- LiteLLM
- Smolagents
- Qwen2 1.5B
- Requests
- Windows PowerShell

### Implementation

In this exercise, I developed a Python script that simulates the behavior of an AI agent.

The agent receives a shipment-related question, uses the local language model to identify the shipment ID, retrieves the shipment's status from a simulated database, and generates an explanation based on the verified information.

The workflow follows three stages:

1. **Thought:** The language model interprets the user's question and identifies the shipment.
2. **Action:** A Python function retrieves the corresponding tracking status.
3. **Observation:** The verified result is provided to the model to generate the final response.

### Testing Results

| Shipment | Expected Result | Result |
|---|---|---|
| SHP-001 | In Transit | Passed |
| SHP-002 | Delivered | Passed |
| SHP-004 | Delayed | Passed |
| SHP-999 | Shipment not found | Passed |

### Challenges and Lessons Learned

One important challenge was preventing the language model from inventing information when a shipment did not exist.

To address this, I implemented deterministic handling for missing shipments. Instead of allowing the language model to generate an unsupported response, the program returns a predefined message asking the user to verify the shipment ID.

This exercise helped me understand the relationship between language-model reasoning, Python tools, verified observations, and reliable final responses.

**Source Code:** [logistics_dummy_agent.py](exercises/logistics_dummy_agent.py)

**Documentation:** [exercise_002.md](notes/exercise_002.md)

---

## Exercise 003 — Structured Logistics Agent

**Date:** October 26, 2026

### Objective

Develop a logistics AI agent that uses structured JSON output to request tool execution rather than relying exclusively on unstructured natural-language responses.

### Technologies

- Python 3.12
- Ollama
- Qwen2 1.5B
- Requests
- JSON
- Windows PowerShell

### Implementation

In this exercise, I expanded the previous logistics agent by introducing structured action requests.

The language model receives a shipment-related question and generates a JSON object specifying the action to perform and the required arguments.

Example:

```json
{
  "action": "get_shipment_status",
  "action_input": {
    "shipment_id": "SHP-004"
  }
}
```

The Python application parses this JSON, identifies the requested tool, executes the shipment-tracking function, and retrieves the verified observation.

The result is then used to produce a final response.

### Testing Results

| Shipment | Expected Result | Result |
|---|---|---|
| SHP-001 | In Transit | Passed |
| SHP-002 | Delivered | Passed |
| SHP-004 | Delayed | Passed |
| SHP-999 | Shipment not found | Passed |

### Challenges and Lessons Learned

This exercise demonstrated how structured outputs make interactions between language models and software tools more predictable.

I also reinforced the importance of validating shipment information before generating a final answer, particularly when a shipment ID does not exist in the simulated database.

The main improvement over Exercise 002 was the introduction of machine-readable JSON action requests, creating a clearer separation between the language model's decisions and Python's tool execution.

**Source Code:** [structured_logistics_agent.py](exercises/structured_logistics_agent.py)

**Documentation:** [exercise_003.md](notes/exercise_003.md)

---

## Exercise 004 — Smolagents Logistics Agent

**Date:** October 26, 2026

### Objective

Implement a logistics AI agent using the Hugging Face Smolagents framework, moving from manually managed tool execution to framework-based tool calling.

### Technologies

- Python 3.12
- Hugging Face Smolagents
- LiteLLM
- Ollama
- Qwen2 1.5B
- Windows PowerShell

### Implementation

In this exercise, I implemented a logistics agent using `ToolCallingAgent` and `LiteLLMModel`.

The agent connects to the locally running Qwen2 1.5B model through Ollama and uses registered Python tools to retrieve shipment information.

Two tools were implemented:

1. **get_shipment_status:** Retrieves the verified tracking status for a shipment ID.
2. **list_delayed_shipments:** Returns the shipment IDs currently marked as delayed.

Unlike the previous exercises, the framework manages the interaction between the language model and its registered tools.

### Testing Results

| Test | Expected Result | Result |
|---|---|---|
| SHP-004 | Delayed | Passed |
| SHP-999 | Shipment not found | Passed |
| List delayed shipments | SHP-004 | Passed |

### Challenges and Lessons Learned

During development, I encountered several technical challenges, including dependency installation, restricted code execution, unauthorized imports, and model compatibility.

Initially, I experimented with `CodeAgent`, but the smaller local model generated Python code that was incompatible with the framework's execution restrictions.

I resolved this by switching to `ToolCallingAgent`, allowing the model to invoke explicitly registered Python tools instead of generating unrestricted Python code.

I also installed additional dependencies required for successful tool execution.

This exercise helped me understand the differences between manually implemented agents and framework-based agents, while reinforcing the importance of controlled tool execution and verified logistics information.

**Source Code:** [smolagents_logistics_agent.py](exercises/smolagents_logistics_agent.py)

**Documentation:** [exercise_004.md](notes/exercise_004.md)


## Exercise 005 — Logistics Exception Management Agent

**Course:** Hugging Face AI Agents Course — Unit 2.1: smolagents

**Date:** October 28, 2026

### Objective

Extend the shipment-tracking capabilities developed in Exercise 004 into a logistics exception management agent capable of identifying delivery delays, classifying operational priorities, and recommending appropriate actions.

### What I Built

I developed a Python-based logistics exception management system that combines deterministic business rules with AI-powered tool calling.

The system can:

- Retrieve shipment information from a simulated database.
- Calculate delivery delays using a fixed reference date.
- Classify exceptions as NONE, LOW, MEDIUM, or HIGH.
- Recommend operational actions based on predefined rules.
- Generate structured JSON exception reports.
- Execute a custom tool through the smolagents framework.
- Interpret natural-language requests using a locally hosted AI model.
- Handle unknown shipment IDs without inventing tracking information.

### Technologies Used

- Python 3.12.4
- smolagents 1.26.0
- Ollama
- Qwen2 1.5B
- LiteLLMModel
- ToolCallingAgent
- JSON

### Testing Results

| Shipment | Delay | Priority | Recommended Action |
|----------|-------|----------|--------------------|
| SHP-001 | 0 days | NONE | No action required |
| SHP-002 | 0 days | NONE | No action required |
| SHP-003 | 2 days | LOW | Monitor shipment |
| SHP-004 | 5 days | HIGH | Escalate to logistics manager |
| SHP-005 | 4 days | MEDIUM | Contact carrier |
| SHP-999 | Not found | UNKNOWN | Verify shipment ID |

The Python business logic was tested across the priority categories.

The AI agent also successfully executed shipment analysis requests using the custom smolagents tool.

### What I Learned

This exercise helped me understand the importance of separating deterministic business logic from AI decision-making.

Instead of allowing the language model to calculate delays or invent operational recommendations, I created Python functions responsible for these tasks.

The AI agent focuses on interpreting requests, selecting the appropriate tool, and communicating the results.

This approach makes the system easier to test, maintain, and expand.

### Project Files

**Source Code:** [logistics_exception_agent.py](exercises/logistics_exception_agent.py)

**Technical Documentation:** [exercise_005.md](notes/exercise_005.md)

### Next Step

Exercise 006 — Logistics Knowledge Retrieval Agent


## Long-Term Vision

My goal is to progressively develop AI-powered solutions for real-world operational challenges.

Future areas of exploration include:

- Supply chain analytics
- Logistics automation
- Inventory forecasting
- Transportation and route optimization
- AI-assisted operational decision-making

## Learning Resources

- [Hugging Face AI Agents Course](https://huggingface.co/learn/agents-course)
- [Ollama](https://ollama.com/)
- [Python Documentation](https://docs.python.org/3/)

## Project Status

Active development — October 2026.

This repository will continue evolving as I complete additional exercises and develop more advanced AI applications.
