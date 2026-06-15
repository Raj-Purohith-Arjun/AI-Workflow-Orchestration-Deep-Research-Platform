import pytest
from pydantic import ValidationError

from workflow.state import ApprovalStatus, WorkflowStateModel


def test_state_roundtrip_to_graph_state() -> None:
    model = WorkflowStateModel(request_id="req-1", goal="Evaluate MCP compatibility")

    graph_state = model.to_graph_state()
    restored = WorkflowStateModel.from_graph_state(graph_state)

    assert restored.request_id == "req-1"
    assert restored.goal == "Evaluate MCP compatibility"
    assert restored.approval_status == ApprovalStatus.PENDING


def test_state_requires_non_empty_goal() -> None:
    with pytest.raises(ValidationError) as exc_info:
        WorkflowStateModel(request_id="req-1", goal="")
    assert "goal" in str(exc_info.value)
