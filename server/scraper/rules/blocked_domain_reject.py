from __future__ import annotations

from urllib.parse import urlparse

from ..models import ArticleInput

BLOCKED_DOMAINS = (
    "cnn.com",
    "bbc.com",
    "foxnews.com",
)


def _extract_host(link: str) -> str:
    raw_link = (link or "").strip()
    if not raw_link:
        return ""
    if "://" not in raw_link:
        raw_link = f"//{raw_link}"
    parsed = urlparse(raw_link, scheme="http")
    return (parsed.hostname or "").lower()


def blocked_domain_reject(article: ArticleInput) -> bool | None:
    host = _extract_host(article.link)
    if not host:
        return None

    for blocked_domain in BLOCKED_DOMAINS:
        domain = blocked_domain.lower()
        if host == domain or host.endswith(f".{domain}"):
            return False
    return None
