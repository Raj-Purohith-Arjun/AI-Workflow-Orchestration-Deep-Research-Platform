from workflow.graph import route_after_approval
from workflow.state import ApprovalStatus


def test_route_after_approval_execute() -> None:
    assert route_after_approval({"approval_status": ApprovalStatus.APPROVED.value}) == "execute"


def test_route_after_approval_research_when_pending() -> None:
    assert route_after_approval({"approval_status": ApprovalStatus.PENDING.value}) == "research"
