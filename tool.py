from langchain.tools import tool
from tavily import TavilyClient
from bs4 import BeautifulSoup
import os
import requests
from dotenv import load_dotenv
load_dotenv()

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def web_search(query: str) -> str:
    """Search the web for recent and reliable information on a topic . Returns Titles , URLs and snippets."""
    result = tavily.search(query=query, max_results=5)

    out = []

    for r in result["results"]:
        out.append(
            f"Title: {r['title']}\nURL: {r['url']}\nSnippet: {r['content'][:300]}\n"
        )

    return "\n\n----\n\n".join(out)


soups = []
@tool
def web_scrapping(url: str) -> str:
    """"This tool takes URLs and do web scrapping and extract all the text from it"""
    try:
        response = requests.get(url, timeout=15, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(response.text, "html.parser")
        for element in soup(["script", "style", "nav", "footer"]):
            element.decompose()
        return soup.get_text(separator=" ", strip=True)[:1000]         
    except Exception as e:
        return f"Could not scrap the {str(e)}"