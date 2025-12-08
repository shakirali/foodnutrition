"""Tavily web search tool using the Python SDK."""
from typing import Optional
from spoon_ai.tools.base import BaseTool
from pydantic import PrivateAttr
from tavily import TavilyClient
from config import AppConfig


class TavilySearchTool(BaseTool):
    """Tool for searching the web using Tavily API."""
    
    name: str = "tavily_search"
    description: str = (
        "Search the internet for current nutrition information, food data, recipes, or research. "
        "Use this tool when: (1) Food is not found in the NutritionLookupTool database and you need "
        "to search the web for nutritional information, (2) User asks about specific brands, products, "
        "or restaurant items not in the database, (3) User asks about current nutrition trends, recent "
        "research, or up-to-date information, (4) You need to verify or supplement information from "
        "the database with current web sources. Always try NutritionLookupTool first, then use this tool "
        "as a fallback. When calling this tool, ALWAYS provide a clear, specific search query. "
        "Examples: 'nutritional value of McDonald's Big Mac', 'latest research on vitamin D', "
        "'nutrition facts for Trader Joe's frozen meals', 'current recommendations for omega-3 intake'."
    )
    parameters: dict = {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "The search query to find information on the web (e.g., 'nutritional value of apple', 'latest research on vitamin D', 'McDonald's Big Mac nutrition facts')"
            },
            "max_results": {
                "type": "integer",
                "description": "Maximum number of search results to return (default: 5, max: 10)",
                "default": 5,
                "minimum": 1,
                "maximum": 10
            }
        },
        "required": ["query"]
    }
    
    # Use PrivateAttr for internal implementation details
    _client: Optional[TavilyClient] = PrivateAttr(default=None)
    
    def __init__(self, api_key: Optional[str] = None, **kwargs):
        super().__init__(**kwargs)
        api_key = api_key or AppConfig.TAVILY_API_KEY
        if not api_key:
            raise ValueError("TAVILY_API_KEY is required. Set it in your .env file or pass it as api_key parameter.")
        self._client = TavilyClient(api_key=api_key)
    
    @property
    def client(self) -> TavilyClient:
        """Get the Tavily client instance."""
        if self._client is None:
            api_key = AppConfig.TAVILY_API_KEY
            if not api_key:
                raise ValueError("TAVILY_API_KEY is required. Set it in your .env file.")
            self._client = TavilyClient(api_key=api_key)
        return self._client
    
    async def execute(self, query: str, max_results: int = 5) -> str:
        """Execute the web search using Tavily."""
        try:
            # Validate inputs
            if not query or not query.strip():
                return "Error: Query cannot be empty"
            
            max_results = min(max(1, max_results), 10)
            
            # Perform the search
            response = self.client.search(
                query=query.strip(),
                max_results=max_results
            )
            
            # Format the response
            results = response.get('results', [])
            if not results:
                return f"No results found for query: '{query}'. Try rephrasing your search."
            
            # Build formatted response
            response_parts = [f"Found {len(results)} result(s) for '{query}':\n"]
            
            for i, result in enumerate(results, 1):
                title = result.get('title', 'No title')
                url = result.get('url', '')
                content = result.get('content', '')
                
                response_parts.append(f"\n--- Result {i} ---")
                response_parts.append(f"Title: {title}")
                response_parts.append(f"URL: {url}")
                if content:
                    # Truncate content if too long
                    content_preview = content[:500] + "..." if len(content) > 500 else content
                    response_parts.append(f"Content: {content_preview}")
            
            formatted_response = "\n".join(response_parts)
            return formatted_response
            
        except Exception as e:
            return f"Error: Tavily search failed: {str(e)}"
