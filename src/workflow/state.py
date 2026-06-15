from __future__ import annotations

from enum import Enum
from typing import Any, Literal, TypedDict

from pydantic import BaseModel, ConfigDict, Field


class ApprovalStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class GraphWorkflowState(TypedDict, total=False):
    request_id: str
    goal: str
    plan_steps: list[str]
    research_notes: list[str]
    pending_actions: list[str]
    approval_status: str | ApprovalStatus
    approved_by: str | None
    next_action: str
    metadata: dict[str, Any]


class WorkflowStateModel(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    request_id: str
    goal: str = Field(min_length=1)
    plan_steps: list[str] = Field(default_factory=list)
    research_notes: list[str] = Field(default_factory=list)
    pending_actions: list[str] = Field(default_factory=list)
    approval_status: ApprovalStatus = ApprovalStatus.PENDING
    approved_by: str | None = None
    next_action: Literal["plan", "research", "approval", "execute", "complete"] = "plan"
    metadata: dict[str, Any] = Field(default_factory=dict)

    def to_graph_state(self) -> GraphWorkflowState:
        payload = self.model_dump(mode="python")
        return GraphWorkflowState(**payload)

    @classmethod
    def from_graph_state(cls, state: GraphWorkflowState) -> "WorkflowStateModel":
        return cls.model_validate(state)
