from bookinfo import bookinfo
from search_apis import get_book_price_serpapi, get_book_price_scrape_do, get_book_price_valueserp

def searchbook(isbn: str, search_type: str = "serpapi"):
    """ISBNコードから本のタイトルを検索して、Google検索の結果を返す
    Args:
        isbn: ISBNコード
        search_type: 検索タイプ "serpapi" | "scrape_do" | "valueserp"
    Returns:
        list[dict]: 検索結果
    Raises:
        ValueError: 検索タイプが無効な場合
        TimeoutError: 本の情報取得がタイムアウトした場合
        LookupError: 本の情報が見つからない場合
    """

    title, author = bookinfo(isbn)

    if search_type == "serpapi":
        return get_book_price_serpapi(title)
    elif search_type == "scrape_do":
        return get_book_price_scrape_do(title)
    elif search_type == "valueserp":
        return get_book_price_valueserp(title)
    else:
        raise ValueError(f"Invalid search type: {search_type}")
