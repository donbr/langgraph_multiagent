"""Search tools for the multi-agent system."""

try:
    from langchain_tavily import TavilySearchResults
except ImportError:
    from langchain_community.tools.tavily_search import TavilySearchResults


def get_tavily_tool(max_results: int = 5) -> TavilySearchResults:
    """Get a configured Tavily search tool."""
    return TavilySearchResults(max_results=max_results)