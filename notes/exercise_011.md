# Exercise 011 — Reliable Logistics Workflows with LangGraph

**AI Agent Training | Unit 2.2 — Agentic Frameworks**

## 1. Objective

Build a reliable, state-driven logistics workflow using LangGraph, integrating shipment retrieval, data validation, semantic policy retrieval, and operational decision support.

The primary objective is to control execution through explicit workflow states and conditional routing rather than relying entirely on an LLM to determine the next action.

## 2. Technologies

- Python 3.12
- LangGraph
- LlamaIndex
- Hugging Face embeddings
- Local shipment data stored in JSON
- Logistics policy documents
- PowerShell and Visual Studio Code

## 3. Workflow Architecture

The workflow uses a shared `ShipmentState` to maintain shipment information, processing status, errors, retrieved policies, and operational decisions.

**Execution sequence:**

1. **Initialize Shipment:** Prepare the workflow state.
2. **Lookup Shipment:** Retrieve shipment information from the existing local dataset.
3. **Validate Shipment:** Check mandatory shipment fields.
4. **Retrieve Policies:** Perform semantic retrieval of relevant logistics procedures.
5. **Evaluate Shipment:** Generate a structured recommendation based on the shipment and retrieved policies.

Conditional routing prevents invalid or nonexistent shipments from reaching downstream processing stages.

## 4. Semantic Policy Retrieval

The workflow reuses the semantic search capabilities developed in Exercise 009.

Relevant logistics policy documents are retrieved through vector similarity search. Each retrieved result includes:

- Source filename
- Similarity score, when available
- Relevant document excerpt

This provides traceable supporting information for operational assessment.

## 5. Decision Support

For a successfully validated shipment, the workflow generates a structured decision containing:

- Shipment identifier
- Exception type
- Priority
- Recommended action
- Supporting policy filenames
- Human review requirement

The recommendation is deliberately conservative and requires human review. Retrieved policies support the recommendation but do not independently authorize operational actions.

## 6. Testing and Validation

Three automated assertions were executed successfully.

| Test | Expected Outcome | Result |
|---|---|---|
| Existing shipment `SHP-1045` | `evaluated`, with policies and a decision | PASS |
| Nonexistent shipment `SHP-9999` | `not_found`, without policies or decision | PASS |
| Incomplete shipment data | `validation_failed`, with five missing-field errors | PASS |

An additional manual workflow test confirmed that incomplete shipment data stops execution before policy retrieval and evaluation.

**Automated test output:**

```text
PASS: Valid shipment workflow
PASS: Missing shipment workflow
PASS: Incomplete shipment validation

All automated workflow tests passed.
```

## 7. Engineering Lessons

**Deterministic orchestration:** LangGraph makes execution paths explicit and testable.

**Data validation:** Incomplete records must be rejected before downstream analysis.

**Semantic retrieval:** Logistics policies can be retrieved by meaning rather than exact keyword matching.

**Operational safety:** Recommendations should remain subject to human review.

**Modular architecture:** Existing retrieval and shipment lookup functions can be reused within more advanced workflows.

## 8. Limitations and Future Improvements

The current implementation is a local educational prototype, not a production logistics platform.

Future improvements may include:

- Automated tests for every conditional route
- More detailed decision rules based on policy content
- Policy relevance thresholds
- Persistent workflow checkpoints
- Structured logging and exception monitoring
- Integration with external logistics systems

## 9. Conclusion

Exercise 011 demonstrates how LangGraph can coordinate multiple logistics functions through a controlled, state-based workflow.

By combining deterministic routing, validation, semantic retrieval, and human-reviewed decision support, the project establishes a foundation for more reliable logistics AI systems.