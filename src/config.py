import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Enterprise Context Engineering Engine"
    ENVIRONMENT: str = os.getenv("APP_ENV", "development")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Token & Context Window Defaults
    DEFAULT_MAX_TOKEN_BUDGET: int = 4096
    SYSTEM_PROMPT_TOKEN_BUDGET: int = 800
    CONVERSATION_HISTORY_TOKEN_BUDGET: int = 800
    RAG_CONTEXT_TOKEN_BUDGET: int = 2000
    
    # Security & PII Redaction
    ENABLE_PII_REDACTION: bool = True
    ENFORCE_RBAC: bool = True
    
    class Config:
        case_sensitive = True


settings = Settings()
