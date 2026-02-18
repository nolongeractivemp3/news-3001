from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import sys
from typing import Callable

# Allow running this script directly from any working directory.
SERVER_ROOT = Path(__file__).resolve().parents[2]
if str(SERVER_ROOT) not in sys.path:
    sys.path.insert(0, str(SERVER_ROOT))

from scraper.models import ArticleInput
from scraper.rules.blocked_domain_reject import blocked_domain_reject
from scraper.rules.non_article_link_reject import non_article_link_reject
from scraper.rules.runner import first_rule_decision
from scraper.rules.snippet_local_keyword_pass import snippet_local_keyword_pass
from scraper.rules.snippet_strong_non_local_reject import (
    snippet_strong_non_local_reject,
)

RuleFn = Callable[[ArticleInput], bool | None]


@dataclass(frozen=True)
class RuleCase:
    name: str
    rule: RuleFn
    article: ArticleInput
    expected: bool | None


def make_article(
    *,
    title: str,
    description: str = "",
    link: str = "https://example.com/article/1",
    source: str = "test-source",
) -> ArticleInput:
    return ArticleInput(
        source=source,
        title=title,
        description=description,
        link=link,
        full_text="",
        extra={},
    )


CASES: list[RuleCase] = [
    RuleCase(
        name="snippet local keyword allows decision to continue",
        rule=snippet_local_keyword_pass,
        article=make_article(title="Koepenick district update"),
        expected=None,
    ),
    RuleCase(
        name="snippet without local keyword is rejected",
        rule=snippet_local_keyword_pass,
        article=make_article(title="City council update"),
        expected=False,
    ),
    RuleCase(
        name="blocked domain rejects exact domain",
        rule=blocked_domain_reject,
        article=make_article(
            title="Koepenick district update",
            link="https://cnn.com/world/story",
        ),
        expected=False,
    ),
    RuleCase(
        name="blocked domain rejects subdomain",
        rule=blocked_domain_reject,
        article=make_article(
            title="Koepenick district update",
            link="https://news.bbc.com/world/story",
        ),
        expected=False,
    ),
    RuleCase(
        name="non-blocked domain is ignored by blocked-domain rule",
        rule=blocked_domain_reject,
        article=make_article(
            title="Koepenick district update",
            link="https://berlin.de/local/story",
        ),
        expected=None,
    ),
    RuleCase(
        name="non-article path /home is rejected",
        rule=non_article_link_reject,
        article=make_article(
            title="Koepenick district update",
            link="https://example.com/home",
        ),
        expected=False,
    ),
    RuleCase(
        name="maybe path /news returns unknown",
        rule=non_article_link_reject,
        article=make_article(
            title="Koepenick district update",
            link="https://example.com/news",
        ),
        expected=None,
    ),
    RuleCase(
        name="normal article-like path stays unknown",
        rule=non_article_link_reject,
        article=make_article(
            title="Koepenick district update",
            link="https://example.com/politics/2026-budget",
        ),
        expected=None,
    ),
    RuleCase(
        name="strong non-local keyword is rejected",
        rule=snippet_strong_non_local_reject,
        article=make_article(title="Global investment summit"),
        expected=False,
    ),
    RuleCase(
        name="no strong non-local keyword returns unknown",
        rule=snippet_strong_non_local_reject,
        article=make_article(title="District investment summit"),
        expected=None,
    ),
    RuleCase(
        name="runner rejects early when local keyword rule fails",
        rule=first_rule_decision,
        article=make_article(
            title="City council update",
            link="https://cnn.com/world/story",
        ),
        expected=False,
    ),
    RuleCase(
        name="runner rejects blocked domain after local keyword passes",
        rule=first_rule_decision,
        article=make_article(
            title="Treptow district update",
            link="https://cnn.com/world/story",
        ),
        expected=False,
    ),
    RuleCase(
        name="runner rejects non-article path after local keyword passes",
        rule=first_rule_decision,
        article=make_article(
            title="Treptow district update",
            link="https://example.com/home",
        ),
        expected=False,
    ),
    RuleCase(
        name="runner returns unknown when no rule reaches a final decision",
        rule=first_rule_decision,
        article=make_article(
            title="Treptow district update",
            description="Community project overview",
            link="https://example.com/news",
        ),
        expected=None,
    ),
    RuleCase(
        name="runner rejects strong non-local snippet after earlier rules pass",
        rule=first_rule_decision,
        article=make_article(
            title="Treptow global summit update",
            link="https://example.com/article/2",
        ),
        expected=False,
    ),
]


def run_case(case: RuleCase) -> bool:
    actual = case.rule(case.article)
    if actual != case.expected:
        print(f"FAIL: {case.name}")
        print(f"  expected: {case.expected!r}")
        print(f"  actual:   {actual!r}")
        print(f"  title:    {case.article.title}")
        print(f"  link:     {case.article.link}")
        return False

    print(f"PASS: {case.name}")
    return True


def main() -> int:
    total = len(CASES)
    passed = 0

    print(f"Running {total} rule checks...\n")
    for case in CASES:
        if run_case(case):
            passed += 1

    failed = total - passed
    print("\n--- Summary ---")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Total:  {total}")

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
