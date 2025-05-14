"""
Initialize the res module.
This module is responsible for loading environment variables
"""
from pathlib import Path
from dotenv import load_dotenv

# Load .env from root/ (one level above resources/)
load_dotenv(Path(__file__).parent.parent / ".env")
