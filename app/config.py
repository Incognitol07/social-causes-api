# app/config.py

from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # Application settings
    APP_NAME: str = "Social Cause API"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")  # Default to 'development'
    DEBUG: bool = ENVIRONMENT == "development"

    DATABASE_URL: str =os.getenv("DATABASE_URL")

    # Other security settings
    ALLOWED_HOSTS: list = ["*"]
    CORS_ORIGINS: list = ["http://localhost:3000", "http://localhost:5173"]  # Add frontend URL if applicable

# Instantiate settings
settings = Settings()
