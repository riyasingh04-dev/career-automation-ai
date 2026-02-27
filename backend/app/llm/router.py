from typing import Optional, List
from backend.app.core.config import settings
from openai import AsyncOpenAI

class LLMProvider:
    def __init__(self, api_key: str, provider_name: str, base_url: Optional[str] = None):
        self.client = AsyncOpenAI(api_key=api_key, base_url=base_url)
        self.name = provider_name

    async def generate(self, prompt: str, model: str) -> str:
        response = await self.client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content

class LLMRouter:
    def __init__(self):
        self.providers = []
        if settings.OPENAI_API_KEY:
            self.providers.append(LLMProvider(settings.OPENAI_API_KEY, "openai"))
        if settings.GROQ_API_KEY:
            self.providers.append(LLMProvider(
                settings.GROQ_API_KEY, 
                "groq", 
                base_url="https://api.groq.com/openai/v1"
            ))

    async def completion(self, prompt: str, preferred_model: Optional[str] = None) -> str:
        # Simple fallback logic: try primary, then secondary
        for provider in self.providers:
            try:
                model = preferred_model or settings.DEFAULT_MODEL
                return await provider.generate(prompt, model)
            except Exception as e:
                print(f"Provider {provider.name} failed: {e}")
                continue
        raise Exception("All LLM providers failed")

llm_router = LLMRouter()
