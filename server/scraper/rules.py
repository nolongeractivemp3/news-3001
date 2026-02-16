from __future__ import annotations

"""Deterministic locality rules used to short-circuit expensive AI checks."""

from dataclasses import dataclass
from enum import Enum
from typing import Protocol, Sequence

from .models import ArticleInput


class RuleAction(str, Enum):
    PASS = "pass"
    REJECT = "reject"
    DEFER = "defer"


@dataclass(frozen=True)
class RuleDecision:
    action: RuleAction
    rule: str
    reason: str = ""

    @property
    def decided(self) -> bool:
        return self.action != RuleAction.DEFER


def pass_decision(rule: str, reason: str = "") -> RuleDecision:
    return RuleDecision(action=RuleAction.PASS, rule=rule, reason=reason)


def reject_decision(rule: str, reason: str = "") -> RuleDecision:
    return RuleDecision(action=RuleAction.REJECT, rule=rule, reason=reason)


def defer_decision(rule: str, reason: str = "") -> RuleDecision:
    return RuleDecision(action=RuleAction.DEFER, rule=rule, reason=reason)


class LocalityRule(Protocol):
    name: str

    def evaluate(self, article: ArticleInput) -> RuleDecision:
        ...


class RuleEngine:
    def __init__(self, name: str, rules: Sequence[LocalityRule]):
        self.name = name
        self.rules = list(rules)

    def evaluate(self, article: ArticleInput) -> RuleDecision:
        for rule in self.rules:
            decision = rule.evaluate(article)
            if decision.decided:
                return decision
        return defer_decision(
            rule=f"{self.name}_no_rule_match",
            reason="No deterministic rule matched",
        )


LOCAL_TERMS = (
    "kopenick",
    "koepenick",
    "treptow",
    "treptow kopenick",
    "treptow koepenick",
    "friedrichshagen",
    "muggelheim",
    "mueggelheim",
    "grunau",
    "gruenau",
    "rahnsdorf",
    "schmockwitz",
    "adlershof",
    "oberschoeneweide",
    "niederschoeneweide",
)

NON_LOCAL_HINTS = (
    "international",
    "weltweit",
    "welt",
    "global",
    "deutschlandweit",
    "bundesweit",
    "europa",
    "usa",
    "ukraine",
    "russland",
    "israel",
    "gaza",
    "china",
    "trump",
    "bundestag",
    "bundesregierung",
)


def _normalize(text: str) -> str:
    normalized = (text or "").lower()
    normalized = (
        normalized.replace("ä", "ae")
        .replace("ö", "oe")
        .replace("ü", "ue")
        .replace("ß", "ss")
    )
    return " " + normalized.replace("-", " ").replace("/", " ") + " "


def _find_matches(text: str, terms: Sequence[str]) -> list[str]:
    normalized_text = _normalize(text)
    matches = [term for term in terms if f" {term} " in normalized_text]
    return sorted(set(matches))


def _snippet_text(article: ArticleInput) -> str:
    return " ".join([article.title, article.description, article.link])


@dataclass(frozen=True)
class SnippetLocalKeywordPassRule:
    name: str = "snippet_local_keyword_pass"
    min_matches: int = 1

    def evaluate(self, article: ArticleInput) -> RuleDecision:
        matches = _find_matches(_snippet_text(article), LOCAL_TERMS)
        if len(matches) >= self.min_matches:
            return pass_decision(self.name, reason=f"local_terms={','.join(matches[:3])}")
        return defer_decision(self.name)


@dataclass(frozen=True)
class SnippetStrongNonLocalRejectRule:
    name: str = "snippet_strong_non_local_reject"
    min_matches: int = 2

    def evaluate(self, article: ArticleInput) -> RuleDecision:
        snippet = _snippet_text(article)
        local_matches = _find_matches(snippet, LOCAL_TERMS)
        if local_matches:
            return defer_decision(self.name)

        non_local_matches = _find_matches(snippet, NON_LOCAL_HINTS)
        if len(non_local_matches) >= self.min_matches:
            return reject_decision(
                self.name,
                reason=f"non_local_terms={','.join(non_local_matches[:3])}",
            )
        return defer_decision(self.name)


@dataclass(frozen=True)
class ContentTooShortRejectRule:
    name: str = "content_too_short_reject"
    min_length: int = 220

    def evaluate(self, article: ArticleInput) -> RuleDecision:
        content = (article.full_text or "").strip()
        if not content:
            return reject_decision(self.name, reason="full_text_empty")
        local_matches = _find_matches(content, LOCAL_TERMS)
        if len(content) < self.min_length and not local_matches:
            return reject_decision(self.name, reason=f"length={len(content)}")
        return defer_decision(self.name)


@dataclass(frozen=True)
class ContentStrongLocalPassRule:
    name: str = "content_strong_local_pass"
    min_matches: int = 3

    def evaluate(self, article: ArticleInput) -> RuleDecision:
        matches = _find_matches(article.full_text, LOCAL_TERMS)
        if len(matches) >= self.min_matches:
            return pass_decision(self.name, reason=f"local_terms={','.join(matches[:4])}")
        return defer_decision(self.name)


@dataclass(frozen=True)
class ContentNoLocalRejectRule:
    name: str = "content_no_local_reject"
    min_length: int = 450

    def evaluate(self, article: ArticleInput) -> RuleDecision:
        content = (article.full_text or "").strip()
        if len(content) < self.min_length:
            return defer_decision(self.name)
        matches = _find_matches(content, LOCAL_TERMS)
        if not matches:
            return reject_decision(self.name, reason=f"length={len(content)}")
        return defer_decision(self.name)


def build_snippet_rule_engine() -> RuleEngine:
    return RuleEngine(
        name="snippet",
        rules=[
            SnippetLocalKeywordPassRule(),
            SnippetStrongNonLocalRejectRule(),
        ],
    )


def build_content_rule_engine() -> RuleEngine:
    return RuleEngine(
        name="content",
        rules=[
            ContentTooShortRejectRule(),
            ContentStrongLocalPassRule(),
            ContentNoLocalRejectRule(),
        ],
    )
