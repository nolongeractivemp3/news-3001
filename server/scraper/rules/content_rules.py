from __future__ import annotations

from ..models import ArticleInput
from .content_no_local_reject import content_no_local_reject
from .content_strong_local_pass import content_strong_local_pass
from .content_too_short_reject import content_too_short_reject
from .runner import run_rules

CONTENT_RULES = [
    content_too_short_reject,
    content_strong_local_pass,
    content_no_local_reject,
]


def run_content_rules(article: ArticleInput) -> bool | None:
    return run_rules(article=article, rules=CONTENT_RULES)
