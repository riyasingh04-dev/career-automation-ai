import abc
from typing import Dict, Any, List

class MCPTool(abc.ABC):
    @property
    @abc.abstractmethod
    def name(self) -> str:
        pass

    @property
    @abc.abstractmethod
    def description(self) -> str:
        pass

    @abc.abstractmethod
    async def execute(self, **kwargs) -> Any:
        pass

class MCPServer:
    def __init__(self):
        self._tools: Dict[str, MCPTool] = {}

    def register_tool(self, tool: MCPTool):
        self._tools[tool.name] = tool

    async def call_tool(self, tool_name: str, **kwargs) -> Any:
        if tool_name not in self._tools:
            raise ValueError(f"Tool {tool_name} not found")
        return await self._tools[tool_name].execute(**kwargs)

    def list_tools(self) -> List[Dict[str, str]]:
        return [
            {"name": tool.name, "description": tool.description}
            for tool in self._tools.values()
        ]
