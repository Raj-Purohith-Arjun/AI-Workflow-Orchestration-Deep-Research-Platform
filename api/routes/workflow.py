from __future__ import annotations

from fastapi import APIRouter

from api.schemas import CreateWorkflowRequest, WorkflowResponse
from workflow.state import WorkflowStateModel

router = APIRouter(prefix="/api/v1/workflows", tags=["workflows"])


@router.post("", response_model=WorkflowResponse)
def create_workflow(payload: CreateWorkflowRequest) -> WorkflowResponse:
    state = WorkflowStateModel(request_id=payload.request_id, goal=payload.goal)
    return WorkflowResponse(state=state)
