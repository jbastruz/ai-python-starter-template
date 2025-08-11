"""Configuration module using Pydantic BaseSettings.

This module provides application configuration management with environment
variable support and validation using Pydantic BaseSettings.
"""

from functools import lru_cache
from typing import Optional

from pydantic import BaseSettings


class AppSettings(BaseSettings):
    """Application settings with environment variable support.
    
    This class defines all configuration options for the application.
    Values can be set via environment variables or a .env file.
    
    Attributes:
        env: Environment name (default: 'dev')
        api_base_url: Base URL for API calls (default: 'https://httpbin.org')
        api_key: Optional API key for authentication
        log_level: Logging level (default: 'INFO')
    """
    
    env: str = "dev"
    api_base_url: str = "https://httpbin.org"
    api_key: Optional[str] = None
    log_level: str = "INFO"
    
    class Config:
        """Pydantic configuration.
        
        Enables automatic loading from .env files and makes
        field names case-insensitive for environment variables.
        """
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


@lru_cache()
def get_settings() -> AppSettings:
    """Get cached application settings.
    
    This function returns a cached instance of AppSettings to ensure
    that settings are loaded only once during the application lifetime.
    
    Returns:
        AppSettings: Cached application settings instance
        
    Example:
        >>> settings = get_settings()
        >>> print(settings.env)
        'dev'
        >>> print(settings.api_base_url)
        'https://httpbin.org'
    """
    return AppSettings()
