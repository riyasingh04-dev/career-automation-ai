from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # App Settings
    APP_NAME: str = "Job Hunter AI"
    DEBUG: bool = True
    
    # LLM Settings
    OPENAI_API_KEY: Optional[str] = None
    GROQ_API_KEY: Optional[str] = None
    DEFAULT_MODEL: str = "llama-3.3-70b-versatile"
    
    # Database Settings
    DATABASE_URL: str = "postgresql://user:pass@localhost:5432/jobhunter"
    MONGODB_URL: str = "mongodb://localhost:27017"
    
    # Workspace Paths
    WORKSPACE_ROOT: str = "d:/Job Hunter"
    CHROMA_PATH: str = "./rag/data/chroma"
    
    class Config:
        env_file = ".env"

settings = Settings()
