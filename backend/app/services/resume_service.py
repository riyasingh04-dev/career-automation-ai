from backend.app.db.models import Resume, JobMatch
from backend.app.llm.router import llm_router

class ResumeService:
    @staticmethod
    async def analyze_and_tailor(resume_content: str, job_description: str):
        prompt = f"Tailor this resume for the following job description:\n\nResume: {resume_content}\n\nJD: {job_description}"
        tailored_content = await llm_router.completion(prompt)
        return tailored_content

    @staticmethod
    def calculate_ats_score(resume_content: str, job_description: str) -> int:
        # Placeholder for complex ATS scoring logic
        return 75
