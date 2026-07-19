import json
import socket
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET


def _is_timeout_error(exc: BaseException) -> bool:
    if isinstance(exc, (TimeoutError, socket.timeout)):
        return True
    if isinstance(exc, urllib.error.URLError):
        return isinstance(exc.reason, (TimeoutError, socket.timeout))
    return False


def fetch_xml(url: str, timeout: int = 10) -> str | None:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "book-inventory/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as res:
            return res.read().decode("utf-8")
    except Exception as e:
        if _is_timeout_error(e):
            raise TimeoutError(f"Request timed out: {url}") from e
        return None


def fetch_json(url: str, timeout: int = 10) -> dict | list | None:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "book-inventory/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as res:
            return json.loads(res.read().decode("utf-8"))
    except Exception as e:
        if _is_timeout_error(e):
            raise TimeoutError(f"Request timed out: {url}") from e
        return None


def bookinfo_ndl(isbn: str, timeout: int = 10) -> tuple[str, str] | None:
    """国立国会図書館 から (タイトル, 著者) を取得"""
    xml_str = fetch_xml(
        f"https://iss.ndl.go.jp/api/opensearch?isbn={isbn}&cnt=1",
        timeout=timeout,
    )
    if not xml_str:
        return None
    try:
        root = ET.fromstring(xml_str)
        ns = {"dc": "http://purl.org/dc/elements/1.1/"}
        items = root.findall(".//item")
        if not items:
            return None
        item = items[0]

        title_el = item.find("title")
        if title_el is None:
            title_el = item.find("dc:title", ns)
        title = title_el.text.strip() if title_el is not None and title_el.text else ""

        creator_el = item.find("dc:creator", ns)
        author = creator_el.text.strip() if creator_el is not None and creator_el.text else ""

        if not title:
            return None
        return (title, author)
    except ET.ParseError:
        return None


def bookinfo_openbd(isbn: str, timeout: int = 10) -> tuple[str, str] | None:
    """OpenBD から (タイトル, 著者) を取得"""
    data = fetch_json(f"https://api.openbd.jp/v1/get?isbn={isbn}", timeout=timeout)
    if not data or not data[0]:
        return None
    s = data[0].get("summary", {})
    title = s.get("title", "").strip()
    author = s.get("author", "").strip()
    if not title:
        return None
    return (title, author)


def bookinfo(isbn: str, timeout: int = 10, retry: int = 3) -> tuple[str, str]:
    """本の情報を取得
    Args:
        isbn: ISBNコード
        timeout: タイムアウト時間（秒）
        retry: リトライ回数
    Returns:
        tuple[str, str]: (タイトル, 著者)
    Raises:
        TimeoutError: 通信がタイムアウトした場合
        LookupError: 書籍が見つからない場合
    """
    timed_out = False
    for _ in range(retry):
        try:
            result = bookinfo_openbd(isbn, timeout=timeout)
            if result:
                return result
        except TimeoutError:
            timed_out = True

        try:
            result = bookinfo_ndl(isbn, timeout=timeout)
            if result:
                return result
        except TimeoutError:
            timed_out = True

    if timed_out:
        raise TimeoutError(f"Timed out getting book info for ISBN: {isbn}")
    raise LookupError(f"Book not found for ISBN: {isbn}")
