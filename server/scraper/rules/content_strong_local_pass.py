from __future__ import annotations

from ..models import ArticleInput
from .common import LOCAL_TERMS, find_matches

MIN_MATCHES = 3


def content_strong_local_pass(article: ArticleInput) -> bool | None:
    matches = find_matches(article.full_text, LOCAL_TERMS)
    if len(matches) >= MIN_MATCHES:
        return True
    return None
