from __future__ import annotations

from ..models import ArticleInput
from .common import LOCAL_TERMS, find_matches, snippet_text

MIN_MATCHES = 1


def snippet_local_keyword_pass(article: ArticleInput) -> bool | None:
    matches = find_matches(snippet_text(article), LOCAL_TERMS)
    if len(matches) >= MIN_MATCHES:
        return True
    return None
