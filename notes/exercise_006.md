# Exercise 006 — Logistics Knowledge Retrieval Agent

**Course:** Hugging Face AI Agents Course — Unit 2.1: smolagents  
**Date:** October 28, 2026  
**Status:** Completed Prototype  
**Language:** Python 3.12.4

## 1. Objective

The objective of Exercise 006 was to build a logistics knowledge retrieval agent capable of searching a simulated company's internal policies and answering operational questions using verified information.

This exercise builds upon Exercise 005, where I developed an AI-powered logistics exception management system.

Instead of analyzing individual shipment records, I wanted to explore how an AI agent could retrieve organizational knowledge, identify relevant procedures, and use those procedures to answer questions.

My main goal was to create an agent that could provide useful operational guidance without inventing company policies.

## 2. Project Overview

I developed a Python-based logistics knowledge retrieval system using the smolagents framework and a locally hosted language model.

The system combines a simulated logistics knowledge base, keyword-based retrieval, relevance scoring, and AI-powered tool calling.

The knowledge base contains four company policies covering shipment delays, damaged goods, missing shipments, and customer notifications.

The agent can search these policies, retrieve relevant procedural information, and formulate a natural-language response.

Unlike a general-purpose chatbot, the agent is instructed to rely on retrieved company policies when answering operational questions.

## 3. Technologies Used

- Python 3.12.4
- Hugging Face smolagents
- Ollama
- Qwen2 1.5B
- LiteLLMModel
- ToolCallingAgent
- Python dictionaries and lists
- JSON
- PowerShell
- Visual Studio Code
- Git and GitHub

The project runs locally using Ollama rather than requiring a cloud-hosted language model.

## 4. Knowledge Base Design

I created a simulated internal knowledge base containing four logistics policies.

Each policy includes a unique identifier, title, category, and procedural content.

| Policy ID | Policy Title | Operational Purpose |
|---|---|---|
| POL-001 | Delayed Shipment Procedure | Defines responses to shipment delays |
| POL-002 | Damaged Goods Procedure | Explains how to handle damaged shipments |
| POL-003 | Missing Shipment Procedure | Provides guidance for shipments that cannot be located |
| POL-004 | Customer Notification Guidelines | Describes customer communication requirements |

The knowledge base serves as the agent's source of organizational information.

It is a simulated dataset for educational purposes, not an actual company's policy repository.

## 5. Knowledge Retrieval and Relevance Ranking

I began by implementing a basic policy lookup function.

This allowed me to retrieve individual policies by their identifiers and verify that the underlying knowledge base was accessible.

Next, I implemented a search function that could identify policies associated with a user's keyword.

Initial tests included searches for delayed shipments, damaged goods, carriers, and insurance.

I then extended the search functionality with relevance ranking to better handle natural-language questions.

The ranking process assigns scores to policies based on matching terms, allowing the system to prioritize potentially relevant results.

For example, searching for damaged goods successfully retrieved POL-002, while a shipment-related query returned multiple policies with different relevance scores.

This helped me understand how a basic retrieval system can evolve beyond direct policy ID lookups.

However, the ranking system remains relatively simple and can return policies that are only loosely related to the user's question.

## 6. Integration with smolagents

After testing the knowledge base and search functions independently, I integrated them into an AI agent using the smolagents framework.

The agent uses ToolCallingAgent to request information from a registered knowledge retrieval tool.

The local Qwen2 1.5B model interprets the user's question and decides when to call the search tool.

The Python tool performs the retrieval and returns structured results.

The language model then uses the retrieved information to formulate an answer.

This separates two important responsibilities:

**Python retrieval logic:** Locates and ranks company policies.

**AI reasoning and response generation:** Interprets the question and communicates relevant procedures.

This separation is useful because the language model does not need to memorize the entire knowledge base.

## 7. Agent Workflow

The system follows this process:

1. A user asks a question about a logistics procedure.
2. The agent identifies a relevant search query.
3. The agent calls `search_logistics_knowledge`.
4. Python searches the simulated knowledge base.
5. The retrieval function returns relevant policy information or a no-results message.
6. The agent interprets the returned information.
7. The agent generates a response based on the available policy evidence.

This workflow demonstrates the relationship between tool calling and knowledge retrieval.

The agent is responsible for deciding how to use the tool, while Python provides access to the underlying policy data.

## 8. Testing and Results

I tested the system in several stages to validate the individual functions before running the complete AI agent.

### Test 1 — Direct Policy Retrieval

I tested individual policy IDs to confirm that the knowledge base returned the correct records.

Valid policy IDs returned their corresponding information.

An unknown policy ID returned no matching record.

### Test 2 — Keyword Search

I tested search terms including:

