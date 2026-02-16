import os

import content_scraper

from .models import ArticleInput
from .rules import (
    RuleAction,
    RuleDecision,
    build_content_rule_engine,
    build_snippet_rule_engine,
)

openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
snippet_rule_engine = build_snippet_rule_engine()
content_rule_engine = build_content_rule_engine()


def _print_rule_decision(prefix: str, decision: RuleDecision):
    suffix = f": {decision.reason}" if decision.reason else ""
    print(f"  {prefix} rule ({decision.rule}){suffix}")


def filter_snippet_locality(article: ArticleInput) -> bool:
    decision = snippet_rule_engine.evaluate(article)
    if decision.action == RuleAction.REJECT:
        _print_rule_decision("Snippet", decision)
        print("  Snippet check: Rule rejected (skipping AI)")
        return False
    if decision.action == RuleAction.PASS:
        _print_rule_decision("Snippet", decision)
        print("  Snippet check: Rule accepted (skipping AI)")
        return True

    print("  Snippet check: Ambiguous, asking AI...")
    is_local = content_scraper.check_snippet_locality(
        article.description, article.link, openrouter_api_key
    )
    if not is_local:
        print("  Snippet check: Not local (skipping)")
        return False
    print("  Snippet check: Possibly local")
    return True


def filter_content_locality(article: ArticleInput) -> bool:
    decision = content_rule_engine.evaluate(article)
    if decision.action == RuleAction.REJECT:
        _print_rule_decision("Deep check", decision)
        print("  Deep check: Rule rejected (skipping AI)")
        return False
    if decision.action == RuleAction.PASS:
        _print_rule_decision("Deep check", decision)
        print("  Deep check: Rule accepted (skipping AI)")
        return True

    print("  Deep check: Ambiguous, asking AI...")
    is_local = content_scraper.check_full_content_locality(
        article.full_text, openrouter_api_key
    )
    if not is_local:
        print("  Deep check: Not truly local (skipping)")
        return False
    print("  Confirmed local!")
    return True
