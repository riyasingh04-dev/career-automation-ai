import asyncio
from mcp.tools.browser_tool import BrowserTool

async def main():
    scraper = BrowserTool()
    result = await scraper.execute("https://www.linkedin.com/jobs/search/?keywords=software%20engineer")
    print(f"Scraped Title: {result['title']}")

if __name__ == "__main__":
    asyncio.run(main())
