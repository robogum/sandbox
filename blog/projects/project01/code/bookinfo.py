import json
import urllib.request
import xml.etree.ElementTree as ET


def fetch_xml(url: str) -> str | None:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "book-inventory/1.0"})
        with urllib.request.urlopen(req, timeout=10) as res:
            return res.read().decode("utf-8")
    except Exception:
        return None


def fetch_json(url: str) -> dict | list | None:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "book-inventory/1.0"})
        with urllib.request.urlopen(req, timeout=10) as res:
            return json.loads(res.read().decode("utf-8"))
    except Exception:
        return None


def bookinfo_ndl(isbn: str) -> tuple[str, str] | None:
    """国立国会図書館 から (タイトル, 著者) を取得"""
    xml_str = fetch_xml(f"https://iss.ndl.go.jp/api/opensearch?isbn={isbn}&cnt=1")
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


def bookinfo_openbd(isbn: str) -> tuple[str, str] | None:
    """OpenBD から (タイトル, 著者) を取得"""
    data = fetch_json(f"https://api.openbd.jp/v1/get?isbn={isbn}")
    if not data or not data[0]:
        return None
    s = data[0].get("summary", {})
    title = s.get("title", "").strip()
    author = s.get("author", "").strip()
    if not title:
        return None
    return (title, author)
