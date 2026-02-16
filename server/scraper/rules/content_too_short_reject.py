from __future__ import annotations

from ..models import ArticleInput
from .common import LOCAL_TERMS, find_matches

MIN_LENGTH = 220


def content_too_short_reject(article: ArticleInput) -> bool | None:
    content = (article.full_text or "").strip()
    if not content:
        return False

    local_matches = find_matches(content, LOCAL_TERMS)
    if len(content) < MIN_LENGTH and not local_matches:
        return False
    return None
