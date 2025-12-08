"""
Configuration module for Nutrition-Based Local Food Advisor App
"""

import os
from typing import Optional

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(override=True)


class AppConfig:
    """Application configuration settings"""
    
    # LLM Configuration
    DEFAULT_LLM_PROVIDER: str = os.getenv("DEFAULT_LLM_PROVIDER", "openai")  # Default LLM provider
    DEFAULT_LLM_API_KEY: Optional[str] = os.getenv("DEFAULT_LLM_API_KEY") or os.getenv("OPENAI_API_KEY")  # Default LLM API key
    DEFAULT_LLM_TEMPERATURE: float = float(os.getenv("DEFAULT_LLM_TEMPERATURE", "0.7"))  # Default LLM temperature
    DEFAULT_LLM_MODEL: str = os.getenv("DEFAULT_LLM_MODEL", "gpt-4o-mini")  # Default LLM model
    
    # Agent Configuration
    AGENT_NAME: str = "Nutrition Advisor"
    AGENT_DESCRIPTION: str = (
        "AI-powered nutrition advisor that recommends locally available, "
        "economical, and nutrient-rich foods"
    )
    
    # Data Paths
    DATA_DIR: str = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
    
    # Memory Configuration
    MEMORY_ENABLED: bool = True
    MEMORY_STORAGE_PATH: Optional[str] = os.path.join(DATA_DIR, "user_memory.json")
    
    # Local Store Search Configuration
    GOOGLE_API_KEY: Optional[str] = os.getenv("GOOGLE_API_KEY")
    GOOGLE_SEARCH_ENGINE_ID: Optional[str] = os.getenv("GOOGLE_SEARCH_ENGINE_ID")
    
    # ElevenLabs Configuration
    ELEVENLABS_API_KEY: Optional[str] = os.getenv("ELEVENLABS_API_KEY")
    ELEVENLABS_VOICE_ID: Optional[str] = os.getenv("ELEVENLABS_VOICE_ID")
    ELEVENLABS_OUTPUT_FORMAT: Optional[str] = os.getenv("ELEVENLABS_OUTPUT_FORMAT")
    ELEVENLABS_MODEL_ID: Optional[str] = os.getenv("ELEVENLABS_MODEL_ID")
    
    @classmethod
    def validate(cls) -> bool:
        """
        Validate that required configuration is present.
        
        Returns:
            bool: True if configuration is valid
        """
        # Validation: API keys are optional at startup
        # They will be required when specific features (LLM calls, Google search) are used
        return True
    
    @classmethod
    def get_summary(cls) -> str:
        """
        Get a summary of current configuration.
        
        Returns:
            str: Configuration summary
        """
        return f"""
Configuration Summary:
  - Agent Name: {cls.AGENT_NAME}
  - Default LLM Provider: {cls.DEFAULT_LLM_PROVIDER}
  - Default LLM Model: {cls.DEFAULT_LLM_MODEL}
  - Default LLM API Key: {'Set' if cls.DEFAULT_LLM_API_KEY else 'Not set'}
  - Data Directory: {cls.DATA_DIR}
  - Memory Enabled: {cls.MEMORY_ENABLED}
  - Google API Key: {'Set' if cls.GOOGLE_API_KEY else 'Not set'}
  - ElevenLabs API Key: {'Set' if cls.ELEVENLABS_API_KEY else 'Not set'}
  - ElevenLabs Voice ID: {'Set' if cls.ELEVENLABS_VOICE_ID else 'Not set'}
  - ElevenLabs Output Format: {'Set' if cls.ELEVENLABS_OUTPUT_FORMAT else 'Not set'}
  - ElevenLabs Model ID: {'Set' if cls.ELEVENLABS_MODEL_ID else 'Not set'}
"""

