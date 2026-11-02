# Exercise 010 — Logistics Tool-Using RAG Agent

**Project:** AI Agent Training  
**Exercise:** 010  
**Topic:** Retrieval-Augmented Generation (RAG), Tool Calling, and Reliable Logistics Reporting  
**Language:** Python  
**Status:** Experimental implementation completed; autonomous tool-calling limitations documented

---

## 1. Objective

The objective of Exercise 010 was to develop a logistics investigation system capable of combining structured shipment records with semantically retrieved operational policies.

Unlike a traditional question-answering application, this system was designed to investigate a specific shipment, retrieve relevant policy documents, validate the available information, and generate a structured operational report.

The exercise also evaluated whether a locally hosted language model could reliably coordinate multiple tools and produce evidence-based responses.

The main learning objectives were:

- Retrieve shipment records from a structured JSON database.
- Perform semantic searches across logistics policy documents.
- Connect shipment information with relevant operational procedures.
- Validate shipment data before generating reports.
- Distinguish applicable policies from policies lacking supporting evidence.
- Integrate retrieval and reporting capabilities into an AI agent.
- Evaluate the reliability and limitations of local LLM tool calling.

A major emphasis was placed on preventing unsupported conclusions, particularly when determining whether a shipment should be classified as delayed.

## 2. Technologies and Tools

| Technology | Purpose |
|---|---|
| Python | Application logic, data validation, and reporting |
| JSON | Structured shipment data storage |
| pathlib | Reliable project file path management |
| LlamaIndex | Semantic indexing and document retrieval |
| Embedding model | Conversion of policy documents and queries into semantic representations |
| smolagents | Tool registration and agent orchestration |
| LiteLLM | Interface between the agent framework and the language model |
| Ollama | Local language model execution |
| Qwen 2.5 3B | Experimental local tool-calling model |
| VS Code | Development and debugging |
| PowerShell | Execution and verification |

The system was developed locally as part of the AI Agent Training repository.

## 3. Project Architecture

Exercise 010 combines three major components:

1. Shipment data retrieval.
2. Semantic logistics policy retrieval.
3. AI-assisted investigation and validated reporting.

The implementation separates the retrieval process from the language model's reasoning.

This separation allows the underlying Python functions to operate independently, even when the language model fails to coordinate tool calls correctly.

### Main project files

**`data/exercise_010/shipments.json`**

Stores the shipment records used for testing.

**`exercises/logistics_tool_using_rag_agent.py`**

Implements shipment lookup, semantic policy retrieval, policy prioritization, and integrated shipment investigation.

**`exercises/logistics_rag_llm_agent.py`**

Implements shipment validation, agent tools, local model configuration, and evidence-based reporting functions.

**`exercises/logistics_semantic_search_agent.py`**

Provides the semantic document loading and indexing capabilities reused by Exercise 010.

### Operational workflow

```text
Shipment ID
    |
    v
Shipment Database Lookup
    |
    v
Shipment Data Validation
    |
    +---- Invalid or Missing Data
    |              |
    |              v
    |        Structured Error
    |
    v
Semantic Policy Search
    |
    v
Retrieved Policy Documents
    |
    v
Policy Applicability Evaluation
    |
    v
Validated Shipment Report
    |
    v
Optional LLM Interpretation
```

The validated report serves as the reliable source of information for any subsequent model-generated explanation.

## 4. Phase 1 — Shipment Data Retrieval

The first phase focused on retrieving shipment records using unique shipment identifiers.

The `get_shipment_details()` function reads the shipment database and searches for the requested record.

The implementation includes error handling for:

- Missing database files.
- File reading errors.
- Invalid JSON content.
- Shipment identifiers that do not exist.

This provides a structured foundation for the investigation process.

### Test shipments

| Shipment ID | Customer | Issue | Priority |
|---|---|---|---|
| SHP-1045 | Caribbean Retail Group | Damaged Packaging | High |
| SHP-2087 | Atlantic Distribution | Delivery Delay | Medium |
| SHP-3092 | Global Medical Supplies | Critical Shipment Exception | Critical |
| SHP-9999 | Not found | Missing shipment record | N/A |

The lookup tests successfully retrieved the three existing shipments and returned an appropriate error for the nonexistent shipment.

