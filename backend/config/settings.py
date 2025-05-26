"""
Production settings for BrightData MCP × Google ADK Platform
"""
import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

class Settings:
    """Application settings and configuration"""
    
    # API Configuration
    GEMINI_API_KEY: Optional[str] = os.getenv('GEMINI_API_KEY')
    BRIGHTDATA_API_TOKEN: Optional[str] = os.getenv('BRIGHTDATA_API_TOKEN')
    BROWSER_AUTH: Optional[str] = os.getenv('BROWSER_AUTH')
    API_TOKEN: Optional[str] = os.getenv('API_TOKEN')
    
    # Server Configuration
    HOST: str = os.getenv('HOST', '0.0.0.0')
    PORT: int = int(os.getenv('PORT', '8001'))
    DEBUG: bool = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # Application Configuration
    APP_NAME: str = "BrightData MCP × Google ADK Platform"
    VERSION: str = "2.0.0"
    DESCRIPTION: str = "Professional Web Scraping & Data Extraction Platform"
    
    # Timeout Configuration
    REQUEST_TIMEOUT: int = int(os.getenv('REQUEST_TIMEOUT', '90'))
    QUICK_TIMEOUT: int = int(os.getenv('QUICK_TIMEOUT', '30'))
    
    # CORS Configuration
    ALLOWED_ORIGINS: list = ["*"]  # Configure for production
    
    # Model Configuration
    MODEL_NAME: str = "gemini-2.0-flash"
    AGENT_NAME: str = "brightdata_mcp_professional_agent"
    
    @property
    def is_configured(self) -> bool:
        """Check if all required environment variables are set"""
        return all([
            self.GEMINI_API_KEY,
            self.BRIGHTDATA_API_TOKEN,
            self.BROWSER_AUTH
        ])

# Global settings instance
settings = Settings() 