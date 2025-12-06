
import os
import requests
from spoon_ai.tools.base import BaseTool

class WebSearchTool(BaseTool):
    name: str = "web_search"
    description: str = "Search the web for information using Google. Use this to find nutritional information for specific branded foods (e.g., 'Kellogg's Crunchy Nut nutrition facts') or restaurants."
    
    parameters: dict = {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "The search query (e.g., 'Kellogg's Crunchy Nut nutrition facts')"
            }
        },
        "required": ["query"]
    }

    async def execute(self, query: str) -> str:
        api_key = os.getenv("GOOGLE_API_KEY")
        cse_id = os.getenv("GOOGLE_SEARCH_ENGINE_ID")
        
        if not api_key or not cse_id:
            return "Error: Google Search API key or Engine ID not configured."

        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            "key": api_key,
            "cx": cse_id,
            "q": query,
            "num": 3
        }

        try:
            # Running synchronous requests in async method is bad practice but simplistic here.
            # In production, use aiohttp. For now, it's fine for a demo.
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            results = []
            if "items" in data:
                for item in data["items"]:
                    title = item.get("title", "No title")
                    snippet = item.get("snippet", "No snippet")
                    link = item.get("link", "No link")
                    results.append(f"Title: {title}\nSummary: {snippet}\nLink: {link}\n")
            
            if not results:
                return "No results found."
                
            return "\n---\n".join(results)
            
        except Exception as e:
            return f"Error executing search: {str(e)}"
