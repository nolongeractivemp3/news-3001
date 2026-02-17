from __future__ import annotations

from ..models import ArticleInput

BLOCKED_KEYWORDS = (
    "international",
    "global",
    "weltweit",
    "bundesweit",
)


def _normalize(text: str) -> str:
    normalized = (text or "").lower()
    normalized = (
        normalized.replace("ä", "ae")
        .replace("ö", "oe")
        .replace("ü", "ue")
        .replace("ß", "ss")
    )
    return normalized.replace("-", " ").replace("/", " ").replace("_", " ")


def _contains_keyword(text: str, keyword: str) -> bool:
    normalized_text = " " + _normalize(text) + " "
    normalized_keyword = _normalize(keyword).strip()
    return f" {normalized_keyword} " in normalized_text


def snippet_strong_non_local_reject(article: ArticleInput) -> bool | None:
    scope = " ".join([article.title, article.description])
    if any(_contains_keyword(scope, keyword) for keyword in BLOCKED_KEYWORDS):
        return False
    return None
