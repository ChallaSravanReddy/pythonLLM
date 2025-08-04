"""
Configuration module for LLM + Agentic Thinking Application
Handles API keys, LLM provider selection, and application settings
"""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for the application"""
    
    # API Keys - Load from environment variables
    
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    GEMINI_API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY")
    
    # LLM Settings
    DEFAULT_LLM_PROVIDER: str = "gemini"  # "openai" or "gemini"
    OPENAI_MODEL: str = "gpt-3.5-turbo"
    GEMINI_MODEL: str = "gemini-1.5-pro"
    
    # Application Settings
    MAX_TOKENS: int = 1000
    TEMPERATURE: float = 0.7
    LOG_LEVEL: str = "INFO"
    
    # Tool Settings
    CALCULATOR_ENABLED: bool = True
    TRANSLATOR_ENABLED: bool = True
    
    @classmethod
    def validate_config(cls) -> bool:
        """Validate that required configuration is present"""
        if cls.DEFAULT_LLM_PROVIDER == "openai" and not cls.OPENAI_API_KEY:
            print("⚠️  Warning: OPENAI_API_KEY not found in environment variables")
            print("   The application will use fallback mode for Level 1")
            return False
        elif cls.DEFAULT_LLM_PROVIDER == "gemini" and not cls.GEMINI_API_KEY:
            print("⚠️  Warning: GEMINI_API_KEY not found in environment variables")
            print("   The application will use fallback mode for Level 1")
            return False
        return True
    
    @classmethod
    def get_llm_config(cls) -> dict:
        """Get LLM configuration based on selected provider"""
        if cls.DEFAULT_LLM_PROVIDER == "openai":
            return {
                "provider": "openai",
                "api_key": cls.OPENAI_API_KEY,
                "model": cls.OPENAI_MODEL,
                "max_tokens": cls.MAX_TOKENS,
                "temperature": cls.TEMPERATURE
            }
        elif cls.DEFAULT_LLM_PROVIDER == "gemini":
            return {
                "provider": "gemini",
                "api_key": cls.GEMINI_API_KEY,
                "model": cls.GEMINI_MODEL,
                "max_tokens": cls.MAX_TOKENS,
                "temperature": cls.TEMPERATURE
            }
        else:
            return {
                "provider": "fallback",
                "api_key": None,
                "model": "local",
                "max_tokens": cls.MAX_TOKENS,
                "temperature": cls.TEMPERATURE
            } 