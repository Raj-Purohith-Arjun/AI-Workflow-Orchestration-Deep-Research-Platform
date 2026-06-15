from __future__ import annotations

from fastapi import FastAPI

from api.routes.workflow import router as workflow_router

app = FastAPI(title="AI Workflow Orchestration Platform", version="0.1.0")
app.include_router(workflow_router)
