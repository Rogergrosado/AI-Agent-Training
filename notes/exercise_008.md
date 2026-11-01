# Exercise 008 — Multimodal Logistics Research Agent

**Project:** AI Agent Training  
**Domain:** Logistics, Supply Chain Management, and Industrial Engineering  
**Status:** Implementation and integration testing completed  
**Technologies:** Python, Ollama, Local Vision-Language Model, DDGS, JSON, Git

---

## 1. Overview

Exercise 008 explores how artificial intelligence can combine visual analysis with external web research to support logistics-related investigations.

The project focuses on identifying packaging and handling symbols from an image of shipping boxes, evaluating recognition performance against reference labels, researching the detected symbols, and producing a structured report.

Rather than treating AI-generated interpretations as verified operational instructions, the system preserves uncertainty and requires human verification.

The exercise demonstrates a modular approach to multimodal AI development.

## 2. Learning Objectives

The primary objectives were to:

1. Analyze a logistics-related image using a local vision-language model.
2. Extract structured descriptions of packaging symbols.
3. Compare detected labels against a predefined ground-truth dataset.
4. Evaluate recognition using precision, recall, and F1 score.
5. Conduct automated web research on identified symbols.
6. Combine visual observations and research findings into a structured JSON report.
7. Preserve traceability, uncertainty, and human oversight.

## 3. System Architecture

The implementation separates visual recognition, evaluation, web research, and integration into independent Python modules.

```text
Packaging Image
      |
      v
multimodal_logistics_agent.py
      |
      v
Visual Analysis JSON
      |
      +--------------------------+
      |                          |
      v                          v
exercise_008_evaluator.py    exercise_008_integrator.py
      |                          |
      v                          v
Ground-Truth Benchmark     logistics_web_search.py
                                 |
                                 v
                          Web Research JSON
                                 |
                                 v
                          Integrated Report
```

The integrator can reuse an existing visual analysis JSON file, allowing research and reporting to run without repeating model inference.

This separation also makes it possible to investigate individual failures without modifying the visual recognition agent.

## 4. Visual Analysis

The visual analysis module processes an image containing cardboard shipping boxes with several packaging-related markings.

The test image includes graphical elements such as recycling, waste disposal, upward arrows, an umbrella, a snowflake, a fragile-glass symbol, and a numeric marking.

The model produces structured JSON containing information such as:

- Symbol label
- Visual evidence
- Approximate location
- Possible interpretation
- Confidence reported by the model
- Verification status
- Uncertainties and quality warnings

These outputs are treated as model predictions rather than independently verified detections.

The system does not assume that identifying a symbol automatically establishes its regulatory meaning or the correct handling procedure.

## 5. Ground Truth and Benchmarking

Two reference datasets were retained for different evaluation purposes.

**`exercise_008_ground_truth.json`** contains a broader set of 15 expected handling-symbol categories.

**`exercise_008_generic_ground_truth.json`** contains six expected symbol categories for the generic shipping-box test image, along with reference occurrence counts.

The evaluation module supports strict label comparison and alias-aware comparison.

### Strict Label Matching

Strict matching compares normalized predicted labels with expected labels without treating related expressions as equivalent.

For example, a predicted label such as `Umbrella` may fail to match the expected label `Keep Dry`, even when both refer to the same visual marking.

### Alias-Aware Matching

Alias-aware evaluation recognizes predefined relationships between certain labels, such as:

- `Arrows` → `This Way Up`
- `Umbrella` → `Keep Dry`
- `Recycling` → `Recyclable`
- `Waste Disposal` → `Dispose Properly`

This provides a more useful comparison when the model describes the visual appearance of a marking instead of using its standardized handling label.

### Recorded Benchmark Result

| Metric | Result |
|---|---:|
| True positives | 5 |
| False positives | 3 |
| False negatives | 1 |
| Precision | 62.50% |
| Recall | 83.33% |
| F1 score | 71.43% |

These results were obtained using alias-aware comparison on the generic-box reference test.

The benchmark evaluates unique label matching, not individual symbol detection accuracy or physical occurrence counts.

A successful alias match does not prove that the model correctly located or interpreted every symbol in the image.

## 6. Web Research Module

**File:** `exercises/logistics_web_search.py`

The research module uses DDGS to retrieve public web search results related to packaging and handling symbols.

Its responsibilities include:

- Normalizing common symbol labels.
- Building symbol-specific search queries.
- Retrieving search results.
- Filtering URLs.
- Removing duplicate URLs within each query.
- Preserving titles, URLs, and snippets.
- Recording search failures.
- Saving timestamped JSON outputs.

Search results are categorized using statuses such as:

- `results_found`
- `no_results`
- `search_error`

The module deliberately distinguishes retrieved search information from verified source documentation.

Search snippets may be incomplete, inaccurate, or unrelated to the exact symbol shown in the image.