**Result:** Shipment database retrieval and missing-record handling worked as expected in the observed tests.

## 5. Phase 2 — Semantic Policy Retrieval

The second phase introduced semantic search using the existing logistics knowledge base.

Rather than relying exclusively on exact keyword matching, the system uses document embeddings to identify policy documents that are semantically related to a logistics question.

The implementation follows this process:

1. Load the logistics policy documents.
2. Build or load the semantic index.
3. Convert the investigation question into a semantic query.
4. Retrieve the top three matching policy documents.
5. Return policy names, similarity scores, and document content.

### Example retrieval question

> A shipment arrived with damaged packaging. What procedures should the team follow?

The semantic retrieval test returned:

| Rank | Policy | Similarity score |
|---|---|---|
| 1 | `damaged_shipment_policy.txt` | 0.7676 |
| 2 | `shipment_escalation_policy.txt` | 0.6430 |
| 3 | `delayed_delivery_policy.txt` | 0.6318 |

The damaged shipment policy ranked highest, matching the primary issue described in the question.

The other policies were retrieved as potentially related documents, but their presence in the results did not automatically establish applicability.

This distinction became important in later reliability improvements.

**Result:** Semantic retrieval successfully identified relevant operational documents.

## 6. Phase 3 — Integrated Shipment Investigation

The next phase connected shipment records with semantic policy retrieval.

The `investigate_shipment()` function retrieves a shipment, constructs a question using its operational information, and searches the policy knowledge base.

This allows the system to investigate different shipment scenarios using the same workflow.

### Investigation results

**SHP-1045 — Damaged Packaging**

The shipment was placed on hold because of visible packaging damage.

The investigation identified the damaged shipment policy as the highest-ranked document.

**SHP-2087 — Delivery Delay**

The shipment had a recorded delivery delay.

The investigation identified the delayed delivery policy as the highest-ranked document.

**SHP-3092 — Critical Shipment Exception**

The shipment involved repeated delivery failures affecting a critical customer commitment.

The investigation identified the shipment escalation policy as the highest-priority result.

**SHP-9999 — Missing Shipment**

The system returned a `not_found` status and an error explaining that the shipment record did not exist.

These tests demonstrated that the application could handle multiple operational scenarios and a missing-record case.

## 7. Phase 4 — Policy Prioritization

Semantic similarity is useful for discovering relevant information, but it does not always represent operational urgency.

For this reason, the system introduced a policy prioritization rule.

When a shipment has:

- Priority: `Critical`
- Status: `Escalation Required`

the shipment escalation policy is prioritized among the retrieved results.

This rule is implemented in the `prioritize_policies()` function.

### Critical shipment example

For shipment `SHP-3092`, the observed results were:

| Policy | Similarity score |
|---|---|
| `shipment_escalation_policy.txt` | 0.7990 |
| `delayed_delivery_policy.txt` | 0.8082 |
| `damaged_shipment_policy.txt` | 0.7534 |

Although the delayed delivery policy had a slightly higher semantic similarity score, the escalation policy was presented first because the shipment met the explicit critical escalation conditions.

This demonstrated an important engineering principle:

**Operational business rules and semantic relevance serve different purposes.**

Semantic search identifies potentially useful information, while deterministic business rules help enforce operational priorities.

The prioritization function reorders retrieved documents; it does not independently retrieve missing policies.

## 8. Phase 5 — Shipment Data Validation

Before generating operational reports, the application validates the shipment record.

The `validate_shipment()` function checks whether the shipment contains the required information.

### Required fields

- `shipment_id`
- `customer`
- `status`
- `issue_type`
- `priority`
- `delivery_confirmed`

The function also verifies that `delivery_confirmed` is a Boolean value.

When validation fails, the system returns structured error information instead of proceeding with an incomplete investigation.

### Why validation matters

An AI system should not assume that missing information represents a specific operational condition.

For example, an unconfirmed delivery does not necessarily prove that a shipment is delayed.

Validation reduces the risk of generating conclusions from incomplete or incorrectly formatted records.

**Result:** The validated investigation path successfully handled the tested existing and nonexistent shipment records.

## 9. Phase 6 — Reliable Report Generation

