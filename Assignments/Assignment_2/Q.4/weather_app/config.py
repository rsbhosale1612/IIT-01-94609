from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env")

API_KEY = os.getenv("OWM_API_KEY")
UNITS = os.getenv("UNITS", "metric")

if not API_KEY:
    raise RuntimeError("Please set OWM_API_KEY in .env")
