import requests
from bs4 import BeautifulSoup
from googlesearch import search

def get_source_text(query: str) -> str:
    # Search google
    site = next(search(query))
    # Scrape the resulting website from google
    request = requests.get(site)
    # Parse the scraped content
    content = BeautifulSoup(request.content, features="html.parser")
    content = " ".join([p.get_text() for p in content.find_all("p")])
    return content

if __name__ == "__main__":
    content = get_source_text("Chocolate lowers the risk of cancer")
    print(content)