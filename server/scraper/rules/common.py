from __future__ import annotations

from typing import Sequence

from ..models import ArticleInput

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


def normalize(text: str) -> str:
    normalized = (text or "").lower()
    normalized = (
        normalized.replace("ä", "ae")
        .replace("ö", "oe")
        .replace("ü", "ue")
        .replace("ß", "ss")
    )
    return " " + normalized.replace("-", " ").replace("/", " ") + " "


def find_matches(text: str, terms: Sequence[str]) -> list[str]:
    normalized_text = normalize(text)
    matches = [term for term in terms if f" {term} " in normalized_text]
    return sorted(set(matches))


def snippet_text(article: ArticleInput) -> str:
    return " ".join([article.title, article.description, article.link])
