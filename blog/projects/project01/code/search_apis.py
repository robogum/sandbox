from pathlib import Path
import os

import requests
from dotenv import load_dotenv

# このファイルと同じ code/ にある .env を読む
_CODE_DIR = Path(__file__).resolve().parent
load_dotenv(_CODE_DIR / ".env")
load_dotenv(Path.cwd() / ".env")


def get_book_price_scrape_do(book_title):
    token = os.getenv("SCRAPE_DO_TOKEN")
    if not token:
        print('".env" を設定してください。".env.example"を参照')
        return

    params = {
        "token": token,
        "q": f"{book_title} 中古 価格",
        "gl": "jp",
        "hl": "ja",
        "google_domain": "google.co.jp",
    }

    url = "https://api.scrape.do/plugin/google/search"
    response = requests.get(url, params=params)
    data = response.json()

    organic_results = data.get("organic_results", [])
    if not organic_results:
        print("No results found.")
        return []

    for result in organic_results:
        title = result.get("title", "")
        link = result.get("link", "")
        snippet = result.get("snippet", "")

        print(f"Title: {title}")
        print(f"Link: {link}")
        print(f"Snippet: {snippet}\n")

    return organic_results


def get_book_price_serpapi(book_title):
    api_key = os.getenv("SERPAPI_API_KEY")
    if not api_key:
        print('".env" を設定してください。".env.example"を参照')
        return

    params = {
        "api_key": api_key,
        "engine": "google",
        "q": f"{book_title} 中古 価格",
        "gl": "jp",
        "lr": "lang_ja",
    }

    url = "https://serpapi.com/search.json"
    response = requests.get(url, params=params)
    data = response.json()

    organic_results = data.get("organic_results", [])
    if not organic_results:
        print("No results found.")
        return []

    for result in organic_results:
        title = result.get("title", "")
        link = result.get("link", "")
        snippet = result.get("snippet", "")

        print(f"Title: {title}")
        print(f"Link: {link}")
        print(f"Snippet: {snippet}\n")

    return organic_results


def get_book_price_valueserp(book_title):
    api_key = os.getenv("VALUESERP_API_KEY")
    if not api_key:
        print('".env" を設定してください。".env.example"を参照')
        return

    params = {
        "api_key": api_key,
        "q": f"{book_title} 中古 価格",
        "gl": "jp",
        "hl": "ja",
        "google_domain": "google.co.jp",
    }

    url = "https://api.valueserp.com/search"
    response = requests.get(url, params=params)
    data = response.json()

    organic_results = data.get("organic_results", [])
    if not organic_results:
        print("No results found.")
        return []

    for result in organic_results:
        title = result.get("title", "")
        link = result.get("link", "")
        snippet = result.get("snippet", "")

        print(f"Title: {title}")
        print(f"Link: {link}")
        print(f"Snippet: {snippet}\n")

    return organic_results
