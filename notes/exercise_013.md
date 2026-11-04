
# Exercise 013 — Shipment Exception Routing with LangGraph

## Objective

Build a deterministic logistics workflow using LangGraph to classify shipment exceptions, select the appropriate operational route, and update a shared shipment state.

## Technologies

- Python 3.12
- LangGraph 1.2.19
- TypedDict
- Automated tests with Python assertions

## Workflow Architecture

The workflow separates shipment processing into three responsibilities:

1. **Evaluation:** Determine the exception priority.
2. **Routing:** Select the appropriate handling node.
3. **Handling:** Assign a department, recommend an action, and determine whether human review is required.

## Supported Shipment Exceptions

| Exception | Priority | Department | Human Review |
|---|---|---|---|
| Delay | Medium | Transportation Operations | No |
| Documentation | High | Documentation & Compliance | Yes |
| Damage | Critical | Claims & Quality Assurance | Yes |
| None | Low | Logistics Operations | No |
| Unknown | Unknown | Operations Supervisor | Yes |

## State Management

A shared `ShipmentState` TypedDict stores shipment information and workflow outputs.

LangGraph nodes update the state while conditional routing determines which handling function executes.

## Automated Testing

The test suite validates five shipment scenarios.

Each scenario checks four outputs:

- Priority
- Assigned department
- Recommended action
- Human review requirement

**Result:** 5 scenarios passed, with 20 successful assertions.

## Key Engineering Lessons

- Deterministic routing improves predictability.
- Shared state allows workflow nodes to exchange information.
- Conditional edges separate decisions from execution.
- Human review can be explicitly required for sensitive exceptions.
- Automated tests protect operational rules from regressions.
- The `if __name__ == "__main__":` guard prevents demonstrations from running during module imports.

## Files

- `exercises/shipment_exception_routing.py`
- `exercises/exercise_013_tests.py`
- `notes/exercise_013.md`

## Conclusion

Exercise 013 demonstrates how LangGraph can orchestrate structured logistics decisions through explicit state transitions, conditional routing, and independently tested business rules.
