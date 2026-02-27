from mcp.base import MCPTool
from playwright.sync_api import sync_playwright
from typing import Any
import asyncio

class BrowserTool(MCPTool):
    @property
    def name(self) -> str:
        return "job_scraper"

    @property
    def description(self) -> str:
        return "Scrapes job descriptions and details from LinkedIn, Indeed, etc."

    def _execute_sync(self, url: str) -> Any:
        # Running Playwright in synchronous mode
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url)
            
            # Extract clean text instead of raw HTML to help the AI
            content = page.inner_text("body")
            title = page.title()
            
            browser.close()
            return {
                "url": url,
                "title": title,
                "content": content[:5000] # Returning more text for better analysis
            }

    async def execute(self, url: str) -> Any:
        # Offload synchronous Playwright call to a separate thread
        # this solves the NotImplementedError on Windows with SelectorEventLoop
        return await asyncio.to_thread(self._execute_sync, url)

