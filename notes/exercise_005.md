
# Exercise 005 — Logistics Exception Management Agent

## Course
Hugging Face AI Agents Course — Unit 2.1: smolagents

## Objective
Extend the shipment-tracking agent from Exercise 004
into a logistics exception management system capable of
calculating delivery delays, classifying priorities, and
recommending operational actions.

## Technologies
- Python 3.12.4
- smolagents 1.26.0
- Ollama
- Qwen2 1.5B
- LiteLLMModel
- ToolCallingAgent
- JSON

## Architecture

User Request
    |
    v
ToolCallingAgent
    |
    v
analyze_shipment_exception()
    |
    v
generate_exception_report()
    |
    +-- get_shipment()
    +-- calculate_delay()
    +-- classify_priority()
    +-- recommend_action()
    |
    v
Structured JSON Report
    |
    v
AI-Generated Response

## Development Process

### 1. Shipment Database
Created a simulated logistics database containing shipment
statuses, expected delivery dates, and actual delivery dates.

### 2. Delay Calculation
Implemented calculate_delay() using Python's datetime module.

A fixed simulation date of October 28, 2026, ensures
reproducible results.

### 3. Priority Classification
Defined fictional operational rules:

- NONE: 0 days overdue
- LOW: 1–2 days overdue
- MEDIUM: 3–4 days overdue
- HIGH: 5 or more days overdue
- UNKNOWN: Shipment not found

### 4. Operational Recommendations
Mapped priorities to recommended actions:

- NONE: No action required
- LOW: Monitor shipment
- MEDIUM: Contact carrier
- HIGH: Escalate to logistics manager
- UNKNOWN: Verify shipment ID

### 5. Structured Exception Reports
Combined shipment data, delay calculations, priority
classifications, and recommendations into JSON reports.

### 6. smolagents Integration
Created a custom tool using the @tool decorator.

Connected the tool to ToolCallingAgent using LiteLLMModel
and a locally hosted Qwen2 1.5B model through Ollama.

## Testing

| Shipment | Delay | Priority | Expected Action |
|----------|-------|----------|-----------------|
| SHP-001 | 0 | NONE | No action required |
| SHP-002 | 0 | NONE | No action required |
| SHP-003 | 2 | LOW | Monitor shipment |
| SHP-004 | 5 | HIGH | Escalate to logistics manager |
| SHP-005 | 4 | MEDIUM | Contact carrier |
| SHP-999 | N/A | UNKNOWN | Verify shipment ID |

The deterministic functions were tested across the
available priority categories.

The AI agent successfully processed LOW, HIGH, and
UNKNOWN scenarios in the initial test batch.

The additional MEDIUM scenario was also successfully
processed using the local model.

## Observations

- The AI agent successfully selected the custom shipment
  analysis tool using natural-language instructions.
- The logistics calculations were handled by deterministic
  Python functions rather than the language model.
- The model initially omitted the HIGH priority label
  in one final response.
- More explicit instructions improved the completeness
  of subsequent responses.
- The small local model was capable of completing the
  demonstrated tool-calling workflows.

## Limitations

- Shipment records are simulated.
- The reference date is fixed for reproducibility.
- Priority thresholds are fictional business rules.
- Recommendations do not trigger real-world actions.
- The model may occasionally omit fields or generate
  inconsistent responses.
- Further automated testing would be necessary before
  production use.

## Key Lessons

This exercise demonstrated the separation between
deterministic business logic and AI-powered tool selection.

It also introduced exception classification, modular
function reuse, JSON reporting, and reliability testing.

## Source Code

[Logistics Exception Management Agent](../exercises/logistics_exception_agent.py)

## Next Exercise

Exercise 006 — Logistics Knowledge Retrieval Agent