A major improvement introduced during the exercise was the `generate_reliable_report()` function.

This function generates a structured report using validated shipment data and retrieved policies without requiring the language model to compose the underlying operational facts.

### Report information

The report includes:

- Investigation success status.
- Shipment identifier.
- Customer.
- Shipment status.
- Issue type.
- Priority.
- Delivery confirmation status.
- Shipment description.
- Applicable policies.
- Excluded policies.
- Report source.

### Evidence-based policy filtering

The system introduced a rule to prevent the delayed delivery policy from being treated as applicable when there was no verified evidence of a delivery delay.

For shipment `SHP-1045`, the retrieved policy results included a delayed delivery document.

However, the shipment's actual issue was damaged packaging, and its status was `On Hold`.

The validated report therefore excluded the delayed delivery policy.

### Observed report for SHP-1045

**Shipment:** SHP-1045  
**Customer:** Caribbean Retail Group  
**Status:** On Hold  
**Issue:** Damaged Packaging  
**Priority:** High  
**Delivery confirmed:** False

Applicable policies:

| Policy | Similarity score |
|---|---|
| `damaged_shipment_policy.txt` | 0.7979 |
| `shipment_escalation_policy.txt` | 0.7454 |

Excluded policy:

`delayed_delivery_policy.txt`

Reason:

> No verified evidence of a delivery delay.

This result demonstrated that semantic retrieval and policy applicability should be treated as separate stages.

### Missing shipment test

The reliable report function was also tested with `SHP-9999`.

The system returned:

```json
{
  "success": false,
  "shipment_id": "SHP-9999",
  "errors": [
    "Shipment SHP-9999 not found."
  ]
}
```

The application did not invent a customer, shipment status, or operational recommendation.

**Result:** The deterministic reporting function produced structured, evidence-based results in the observed tests.

## 10. Phase 7 — AI Agent Integration

The application used `smolagents` to expose logistics functions as tools available to a local language model.

The experimental agent was configured with:

- Model: `ollama_chat/qwen2.5:3b`
- API endpoint: `http://localhost:11434`
- Context window: 4096 tokens
- Maximum agent steps: 4

The registered tools included:

- `lookup_shipment`
- `search_policy`
- `get_reliable_shipment_report`

The intended workflow was for the language model to call the appropriate tools and summarize the returned information.

### Agent objective

Given a shipment identifier, the agent should:

1. Request the validated shipment report.
2. Read the returned shipment facts.
3. Identify applicable policies.
4. Explain excluded policies.
5. Produce a concise response without inventing information.

This phase tested the distinction between a functioning tool and an agent's ability to invoke that tool correctly.

## 11. Agent Reliability Evaluation

The agent successfully registered the required tools.

A verification command confirmed that `get_reliable_shipment_report` was available alongside the other registered functions.

During an agent execution, the model also successfully invoked the reliable shipment report tool and received the expected structured shipment information.

However, subsequent steps revealed problems with tool-call formatting.

### Observed errors

The terminal repeatedly displayed:

```text
Error while parsing tool call from model output:
The model output does not contain any JSON blob.
```

The model reached its maximum configured steps without completing a consistently reliable tool-calling sequence.

In its final response, it attempted to describe or reproduce information from the previous tool result.

Although portions of the output matched the validated report, the model's behavior was not sufficiently reliable to treat the complete autonomous workflow as production-ready.

### Important distinction

The problem was not that the Python report function failed.

The report function had already returned valid structured data when called directly.

The failure occurred in the language model's ability to consistently follow the tool-calling protocol.

This distinction prevented unnecessary changes to components that were already functioning correctly.

## 12. Root Cause Analysis

The observed failures indicate a limitation in the reliability of the local model's tool-calling behavior within the configured framework.

The system required the model to:

- Interpret a multi-step investigation request.
- Select an appropriate tool.
- Generate correctly formatted tool-call arguments.
- Read structured tool results.
- Decide whether additional tool calls were necessary.
- Produce a final answer grounded in the returned information.

The model successfully completed some of these operations but failed repeatedly during later tool-calling steps.

The available evidence supports identifying malformed tool-call output as the immediate failure.

It does not establish whether the underlying cause was exclusively model size, prompt complexity, framework compatibility, or another configuration factor.

