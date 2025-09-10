# crew/tools/rag_tool.py
import os
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
import google.generativeai as genai

try:
    import faiss
    import numpy as np
except ImportError:
    faiss, np = None, None

from crewai.tools import BaseTool


class RAGTool(BaseTool):
    """
    Retrieval-Augmented Generation tool using Gemini embeddings.
    Stores and retrieves documents locally with FAISS (if available) or JSON fallback.
    """

    # Required by CrewAI / Pydantic
    name: str = "rag_search"
    description: str = "Retrieve top-k relevant documents for a query from a local FAISS/JSON vector store."

    # Custom internal fields must be declared here
    store_path: Optional[Path] = None
    use_faiss: bool = False
    embed_model: str = "models/embedding-001"

    # FAISS-related
    index_file: Optional[Path] = None
    meta_file: Optional[Path] = None
    metadata: Optional[list] = None
    index: Any = None

    # JSON fallback
    json_file: Optional[Path] = None

    def __init__(self, store_path: str = ".memory/vs", **kwargs):
        super().__init__(**kwargs)  # important for BaseTool init

        self.store_path = Path(store_path)
        self.store_path.mkdir(parents=True, exist_ok=True)

        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError("GEMINI_API_KEY is missing. Please set it in .env")

        genai.configure(api_key=api_key)

        # Use FAISS if available
        self.use_faiss = faiss is not None
        if self.use_faiss:
            self.index_file = self.store_path / "faiss.index"
            self.meta_file = self.store_path / "metadata.json"
            self._load_index()
        else:
            self.json_file = self.store_path / "store.json"
            if not self.json_file.exists():
                with open(self.json_file, "w", encoding="utf-8") as f:
                    json.dump([], f)

    # -----------------------------
    # Embedding
    # -----------------------------
    def _embed(self, text: str) -> List[float]:
        """Generate embedding vector for text using Gemini."""
        resp = genai.embed_content(model=self.embed_model, content=text)
        return resp["embedding"]

    # -----------------------------
    # FAISS handling
    # -----------------------------
    def _load_index(self):
        if self.index_file.exists() and self.meta_file.exists():
            self.index = faiss.read_index(str(self.index_file))
            with open(self.meta_file, "r", encoding="utf-8") as f:
                self.metadata = json.load(f)
        else:
            self.index = faiss.IndexFlatL2(768)  # Gemini embeddings are 768-d
            self.metadata = []
            faiss.write_index(self.index, str(self.index_file))
            with open(self.meta_file, "w", encoding="utf-8") as f:
                json.dump([], f)

    def _save_index(self):
        faiss.write_index(self.index, str(self.index_file))
        with open(self.meta_file, "w", encoding="utf-8") as f:
            json.dump(self.metadata, f, ensure_ascii=False, indent=2)

    # -----------------------------
    # CrewAI entrypoint
    # -----------------------------
    def _run(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """CrewAI will call this when the agent uses the tool."""
        return self.search(query, k)

    # -----------------------------
    # Public API (still usable directly)
    # -----------------------------
    def search(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """Retrieve top-k relevant documents for a query."""
        qvec = self._embed(query)

        if self.use_faiss:
            if len(self.metadata) == 0:
                return []
            D, I = self.index.search([qvec], k=min(k, len(self.metadata)))
            return [self.metadata[i] for i in I[0]]
        else:
            with open(self.json_file, "r", encoding="utf-8") as f:
                items = json.load(f)

            # cosine similarity
            from numpy import dot
            from numpy.linalg import norm
            scored = []
            for item in items:
                vec = item["embedding"]
                sim = dot(vec, qvec) / (norm(vec) * norm(qvec))
                scored.append((sim, item))
            scored.sort(key=lambda x: x[0], reverse=True)
            return [item for _, item in scored[:k]]

    def add_documents(self, docs: List[Dict[str, str]]):
        """
        Add new documents into the store.
        Docs should be a list of dicts with keys: {title, content, url?}.
        """
        for doc in docs:
            emb = self._embed(doc["content"])
            record = {**doc, "embedding": emb}

            if self.use_faiss:
                vec = np.array([emb], dtype="float32")
                self.index.add(vec)
                self.metadata.append(doc)
            else:
                with open(self.json_file, "r+", encoding="utf-8") as f:
                    items = json.load(f)
                    items.append(record)
                    f.seek(0)
                    json.dump(items, f, ensure_ascii=False, indent=2)

        if self.use_faiss:
            self._save_index()
