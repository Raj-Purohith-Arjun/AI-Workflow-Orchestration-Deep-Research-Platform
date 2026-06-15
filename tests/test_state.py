from workflow.state import ApprovalStatus, WorkflowStateModel


def test_state_roundtrip_to_graph_state() -> None:
    model = WorkflowStateModel(request_id="req-1", goal="Evaluate MCP compatibility")

    graph_state = model.to_graph_state()
    restored = WorkflowStateModel.from_graph_state(graph_state)

    assert restored.request_id == "req-1"
    assert restored.goal == "Evaluate MCP compatibility"
    assert restored.approval_status == ApprovalStatus.PENDING


def test_state_requires_non_empty_goal() -> None:
    try:
        WorkflowStateModel(request_id="req-1", goal="")
        raise AssertionError("Expected validation error")
    except Exception as exc:  # noqa: BLE001
        assert "goal" in str(exc)
