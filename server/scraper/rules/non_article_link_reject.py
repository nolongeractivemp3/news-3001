from __future__ import annotations

from urllib.parse import urlparse

from ..models import ArticleInput

DEFINITE_FALSE_PATHS = (
    "/",
    "/home",
    "/homepage",
    "/startseite",
    "/search",
    "/suche",
    "/login",
    "/account",
    "/kontakt",
    "/about",
    "/impressum",
    "/newsletter",
    "/rss",
    "/feed",
    "/category",
    "/categories",
    "/tag",
    "/tags",
    "/topic",
    "/topics",
    "/thema",
    "/themen",
    "/kategorie",
)

MAYBE_PATHS = (
    "/news",
    "/nachrichten",
    "/latest",
    "/archive",
)


def _normalize_path(link: str) -> str:
    raw_link = (link or "").strip()
    if not raw_link:
        return ""
    if "://" not in raw_link:
        raw_link = f"//{raw_link}"
    parsed = urlparse(raw_link, scheme="http")
    path = (parsed.path or "").lower()
    if not path:
        return "/"
    if path != "/":
        path = path.rstrip("/")
    return path or "/"


def non_article_link_reject(article: ArticleInput) -> bool | None:
    path = _normalize_path(article.link)
    if not path:
        return None

    for definite_false_path in DEFINITE_FALSE_PATHS:
        if path == definite_false_path:
            return False

    for maybe_path in MAYBE_PATHS:
        if path == maybe_path:
            return None

    return None
