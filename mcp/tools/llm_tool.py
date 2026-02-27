from mcp.base import MCPTool
from backend.app.core.config import settings
from openai import AsyncOpenAI
from typing import Any

class LLMTool(MCPTool):
    def __init__(self):
        api_key = settings.OPENAI_API_KEY or settings.GROQ_API_KEY
        base_url = None
        
        # If using Groq key, we must specify the Groq base URL
        if settings.GROQ_API_KEY and api_key == settings.GROQ_API_KEY:
            base_url = "https://api.groq.com/openai/v1"
            
        self.client = AsyncOpenAI(api_key=api_key, base_url=base_url)

    @property
    def name(self) -> str:
        return "llm_brain"

    @property
    def description(self) -> str:
        return "Brain for resume tailoring, cover letter generation, and skill analysis."

    async def execute(self, prompt_type: str, context: dict) -> Any:
        if prompt_type == "tailor_resume":
            return await self._tailor_resume(context)
        elif prompt_type == "generate_cover_letter":
            return await self._generate_cover_letter(context)
        else:
            return {"error": "Invalid prompt type"}

    async def _tailor_resume(self, context: dict) -> dict:
        resume = context.get("resume")
        jd = context.get("job_description")
        prompt = (
            "You are an elite Recruitment Architect and ATS Optimization Specialist. "
            "Analyze the following resume against the job description with extreme scrutiny. "
            "1. Generate a tailored version of the resume that strategically highlights relevant skills and experiences while maintaining perfect honesty. "
            "2. Calculate a high-precision ATS compatibility score (0-100). This score must be based on a granular analysis of: "
            "   - Semantic match of technical skills (not just keywords, but depth of experience). "
            "   - Project relevance to the JD requirements. "
            "   - Formatting and section optimization.\n\n"
            "CRITICAL: Do NOT give generic scores (like 85 or 90). The score should be highly specific to this exact match (e.g., 73, 94, 68). "
            "If the resume is a poor match, give a low score. If it's excellent, give a high score.\n\n"
            "Respond ONLY with a JSON object in this format:\n"
            "{\n"
            "  \"tailored_resume\": \"string...\",\n"
            "  \"ats_score\": integer\n"
            "}\n\n"
            f"Resume: {resume}\n\n"
            f"JD: {jd}"
        )
        
        response = await self.client.chat.completions.create(
            model=settings.DEFAULT_MODEL,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        import json
        return json.loads(response.choices[0].message.content)

    async def _generate_cover_letter(self, context: dict) -> str:
        resume = context.get("resume")
        jd = context.get("job_description")
        prompt = f"Write a compelling cover letter based on this resume and job description:\n\nResume: {resume}\n\nJD: {jd}"
        
        response = await self.client.chat.completions.create(
            model=settings.DEFAULT_MODEL,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
