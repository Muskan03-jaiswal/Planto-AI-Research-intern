from typing import List
import google.generativeai as genai
from crew.config import GEMINI_API_KEY

# Simple helper for embeddings with Gemini
class GeminiEmbedder:
    def __init__(self, model: str = "text-embedding-004"):
        if not GEMINI_API_KEY:
            raise RuntimeError("Gemini API key missing")
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = model

    def embed(self, texts: List[str]) -> List[List[float]]:
        # Gemini batches up to 1000 tokens per text; chunk before calling if needed
        out = genai.embed_content(model=self.model, content=texts)
        vectors = out["embedding"] if isinstance(texts, str) else out["embeddings"]
        # Normalize output shape
        if isinstance(texts, str):
            return [vectors]
        return [e["values"] if isinstance(e, dict) else e for e in vectors]
