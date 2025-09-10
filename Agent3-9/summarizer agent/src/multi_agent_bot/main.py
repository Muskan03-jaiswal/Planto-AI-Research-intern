# crew.py
from crewai import Crew
from duckduckgo_search import DDGS

# Custom DuckDuckGo search tool
class WebSearchTool:
    name = "web_search"
    description = "Search the web using DuckDuckGo and return a list of {title, url, content}."

    def run(self, query: str, max_results: int = 8):
        results = []
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=max_results):
                results.append({
                    "title": r.get("title"),
                    "url": r.get("href"),
                    "content": r.get("body")
                })
        return results

def load_crew():
    return Crew.from_yaml("crew.yaml", tools=[WebSearchTool()])
