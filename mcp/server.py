from .base import MCPTool, MCPServer

# Global instance
mcp_server = MCPServer()

# Utility to load tools
def load_tools():
    from mcp.tools.browser_tool import BrowserTool
    from mcp.tools.file_tool import FileTool
    from mcp.tools.llm_tool import LLMTool
    
    mcp_server.register_tool(BrowserTool())
    mcp_server.register_tool(FileTool())
    mcp_server.register_tool(LLMTool())

load_tools()
