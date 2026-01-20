"""
Application configuration module.
Handles environment variables and application settings.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings:
    """Application settings and configuration."""
    
    # API Settings
    API_TITLE = "Wikipedia Country Outline API"
    API_VERSION = "1.0.0"
    API_DESCRIPTION = """
    Extract hierarchical outlines from Wikipedia country pages.
    
    This API fetches Wikipedia pages for countries and extracts all headings
    (H1-H6) to create a structured Markdown outline.
    """
    
    # Server Settings
    HOST = os.getenv("API_HOST", "0.0.0.0")
    PORT = int(os.getenv("API_PORT", "8000"))
    
    # Cache Settings
    CACHE_DIR = Path(os.getenv("CACHE_DIR", "./cache"))
    
    # HTTP Settings
    REQUEST_TIMEOUT = 60
    USER_AGENT = "WikipediaOutlineBot/1.0 (Educational Project)"
    
    def __init__(self):
        """Initialize settings and ensure cache directory exists."""
        self.CACHE_DIR.mkdir(parents=True, exist_ok=True)

# Global settings instance
settings = Settings()