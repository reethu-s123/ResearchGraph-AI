"""
Configuration Management
"""

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration"""
    
    EUROPE_PMC_API_KEY = os.getenv("EUROPE_PMC_API_KEY", "")
    EUROPE_PMC_BASE_URL = os.getenv("EUROPE_PMC_BASE_URL", "https://www.ebi.ac.uk/europepmc/webservices/rest")
    MAX_PAPERS_PER_SEARCH = int(os.getenv("MAX_PAPERS_PER_SEARCH", 50))
    SIMILARITY_THRESHOLD = float(os.getenv("SIMILARITY_THRESHOLD", 0.7))
    
    CACHE_ENABLED = os.getenv("CACHE_ENABLED", "true").lower() == "true"
    CACHE_TTL = int(os.getenv("CACHE_TTL", 3600))
    
    SUMMARIZATION_MODEL = os.getenv("SUMMARIZATION_MODEL", "facebook/bart-large-cnn")
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
    SPACY_MODEL = os.getenv("SPACY_MODEL", "en_core_web_sm")
    
    NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
    NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")
    
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = os.getenv("LOG_FILE", "logs/app.log")
    
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"
    ENVIRONMENT = os.getenv("ENVIRONMENT", "production")

os.makedirs("logs", exist_ok=True)
