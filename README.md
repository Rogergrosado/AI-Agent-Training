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
│   └── logistics_dummy_agent.py
├── notes/
│   ├── exercise_001.md
│   └── exercise_002.md
├── projects/
├── README.md
└── .gitignore
```

## Training Progress

|## Training Progress

| Exercise | Description | Status |
|---|---|---|
| 001 | Running My First Local LLM | Completed |
| 002 | Logistics Dummy Agent - Thought-Action-Observation Cycle | Completed |

## Exercise 001 — Running My First Local LLM

**Date:** October 25, 2026

For my first exercise, I configured a local language model using Ollama and Python.

I successfully executed Qwen2:1.5b and developed a Python script that communicated with the local model.

The application explored how AI technologies could support logistics operations, including route optimization, inventory management, and supply chain visibility.

**Source code:** [first_local_llm.py](exercises/first_local_llm.py)

**Technical documentation:** [Exercise 001](notes/exercise_001.md)

## Exercise 002 - Logistics Dummy Agent

**Date:** October 26, 2026

In this exercise, I developed a basic logistics AI agent inspired by the Hugging Face AI Agents Course.

The application demonstrates the Thought-Action-Observation cycle by combining a locally running language model with a Python shipment tracking tool.

Using Ollama and Qwen2 1.5B, the agent identifies shipment IDs from user questions, retrieves shipment information, and generates natural-language explanations.

The exercise includes four shipment scenarios:

- SHP-001: In Transit
- SHP-002: Delivered
- SHP-004: Delayed
- SHP-999: Shipment not found

A reliability improvement was implemented to handle missing shipment records with a deterministic response instead of relying on the language model.

**Key Concepts:**
- AI agent architecture
- Thought-Action-Observation cycle
- Tool integration
- Local LLM inference
- Response reliability
- Logistics automation

**Source code:** [logistics_dummy_agent.py](exercises/logistics_dummy_agent.py)

**Technical documentation:** [Exercise 002](notes/exercise_002.md)

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