# AI Workflow Orchestration & Deep Research Platform

Enterprise workflow orchestration platform for multi-step AI research operations with explicit approval controls and full traceability.

## Business Outcomes

- Reduces human oversight time in document research workflows through structured approval gates and repeatable execution paths.
- Improves auditability with deterministic state transitions and trace-ready orchestration design.
- Standardizes tool invocation through MCP-compatible interfaces.

## Architecture Decisions

### Orchestration Core (LangGraph)

- Stateful, cyclical workflow modeled as a LangGraph graph.
- Primary phases: `plan -> research -> approval_gate -> execute`.
- Human-in-the-loop interrupt is enforced before `approval_gate` to support explicit approval for critical actions.

### Tool Integration (MCP)

- Tool calls are abstracted behind a base MCP client (`tools/mcp/base_client.py`).
- JSON-RPC message shape is enforced for compatibility with MCP server implementations.

### API Layer (FastAPI + Pydantic v2)

- FastAPI serves typed endpoints under `/api/v1/workflows`.
- Pydantic v2 models provide strict validation and structured outputs.

### Observability (LangSmith)

- Runtime is designed for LangSmith trace integration via environment configuration (`LANGCHAIN_TRACING_V2`, `LANGCHAIN_API_KEY`).

### Deployment

- Poetry-managed dependency graph via `pyproject.toml`.
- Production container image with `Dockerfile`.
- Local multi-service development topology in `docker-compose.yml`.

## Repository Layout

- `src/` — orchestration and domain logic
- `api/` — FastAPI app and route handlers
- `tools/` — MCP client/server components
- `tests/` — pytest coverage
- `docs/` — architecture and operational documentation

## Environment Setup

```bash
poetry install
poetry run uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

## API Usage

### Create workflow state

```bash
curl -X POST http://localhost:8000/api/v1/workflows \
  -H "Content-Type: application/json" \
  -d '{
    "request_id": "req-001",
    "goal": "Research enterprise MCP adoption patterns"
  }'
```

## Human Approval Flow

1. Graph plans and gathers research.
2. Execution pauses at `approval_gate` interrupt.
3. A human reviewer sets `approval_status`.
4. Graph resumes to `execute` when approved, or cycles back to `research` when not approved.

## Development Standards

- Strict typing across runtime and API models.
- Defensive error handling in integration boundaries.
- Semantic commit messages (`feat:`, `fix:`, `refactor:`, `docs:`).
