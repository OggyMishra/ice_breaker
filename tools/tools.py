from langchain_community.tools.tavily_search import TavilySearchResults


def get_profile_url_tavily(search_query: str):
    """Searches for linkedin or twitter profile page"""
    search = TavilySearchResults()
    res = search.run(f"{search_query}")
    return res
