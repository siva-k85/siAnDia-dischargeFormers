import os
import json
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Project paths
PROJECT_ROOT = Path(__file__).parent
DATA_DIR = PROJECT_ROOT / "data"
LOGS_DIR = PROJECT_ROOT / "logs"

# Ensure directories exist
LOGS_DIR.mkdir(exist_ok=True)

# LLM settings
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4")
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.2"))
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "4000"))

# API keys - set in .env file or use credentials.json as fallback
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# Try to load from credentials.json if not found in environment
if not OPENAI_API_KEY:
    try:
        with open("credentials.json") as f:
            credentials = json.load(f)
            OPENAI_API_KEY = credentials.get("openai_api_key", "")
    except (FileNotFoundError, json.JSONDecodeError):
        pass

if not OPENAI_API_KEY:
    print("Warning: No API key found. Set OPENAI_API_KEY in .env or credentials.json")

# UI settings
UI_TITLE = "Medical Discharge Summary Generator"
UI_DESCRIPTION = "Generate professional discharge summaries from patient data"

# Logging configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
LOG_RETENTION = "7 days"
