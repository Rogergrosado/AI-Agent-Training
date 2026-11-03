from logistics_multi_agent_system import (
    create_initial_state,
    shipment_agent,
    validate_shipment_agent,
    build_multi_agent_workflow,
)


def test_valid_shipment_workflow(app):
    """Verify successful multi-agent coordination."""

    result = app.invoke(create_initial_state("SHP-1045"))

    assert result["status"] == "decision_prepared"
    assert result["errors"] == []
    assert result["shipment"]["shipment_id"] == "SHP-1045"
    assert len(result["policies"]) > 0
    assert result["exception_analysis"]
    assert result["decision"]

    decision = result["decision"]

    assert decision["requires_human_review"] is True
    assert decision["execution_authorized"] is False

    expected_history = [
        "Shipment Agent: shipment retrieved",
        "Shipment Validation: passed",
        "Policy Agent: retrieved 3 policies",
        "Exception Analysis Agent: analysis completed",
        "Operational Decision Agent: recommendation prepared",
    ]

    assert result["agent_history"] == expected_history

    print("PASS: Valid multi-agent workflow")


def test_missing_shipment_workflow(app):
    """Verify early termination for nonexistent shipments."""

    result = app.invoke(create_initial_state("SHP-9999"))

    assert result["status"] == "not_found"
    assert result["shipment"] == {}
    assert result["policies"] == []
    assert result["decision"] == {}
    assert result["errors"]
    assert len(result["agent_history"]) == 1

    print("PASS: Missing shipment workflow")


def test_incomplete_shipment_validation():
    """Verify rejection of incomplete shipment data."""

    state = create_initial_state("SHP-TEST")

    state["shipment"] = {
        "shipment_id": "SHP-TEST",
        "status": "On Hold",
    }

    state.update(validate_shipment_agent(state))

    assert state["status"] == "validation_failed"
    assert state["errors"]
    assert state["policies"] == []
    assert state["decision"] == {}

    print("PASS: Incomplete shipment validation")


def run_tests():
    print("EXERCISE 012 — AUTOMATED INTEGRATION TESTS")
    print("-" * 55)

    app = build_multi_agent_workflow()

    test_valid_shipment_workflow(app)
    test_missing_shipment_workflow(app)
    test_incomplete_shipment_validation()

    print("-" * 55)
    print("ALL EXERCISE 012 TESTS PASSED")


if __name__ == "__main__":
    run_tests()
