from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Callable


@dataclass(frozen=True)
class MCPToolResult:
    content: dict[str, Any]
    is_error: bool = False


class BaseMCPClient(ABC):
    @abstractmethod
    async def list_tools(self) -> list[dict[str, Any]]:
        """Return available tool descriptors."""

    @abstractmethod
    async def call_tool(self, name: str, arguments: dict[str, Any] | None = None) -> MCPToolResult:
        """Invoke a tool and return structured output."""


class JsonRpcMCPClient(BaseMCPClient):
    def __init__(
        self,
        request_handler: Callable[[dict[str, Any]], dict[str, Any]],
    ) -> None:
        self._request_handler = request_handler
        self._request_id = 0

    def _next_request_id(self) -> int:
        self._request_id += 1
        return self._request_id

    async def list_tools(self) -> list[dict[str, Any]]:
        payload = {
            "jsonrpc": "2.0",
            "id": self._next_request_id(),
            "method": "tools/list",
            "params": {},
        }
        response = self._request_handler(payload)
        tools = response.get("result", {}).get("tools", [])
        return tools if isinstance(tools, list) else []

    async def call_tool(self, name: str, arguments: dict[str, Any] | None = None) -> MCPToolResult:
        payload = {
            "jsonrpc": "2.0",
            "id": self._next_request_id(),
            "method": "tools/call",
            "params": {
                "name": name,
                "arguments": arguments or {},
            },
        }
        response = self._request_handler(payload)
        if "error" in response:
            return MCPToolResult(content=response["error"], is_error=True)
        return MCPToolResult(content=response.get("result", {}), is_error=False)
