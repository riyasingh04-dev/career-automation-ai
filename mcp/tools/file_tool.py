from mcp.base import MCPTool
import os
from typing import Any
from pypdf import PdfReader, PdfWriter

class FileTool(MCPTool):
    @property
    def name(self) -> str:
        return "file_utility"

    @property
    def description(self) -> str:
        return "Reads and writes files, specifically PDF resumes."

    async def execute(self, action: str, file_path: str, content: Any = None) -> Any:
        if action == "read_pdf":
            return self._read_pdf(file_path)
        elif action == "write_txt":
            return self._write_txt(file_path, content)
        elif action == "save_upload":
            return self._save_upload(file_path, content)
        else:
            return {"error": f"Action {action} not supported"}

    def _save_upload(self, path: str, content: bytes):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wb") as f:
            f.write(content)
        return f"File saved to {path}"

    def _read_pdf(self, path: str) -> str:
        abs_path = os.path.abspath(path)
        if not os.path.exists(abs_path):
            return f"File not found at {abs_path}"
        reader = PdfReader(abs_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text

    def _write_txt(self, path: str, content: str):
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Successfully wrote to {path}"
