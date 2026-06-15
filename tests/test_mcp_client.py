import asyncio

from tools.mcp.base_client import JsonRpcMCPClient


def _handler(payload: dict):
    if payload["method"] == "tools/list":
        return {"result": {"tools": [{"name": "web_search"}]}}
    if payload["method"] == "tools/call":
        return {"result": {"output": payload["params"]}}
    return {"error": {"code": -32601, "message": "Method not found"}}


def test_list_tools() -> None:
    client = JsonRpcMCPClient(request_handler=_handler)
    tools = asyncio.run(client.list_tools())
    assert tools == [{"name": "web_search"}]


def test_call_tool() -> None:
    client = JsonRpcMCPClient(request_handler=_handler)
    result = asyncio.run(client.call_tool("web_search", {"query": "langgraph"}))
    assert result.is_error is False
    assert result.content["output"]["name"] == "web_search"
