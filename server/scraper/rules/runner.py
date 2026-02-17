from __future__ import annotations

from ..models import ArticleInput
from .blocked_domain_reject import blocked_domain_reject
from .snippet_local_keyword_pass import snippet_local_keyword_pass
from .snippet_strong_non_local_reject import snippet_strong_non_local_reject

RULES = [
    snippet_local_keyword_pass,
    blocked_domain_reject,
    snippet_strong_non_local_reject,
]


def first_rule_decision(article: ArticleInput) -> bool | None:
    for rule in RULES:
        result = rule(article)
        if result is not None:
            return result
    return None
