# Architecture Overview

## Workflow lifecycle

The orchestration graph cycles through planning, research, and approval checkpoints before execution. Approval failures route back to research to maintain a controlled iterative loop.

## Integration model

MCP-compatible tools are accessed through a base client abstraction, enabling transport-specific implementations without changing orchestration logic.

## API contract

The API accepts strict Pydantic workflow state payloads and returns structured state documents suitable for downstream automation.
