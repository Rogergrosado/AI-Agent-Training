from shipment_exception_routing import shipment_graph, shipment_001

# Expected outcomes for each exception type
test_cases = {
    "delay": (
        "medium",
        "Transportation Operations",
        False,
        "Contact carrier and request updated ETA.",
    ),
    "documentation": (
        "high",
        "Documentation & Compliance",
        True,
        "Verify missing or incorrect shipping documents.",
    ),
    "damage": (
        "critical",
        "Claims & Quality Assurance",
        True,
        "Document damage and initiate claims review.",
    ),
    "none": (
        "low",
        "Logistics Operations",
        False,
        "Continue standard shipment monitoring.",
    ),
    "unknown": (
        "unknown",
        "Operations Supervisor",
        True,
        "Investigate unclassified shipment exception.",
    ),
}

for exception_type, (
    expected_priority,
    expected_department,
    expected_review,
    expected_action,
) in test_cases.items():
    shipment = shipment_001.copy()
    shipment["exception_type"] = exception_type

    result = shipment_graph.invoke(shipment)

    assert result["priority"] == expected_priority
    assert result["assigned_department"] == expected_department
    assert result["requires_human_review"] == expected_review
    assert result["recommended_action"] == expected_action

    print(f"PASS: {exception_type}")

print("\nAll 5 workflow tests passed!")
