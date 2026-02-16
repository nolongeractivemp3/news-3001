from __future__ import annotations

from ..models import ArticleInput
from .common import LOCAL_TERMS, NON_LOCAL_HINTS, find_matches, snippet_text

MIN_MATCHES = 2


def snippet_strong_non_local_reject(article: ArticleInput) -> bool | None:
    snippet = snippet_text(article)
    local_matches = find_matches(snippet, LOCAL_TERMS)
    if local_matches:
        return None

    non_local_matches = find_matches(snippet, NON_LOCAL_HINTS)
    if len(non_local_matches) >= MIN_MATCHES:
        return False
    return None
