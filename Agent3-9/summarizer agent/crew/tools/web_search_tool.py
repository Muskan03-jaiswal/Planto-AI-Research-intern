from typing import List, Dict
from crew.config import SerpAPI, MAX_WEB_RESULTS
from crewai.tools import BaseTool
from serpapi import GoogleSearch
from typing import Dict, Any
import os

def serpapi_search(query: str, api_key: str, num: int = 5):
    search = GoogleSearch({
        "q": query,
        "api_key": api_key,
        "num": num
    })
    results = search.get_dict()
    return results.get("organic_results", [])

# ✅ CrewAI-compatible wrapper
class WebSearchTool(BaseTool):
    name: str = "web_search"
    description: str = "Search the web using SerpAPI. Input: {query:str, num?:int}"

    def _run(self, query: str, num: int = 5):
        api_key = os.getenv("SERPAPI_API_KEY")
        if not api_key:
            raise RuntimeError("SERPAPI_API_KEY not set in .env")

        search = GoogleSearch({
            "q": query,
            "api_key": api_key,
            "num": num
        })
        results = search.get_dict()
        return results.get("organic_results", [])


