from __future__ import annotations

from typing import Any

from workflow.state import ApprovalStatus, GraphWorkflowState


def _to_list(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value]
    return []


def plan_node(state: GraphWorkflowState) -> GraphWorkflowState:
    plan_steps = _to_list(state.get("plan_steps"))
    goal = str(state.get("goal", "")).strip()
    if not plan_steps and goal:
        plan_steps = [f"Investigate: {goal}", "Prepare findings for approval"]
    return {"plan_steps": plan_steps, "next_action": "research"}


def research_node(state: GraphWorkflowState) -> GraphWorkflowState:
    notes = _to_list(state.get("research_notes"))
    if not notes:
        notes = ["Initial research notes captured"]
    return {"research_notes": notes, "next_action": "approval"}


def approval_gate_node(state: GraphWorkflowState) -> GraphWorkflowState:
    return {
        "approval_status": str(state.get("approval_status", ApprovalStatus.PENDING.value)),
        "next_action": "approval",
    }


def execute_node(state: GraphWorkflowState) -> GraphWorkflowState:
    actions = _to_list(state.get("pending_actions"))
    if not actions:
        actions = ["Execution completed"]
    return {"pending_actions": actions, "next_action": "complete"}


def route_after_approval(state: GraphWorkflowState) -> str:
    approval_value = str(state.get("approval_status", "")).strip().lower()
    if approval_value == ApprovalStatus.APPROVED.value:
        return "execute"
    return "research"


def build_primary_workflow_graph():
    from langgraph.graph import END, START, StateGraph

    graph = StateGraph(GraphWorkflowState)
    graph.add_node("plan", plan_node)
    graph.add_node("research", research_node)
    graph.add_node("approval_gate", approval_gate_node)
    graph.add_node("execute", execute_node)

    graph.add_edge(START, "plan")
    graph.add_edge("plan", "research")
    graph.add_edge("research", "approval_gate")
    graph.add_conditional_edges(
        "approval_gate",
        route_after_approval,
        {
            "execute": "execute",
            "research": "research",
        },
    )
    graph.add_edge("execute", END)

    return graph.compile(interrupt_before=["approval_gate"])
