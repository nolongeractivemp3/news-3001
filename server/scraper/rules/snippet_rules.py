from __future__ import annotations

from ..models import ArticleInput
from .runner import run_rules
from .snippet_local_keyword_pass import snippet_local_keyword_pass
from .snippet_strong_non_local_reject import snippet_strong_non_local_reject

SNIPPET_RULES = [
    snippet_local_keyword_pass,
    snippet_strong_non_local_reject,
]


def run_snippet_rules(article: ArticleInput) -> bool | None:
    return run_rules(article=article, rules=SNIPPET_RULES)
