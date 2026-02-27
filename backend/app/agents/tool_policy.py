from typing import List, Set

class ToolPolicy:
    AGENT_PERMISSIONS = {
        "resume_agent": {"file_utility", "llm_brain", "rag_tool"},
        "job_match_agent": {"job_scraper", "llm_brain", "rag_tool"},
        "full_agent": {"*"}
    }

    @staticmethod
    def is_allowed(agent_name: str, tool_name: str) -> bool:
        allowed_tools = ToolPolicy.AGENT_PERMISSIONS.get(agent_name, set())
        if "*" in allowed_tools:
            return True
        return tool_name in allowed_tools

    @staticmethod
    def enforce(agent_name: str, tool_name: str):
        if not ToolPolicy.is_allowed(agent_name, tool_name):
            raise PermissionError(f"Agent '{agent_name}' is not authorized to use tool '{tool_name}'")
