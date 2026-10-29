
# Exercise 007 — Logistics Policy Decision Agent

**Course:** Hugging Face AI Agents Course — Unit 2.1: smolagents  
**Date:** October 28, 2026  
**Status:** Completed Prototype

## Objective

Develop a logistics decision-support prototype that combines shipment exception analysis, company policy retrieval, decision validation, and AI-powered tool calling.

## What I Built

I integrated the capabilities developed in Exercises 005 and 006 into a policy-based logistics decision system.

The system can:

- Analyze shipment status and delivery delays.
- Identify operational priorities and recommended actions.
- Retrieve relevant company logistics policies.
- Validate recommendations against policy rules.
- Handle unknown shipment identifiers.
- Generate consistent operational reports.
- Expose decision analysis through a smolagents tool.

## Technologies Used

- Python 3.12.4
- smolagents
- Ollama
- Qwen2 1.5B
- LiteLLMModel
- ToolCallingAgent
- JSON
- Git and GitHub

## System Architecture

The prototype combines three main components:

1. Shipment exception analysis from Exercise 005.
2. Logistics policy retrieval from Exercise 006.
3. Policy decision validation and reporting from Exercise 007.

The AI agent can call the `evaluate_logistics_decision` tool to retrieve structured decision information.

A separate deterministic reporting function ensures that the application can generate complete reports without depending on the language model to reproduce every field correctly.

## Testing Results

| Test Case | Expected Result | Status |
|---|---|---|
| SHP-001 | No action required | Passed |
| SHP-004 | Escalate to logistics manager | Passed |
| SHP-999 | Verify shipment ID | Passed |

The validated report and reliable-output tests produced the expected results for all three scenarios.

## Challenges Encountered

During development, the local Qwen2 1.5B model sometimes repeated tool calls, generated malformed tool-call structures, or omitted requested information from its final answer.

These issues demonstrated the limitations of relying exclusively on a small language model for structured operational reporting.

## Engineering Improvements

To improve reliability, I implemented:

- Explicit policy validation.
- Structured decision dictionaries.
- Handling for unknown shipments.
- Consistent report formatting.
- A deterministic application-facing reporting function.

These improvements preserve the AI agent as an experimental component while providing a reliable reporting path.

## Current Limitations

- Shipment records and policies are simulated.
- The policy knowledge base is small.
- Policy retrieval uses keyword-based relevance ranking.
- The local language model may produce incomplete responses.
- The reliable reporting function operates separately from the AI agent.
- The prototype has not been evaluated using real operational data.

## Lessons Learned

This exercise helped me understand how multiple AI agent components can be integrated into a decision-support workflow.

I also learned that AI-generated responses should not be treated as authoritative operational decisions without validation.

Combining AI tool calling with deterministic business rules creates a more reliable foundation for logistics automation.

## Future Improvements

Potential enhancements include:

- Automated regression tests.
- More comprehensive policy coverage.
- Structured output validation.
- A persistent shipment database.
- Integration with real logistics systems.
- Improved agent orchestration.

## Conclusion

Exercise 007 represents another step toward building practical AI-assisted logistics systems.

By integrating exception analysis, policy retrieval, validation, and reporting, I developed a prototype that demonstrates how AI agents can support operational decision-making while maintaining explicit business-rule controls.
