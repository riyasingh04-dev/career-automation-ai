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
            "You are a World-Class ATS (Applicant Tracking System) Optimization Specialist and Recruitment Strategist. "
            "Your mission is to rewrite the provided resume to ensure it achieves an **ATS Match Score of 90 or higher** against the Job Description (JD). "
            "\n\n**REWRITING GUIDELINES:**\n"
            "1. **Semantic Mirroring**: Identify core technical skills, methodologies, and soft skills in the JD. Incorporate these naturally into the resume's 'Professional Summary', 'Experience', and 'Skills' sections. "
            "2. **Metric-Driven Results**: Transform bullet points to follow the 'Action Verb + Task + Result' formula. Ensure results are quantified (e.g., 'reduced latency by 30%', 'managed $1M budget'). "
            "3. **Keyword Density**: Ensure high-priority keywords from the JD are present in correct contexts, but avoid keyword stuffing. "
            "4. **Formatting for Parsers**: Use standard headers (EXPERIENCE, EDUCATION, SKILLS) that ATS software recognizes instantly. "
            "5. **Honesty Clause**: While optimizing for 90+ score, maintain the core integrity of the user's background. Shift emphasis rather than inventing facts. "
            "\n\n**SCORING CRITERIA:**\n"
            "Calculate a high-precision ATS compatibility score (0-100). The score must reflect the success of your optimization. "
            "A score above 90 is EXPECTED if you have performed the optimization correctly. "
            "\n\nRespond ONLY with a JSON object in this format:\n"
            "{\n"
            "  \"tailored_resume\": \"string (The fully optimized, high-score version)...\",\n"
            "  \"ats_score\": integer (TARGET: 90-100)\n"
            "}\n\n"
            f"ORIGINAL RESUME:\n{resume}\n\n"
            f"TARGET JOB DESCRIPTION:\n{jd}"
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
