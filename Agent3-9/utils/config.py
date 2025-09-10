import os
from dotenv import load_dotenv

load_dotenv()

# Paths
REFERENCE_DIR = os.getenv("REFERENCE_DIR", "./reference_pdfs")
CHROMA_DIR = os.getenv("CHROMA_DIR", "./chroma_db")
HANDOFF_DIR = os.getenv("HANDOFF_DIR", "./handoff")

# Create handoff dir if not exists
os.makedirs(HANDOFF_DIR, exist_ok=True)

# Embeddings
EMBED_MODEL = os.getenv("EMBED_MODEL", "sentence-transformers/all-MiniLM-L6-v2")

# LLM via OpenRouter (OpenAI-compatible)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "google/gemini-2.0-flash-001")


# Retrieval
TOP_K = int(os.getenv("TOP_K", "5"))

# Chunking
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1000"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "200"))