## 7. Visual and Web Integration

**File:** `exercises/exercise_008_integrator.py`

The integration module connects the visual model's symbol predictions with corresponding web research records.

It supports an automated workflow that:

1. Loads an existing visual analysis JSON file.
2. Extracts the predicted symbol labels.
3. Initiates web research for the detected symbols.
4. Saves the research results.
5. Matches research records to visual predictions.
6. Generates an integrated JSON report.

Each integrated symbol retains its original visual evidence and model interpretation, along with its research status and available sources.

The integration does not convert preliminary research into verified operational instructions.

### Recorded Integration Test

| Measurement | Result |
|---|---:|
| Visual symbols processed | 8 |
| Research records matched | 8 |
| Successful research results | 4 |
| Search errors | 4 |

The successful integration of eight records demonstrates that the system connected visual labels to corresponding research records.

However, only four research operations returned usable results in that execution.

The remaining four were recorded as search errors rather than silently treated as successful investigations.

## 8. Reliability and Error Handling

Several reliability challenges were observed during development.

### Inconsistent Visual Predictions

Different model executions produced different symbol labels and classifications.

This demonstrated that local vision-language model outputs may vary across runs, even when the same input image is used.

### Structured Output Failures

Some model responses contained malformed JSON or incomplete information.

The workflow therefore needed to account for model output failures rather than assuming every response would be valid.

### Label Ambiguity

Visual descriptions such as `Arrows`, `Umbrella`, and `Number 2` do not necessarily communicate the full operational meaning of a packaging marking.

Alias-aware evaluation improved label comparison, but it did not eliminate the need for visual and semantic verification.

### Web Search Errors

Automated web searches occasionally failed to return results.

The research module records these failures explicitly, allowing the integration stage to continue without inventing missing sources.

### Confidence Limitations

A model-reported confidence value such as `high` is not a calibrated statistical accuracy measurement.

Consequently, confidence alone is insufficient to authorize logistics decisions.

## 9. Human Verification and Operational Safety

The system is designed as a research and decision-support prototype, not an autonomous compliance authority.

Human review remains necessary before making decisions involving:

- Fragile cargo handling
- Moisture protection
- Temperature-sensitive shipments
- Stacking restrictions
- Packaging disposal requirements
- Regulatory or contractual compliance

The workflow preserves source references and uncertainty so that a human reviewer can investigate the original evidence.

No search result or AI-generated interpretation is treated as proof of compliance.

## 10. Project Files

| File | Responsibility |
|---|---|
| `multimodal_logistics_agent.py` | Local visual analysis and structured predictions |
| `exercise_008_evaluator.py` | Benchmarking and recognition evaluation |
| `exercise_008_ground_truth.json` | Broader reference symbol dataset |
| `exercise_008_generic_ground_truth.json` | Generic-box image reference labels and occurrence counts |
| `logistics_web_search.py` | Independent web research |
| `exercise_008_integrator.py` | Automated research and report integration |
| `notes/exercise_008.md` | Technical documentation |

Earlier evaluator variants were archived separately to preserve development history without cluttering the active exercise directory.

## 11. Key Engineering Lessons

**1. Visual recognition and semantic interpretation are different tasks.**

A model may identify the appearance of a symbol without reliably understanding its operational significance.

**2. Evaluation methodology matters.**

Strict and alias-aware scoring answer different questions. A higher alias-aware F1 score does not necessarily indicate better visual perception.

**3. Modularity improves reliability.**

Separating image analysis, evaluation, research, and integration reduces coupling and makes individual components easier to test.

**4. External research introduces new failure modes.**

Web access expands the system's information sources but also introduces availability problems, irrelevant results, and source-quality concerns.

**5. Human oversight remains essential.**

AI can organize observations and research efficiently, but unverified predictions should not directly determine cargo handling or compliance decisions.

## 12. Future Improvements

Potential future enhancements include:

- More robust JSON validation.
- Expanded image test datasets.
- Per-symbol location and occurrence verification.
- Additional evaluation runs to measure prediction consistency.
- Improved search retry and error recovery.
- Source relevance ranking.
- Retrieval and verification of authoritative source documents.
- More structured reporting for logistics operations.

These improvements are future development opportunities, not capabilities claimed to be completed in this exercise.

## 13. Conclusion

Exercise 008 established a modular multimodal logistics research workflow that connects local image analysis, benchmark evaluation, automated web research, and structured JSON reporting.

The generic-box benchmark achieved an alias-aware F1 score of **71.43%**, while the automated integration successfully connected all eight visual predictions to research records in the recorded test. Four of those research operations returned usable results.

The exercise also demonstrated important limitations involving visual consistency, label ambiguity, search reliability, and unverified source information.

The main outcome is a working technical prototype that illustrates how multimodal AI can support logistics research while maintaining clear boundaries between model predictions, external evidence, and human operational judgment.