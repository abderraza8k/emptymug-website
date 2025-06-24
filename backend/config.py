# Configuration settings for the application
from pydantic import BaseSettings, Field
from typing import Literal
import os

class Settings(BaseSettings):
    # Database configuration
    database_type: Literal["memory", "postgres", "dynamodb"] = Field(
        default="memory", 
        description="Database type to use"
    )
    
    # PostgreSQL settings
    postgres_host: str = Field(default="localhost", description="PostgreSQL host")
    postgres_port: int = Field(default=5432, description="PostgreSQL port")
    postgres_user: str = Field(default="postgres", description="PostgreSQL username")
    postgres_password: str = Field(default="password", description="PostgreSQL password")
    postgres_db: str = Field(default="emptymug", description="PostgreSQL database name")
    
    # DynamoDB settings
    dynamodb_region: str = Field(default="us-east-1", description="DynamoDB region")
    dynamodb_table_name: str = Field(default="emptymug_contacts", description="DynamoDB table name")
    aws_access_key_id: str = Field(default="", description="AWS Access Key ID")
    aws_secret_access_key: str = Field(default="", description="AWS Secret Access Key")
    
    # LLM settings
    ollama_host: str = Field(default="http://localhost:11434", description="Ollama host URL")
    ollama_model: str = Field(default="llama2", description="Ollama model name")
    
    # Application settings
    cors_origins: str = Field(default="http://localhost:3000", description="CORS origins")
    log_level: str = Field(default="INFO", description="Logging level")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Global settings instance
settings = Settings()