- Delayed
- Damaged
- Carrier
- Insurance

The system successfully retrieved policies associated with the first three terms.

The insurance search returned no matching policies.

### Test 3 — Relevance Ranking

I tested the ranking system using operational keywords.

The damaged-goods search ranked POL-002 as the most relevant policy.

The shipment search returned multiple policies with different scores.

The insurance search returned no relevant policies.

These tests demonstrated that the ranking system could distinguish between matching and nonmatching information, although its precision was not perfect.

### Test 4 — AI Agent: Damaged Goods

**Question:** What should employees do when goods arrive damaged?

**Retrieved policy:** POL-002 — Damaged Goods Procedure.

**Result:** The agent explained that employees should document the damage, photograph affected items, notify the carrier, and open an incident report.

**Assessment:** Successful retrieval and a policy-grounded response.

One observed limitation was that a broader search also retrieved a missing-shipment policy, even though it was not necessary to answer the question.

### Test 5 — AI Agent: Delayed Shipment

**Scenario:** A shipment is delayed by five days.

**Retrieved policy:** POL-001 — Delayed Shipment Procedure.

**Result:** The agent correctly stated that shipments delayed by five or more days must be escalated to the logistics manager.

**Assessment:** Successful policy retrieval and correct procedural guidance.

### Test 6 — AI Agent: Unknown Insurance Policy

**Question:** What is the company's insurance reimbursement policy?

**Expected behavior:** The agent should recognize that the simulated knowledge base does not contain the requested policy.

**Observed behavior:** The search tool repeatedly returned no relevant logistics policies. The agent eventually reached its maximum number of steps and responded:

"Sorry, but I can't assist with that."

**Assessment:** Partially successful.

The agent did not invent an insurance reimbursement procedure, which satisfied the primary safety objective.

However, the response was not sufficiently informative, and the agent performed unnecessary repeated searches.

## 9. Challenges and Lessons Learned

One of the main challenges was improving retrieval relevance.

Simple keyword matching worked for direct searches but was less reliable when users asked complete natural-language questions.

Adding relevance scoring improved the search results, although unrelated policies could still appear.

Another challenge was controlling the behavior of the local language model when no relevant policy was available.

The model sometimes repeated searches rather than immediately explaining that the requested information was unavailable.

The insurance reimbursement test demonstrated this limitation.

I also learned that retrieving information and generating an answer are separate tasks.

A successful retrieval function does not automatically guarantee a clear or efficient AI response.

Both components must be evaluated independently.

## 10. Potential Improvements

Future improvements could include:

- More precise search ranking and filtering.
- Better handling of queries with no matching policies.
- A maximum retry limit for repeated searches.
- More consistent inclusion of policy IDs in final answers.
- Automated test cases for policy retrieval.
- Improved query normalization.
- A larger and more realistic policy knowledge base.
- Semantic retrieval using embeddings.
- Integration with external documents or organizational data sources.

These improvements could help transform the prototype into a more reliable operational knowledge assistant.

## 11. Connection to Industrial Engineering and Logistics

This exercise demonstrates a potential application of AI agents in industrial engineering and supply chain operations.

Logistics teams regularly depend on standard operating procedures, internal policies, and operational guidelines.

A knowledge retrieval agent could help employees locate relevant procedures without manually searching multiple documents.

Potential applications include shipment exception handling, warehouse operations, customer service, carrier coordination, and internal process support.

For me, this project also connects AI development with process standardization and operational decision support.

## 12. Final Reflection

Exercise 006 helped me understand how AI agents can use external knowledge rather than relying exclusively on the information contained in a language model.

I developed a simulated policy knowledge base, implemented search and relevance ranking, connected the retrieval system to smolagents, and tested the resulting agent with realistic logistics questions.

The most important lesson was that an AI agent must be evaluated not only on whether it produces an answer, but also on whether that answer is supported by reliable information.

The prototype successfully retrieved relevant policies and avoided fabricating an unavailable insurance procedure.

At the same time, its repeated searches and imperfect fallback response showed me where additional engineering is needed.

This exercise represents another step toward my long-term goal of building practical AI-powered solutions for logistics, supply chain management, and industrial engineering.

## 13. Project Files

**Source code:** `exercises/logistics_knowledge_agent.py`

**Technical documentation:** `notes/exercise_006.md`

**Repository:** https://github.com/Rogergrosado/AI-Agent-Training

## 14. Learning Resources

- Hugging Face — AI Agents Course: https://huggingface.co/learn/agents-course/
- Hugging Face — smolagents Documentation: https://huggingface.co/docs/smolagents/
- Ollama: https://ollama.com/
- Python Documentation: https://docs.python.org/3/