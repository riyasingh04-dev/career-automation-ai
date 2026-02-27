from typing import Dict
from backend.app.observability.logger import app_logger

class PromptManager:
    # In-memory defaults, usually backed by the PromptVersion DB table
    DEFAULT_PROMPTS = {
        "tailor_resume": {
            "version": "1.0.0",
            "template": "Modify this resume to match the following job description while keeping it ATS friendly:\n\nResume: {resume}\n\nJD: {jd}"
        },
        "cover_letter": {
            "version": "1.1.0",
            "template": "Write a compelling cover letter based on this resume and job description:\n\nResume: {resume}\n\nJD: {jd}"
        }
    }

    @staticmethod
    def get_prompt(name: str, version: str = None) -> str:
        # Fallback to defaults or fetch from DB by name/version
        prompt_data = PromptManager.DEFAULT_PROMPTS.get(name)
        if not prompt_data:
            app_logger.error(f"Prompt '{name}' not found")
            return ""
        
        app_logger.info(f"Using prompt '{name}' version {prompt_data['version']}")
        return prompt_data['template']

    @staticmethod
    def format_prompt(name: str, **kwargs) -> str:
        template = PromptManager.get_prompt(name)
        return template.format(**kwargs)
