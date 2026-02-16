from __future__ import annotations

from collections.abc import Callable

from ..models import ArticleInput

RuleFn = Callable[[ArticleInput], bool | None]


def first_rule_decision(article: ArticleInput, rules: list[RuleFn]) -> bool | None:
    for rule in rules:
        result = rule(article)
        if result is not None:
            return result
    return None
