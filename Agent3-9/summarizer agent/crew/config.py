import os
from dotenv import load_dotenv

load_dotenv()

CREW_VERBOSE = os.getenv("CREWAI_VERBOSE", "false").lower() == "true"

# LiteLLM model string, e.g., "gemini/gemini-1.5-pro"
MODEL = os.getenv("MODEL", "gemini/gemini-2.0-flash-001")

# Web search
SerpAPI = os.getenv("SerpAPI", "ccec3218b6dcce699760527b068612e888b2cc91")

# RAG / Embeddings (Gemini)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Other knobs
MAX_WEB_RESULTS = int(os.getenv("MAX_WEB_RESULTS", "8"))

# Output dir
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)