Additional benchmarking would be required to isolate those causes.

## 13. Engineering Decision

Rather than continuing to add instructions or more complex orchestration logic, the exercise was closed with a clear distinction between the reliable and experimental components.

The following capabilities were retained as successful engineering outcomes:

- Structured shipment retrieval.
- Semantic policy search.
- Critical escalation prioritization.
- Shipment data validation.
- Evidence-based policy filtering.
- Deterministic report generation.
- Structured error handling.

The autonomous tool-calling workflow was classified as experimental because its reliability was not consistently demonstrated.

This decision avoided increasing complexity in a system whose local model was already struggling with the existing workflow.

### Version control checkpoint

The repository retained a previously pushed checkpoint:

`ed48650`

Commit description:

`checkpoint: preserve Exercise 010 RAG agent before reliability improvements`

The checkpoint provides a stable reference for the project.

The subsequent reliability improvements remained local during the observed evaluation and were not automatically considered part of that checkpoint.

## 14. Key Lessons Learned

### 14.1 Retrieval is not the same as applicability

A document can have a high similarity score without being operationally applicable to the shipment being investigated.

Policy selection must consider verified shipment conditions.

### 14.2 Business rules should not depend entirely on the LLM

Critical decisions, such as determining whether a shipment meets escalation conditions, can be implemented through deterministic logic.

This provides more predictable behavior.

### 14.3 Validation should happen before interpretation

The application should verify required fields and data types before asking a language model to interpret shipment information.

### 14.4 Tool registration does not guarantee successful tool calling

A tool may be correctly implemented and registered while the language model still fails to invoke it reliably.

Tool functionality and agent orchestration require separate testing.

### 14.5 Smaller local models have practical limitations

Local models can support experimentation, but successful execution in one step does not guarantee consistent performance across a multi-step workflow.

Model reliability must be measured rather than assumed.

### 14.6 A failed experiment can produce valuable engineering evidence

The autonomous workflow did not achieve the desired consistency.

However, the exercise successfully identified the boundary between reliable Python functionality and unreliable model-generated tool calls.

Documenting this limitation is part of responsible system development.

## 15. Future Improvements

Potential improvements for future exercises include:

**Automated testing**

Develop unit tests for shipment validation, policy prioritization, and report generation.

**Policy applicability rules**

Expand the evidence-based filtering system beyond delivery delays to cover additional shipment exceptions.

**Model benchmarking**

Compare multiple local models using the same shipment scenarios, tool definitions, and evaluation criteria.

**Structured output validation**

Introduce additional checks to verify that model-generated responses match the validated report.

**Performance optimization**

Reduce repeated embedding model initialization and reuse the semantic index when appropriate.

**Observability**

Record tool-call success rates, parsing failures, response times, and unsupported statements.

These improvements should be considered independently and introduced only when they provide measurable value.

## 16. Final Results

| Component | Observed outcome |
|---|---|
| Shipment database lookup | Successful |
| Missing shipment handling | Successful |
| Semantic policy retrieval | Successful |
| Integrated shipment investigation | Successful |
| Critical escalation prioritization | Successful |
| Shipment data validation | Successful in tested scenarios |
| Evidence-based policy filtering | Successful in tested scenario |
| Deterministic report generation | Successful in tested scenarios |
| Tool registration | Successful |
| Autonomous LLM tool calling | Inconsistent |
| Production readiness | Not established |

## 17. Conclusion

Exercise 010 demonstrated how structured shipment information, semantic document retrieval, and deterministic business rules can work together to support logistics investigations.

The project successfully implemented a reliable foundation for retrieving shipment records, identifying relevant operational policies, validating data, and generating evidence-based reports.

The experiment also exposed an important limitation of local language model orchestration.

Although Qwen 2.5 3B was able to invoke a tool successfully, it did not consistently maintain the required tool-calling format throughout the agent workflow.

As a result, the most dependable component of the project was the validated Python reporting pipeline rather than the autonomous language model.

The central engineering lesson was that **an AI agent's usefulness depends not only on its language capabilities, but also on the reliability of its tools, data validation, operational rules, and execution boundaries.**

This exercise provides a practical foundation for developing more reliable logistics AI systems in future projects.