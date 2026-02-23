from __future__ import annotations

import importlib
import pkgutil
from pathlib import Path
from typing import Callable

from ..models import ArticleInput

_RULES_PATH = Path(__file__).parent
RuleFunc = Callable[[ArticleInput], bool | None]


def _discover_rules() -> list[RuleFunc]:
    """
    Auto-discover rules from sibling modules in this package.

    Each rule file should define a function named `rule`:
        my_rule.py -> def rule(article: ArticleInput) -> bool | None
    """
    rules: list[RuleFunc] = []

    for importer, modname, ispkg in pkgutil.iter_modules([str(_RULES_PATH)]):
        if modname == "runner":
            continue

        module = importlib.import_module(f"scraper.rules.{modname}")
        rule_func = getattr(module, "rule", None)
        if callable(rule_func):
            rules.append(rule_func)  # type: ignore[arg-type]

    return rules


RULES = _discover_rules()


def first_rule_decision(article: ArticleInput) -> bool | None:
    for rule in RULES:
        result = rule(article)
        if result is not None:
            return result
    return None
