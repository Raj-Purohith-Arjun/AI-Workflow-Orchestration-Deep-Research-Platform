from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from workflow.state import WorkflowStateModel


class CreateWorkflowRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    request_id: str
    goal: str


class WorkflowResponse(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    state: WorkflowStateModel
