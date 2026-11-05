
# Exercise 014 — Logistics Research & Decision Support Agent

## Objective

Build a logistics AI agent that combines structured shipment data,
information retrieval, research tools, and decision-support logic.

The agent must provide evidence-based recommendations while clearly
distinguishing verified information from uncertainty.

## Phase 1 — Architecture and Data Design

### Dataset

File: `projects/logistics_research/data/shipments.json`

The dataset contains four fictional logistics scenarios:

1. SHP-001 — Normal shipment
2. SHP-002 — Delayed shipment
3. SHP-003 — Customs hold
4. SHP-004 — Critical shipment

### Data Contract

Each shipment must contain:

- shipment_id: unique, non-empty string
- origin: non-empty string
- destination: non-empty string
- transport_mode: ocean, air, or road
- status: in_transit, delayed, or customs_hold
- eta: valid date in YYYY-MM-DD format
- exception: string or null
- priority: low, medium, high, or critical

### Initial Decision Rules

- Normal: report shipment status and recommend monitoring.
- Delayed: investigate the cause and assess delivery impact.
- Customs hold: identify documentation issues and recommend review.
- Critical: prioritize investigation and recommend escalation.

### Reliability Requirements

1. Never invent shipment information.
2. Distinguish dataset facts from external research.
3. Identify missing information.
4. Explain the evidence supporting each recommendation.
5. Avoid treating model-generated text as verified evidence.

## Planned Architecture

Shipment Dataset
    -> Data Validation
    -> Shipment Analysis
    -> Information Retrieval
    -> Research Tools
    -> Decision Support
    -> Evidence-Based Report

## Phase 1 Status

- Project structure created.
- Initial shipment dataset created.
- JSON syntax validated.
- Data contract defined.
- Architecture documented.


## Phase 2 — Implemented System Architecture

### System Overview

Exercise 014 evolved from an initial logistics decision-support concept into a modular research workflow that combines structured shipment analysis, external information retrieval, and evidence quality assessment.

The system uses deterministic Python functions for shipment classification and reporting. External research provides supplementary context rather than replacing the shipment dataset as the source of operational facts.

### Implemented Components

| Component | Responsibility |
|---|---|
| `data/shipments.json` | Stores four fictional shipment scenarios. |
| `shipment_analysis.py` | Loads shipment records, classifies operational conditions, and generates decision reports. |
| `research_tools.py` | Generates research queries using shipment information. |
| `external_research.py` | Retrieves external research metadata and handles search failures. |
| `evidence_quality.py` | Evaluates source relevance, traceability, and verification limitations. |
| `research_workflow.py` | Coordinates shipment analysis, research, and evidence assessment. |

### Workflow

```text
Shipment Dataset
       |
       v
Shipment Classification
       |
       v
Decision Support Report
       |
       v
Is External Research Required?
       |
       +---- No ----> Return Decision Report
       |
       +---- Yes
              |
              v
       Generate Research Query
              |
              v
       Retrieve External Sources
              |
              v
       Assess Evidence Quality
              |
              v
       Return Structured Research Report
```

### Engineering Principles

1. Preserve shipment information from the original dataset.
2. Apply deterministic classification rules before external research.
3. Separate internal operational facts from external research metadata.
4. Evaluate evidence without assuming that retrieved sources verify shipment-specific claims.
5. Preserve useful operational results when external research fails.
6. Avoid generating unsupported conclusions or fabricated evidence.

## Phase 3 — External Research and Evidence Quality

### External Research

The research component retrieves source metadata such as publication titles, URLs, publishers, and publication dates when available.

A successful search does not automatically establish that a publication supports a specific operational conclusion.

### Evidence Assessment

The evidence quality component distinguishes between:

- Source relevance to the research query.
- Source traceability through identifying metadata.
- Verification of publication content.
- Support for shipment-specific claims.
- Explicit evidence limitations.

Retrieving metadata is not equivalent to verifying the full publication.

### Research Failure Handling

The workflow handles unsuccessful external searches without discarding the original shipment analysis.

During live execution, an HTTP 429 response was observed, indicating that the external service had limited requests.

The workflow retained the shipment decision report, recorded the research error, and returned empty source and assessment collections rather than inventing evidence.

## Phase 4 — Automated Testing

The project uses Python's `unittest` framework.

The latest confirmed test execution completed:

**36 tests — OK**

The test suite covers:

- Shipment data loading and classification.
- Shipment lookup and missing records.
- Priority-based escalation.
- Research query generation and input validation.
- External research success and failure scenarios.
- Workflow integration.
- Evidence quality assessment.
- Evidence assessment behavior for successful, empty, and failed research results.

The tests verify expected behavior across the implemented test cases. They do not independently establish the scientific reliability of retrieved publications or guarantee uninterrupted access to external research services.

## Phase 5 — Current Results and Limitations

### Confirmed Results

- Four fictional logistics scenarios are available.
- Structured shipment decision reports are generated.
- External research is integrated into the workflow.
- Evidence quality assessments are included when applicable.
- The system preserves operational decisions when research is unavailable.
- All 36 automated tests passed in the latest confirmed execution.

### Current Limitations

1. The shipment dataset is fictional and limited to four scenarios.
2. External research depends on service availability and request limits.
3. Retrieved publication metadata does not establish full-content verification.
4. Evidence relevance does not prove a shipment-specific causal relationship.
5. The current workflow is a learning prototype, not a production logistics platform.

### Engineering Lessons

The central lesson of Exercise 014 is that reliable decision support requires more than retrieving information.

A trustworthy workflow must separate operational facts, external research, evidence quality, and uncertainty. It must also remain useful when external services fail.

This architecture provides a foundation for future logistics intelligence systems, including exception monitoring, supply chain research, and evidence-aware operational reporting.
