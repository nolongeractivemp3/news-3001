from __future__ import annotations

from ..models import ArticleInput
from .common import LOCAL_TERMS, find_matches

MIN_LENGTH = 450


def content_no_local_reject(article: ArticleInput) -> bool | None:
    content = (article.full_text or "").strip()
    if len(content) < MIN_LENGTH:
        return None

    matches = find_matches(content, LOCAL_TERMS)
    if not matches:
        return False
    return None
