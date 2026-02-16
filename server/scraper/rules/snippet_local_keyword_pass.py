from __future__ import annotations

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

MIN_LOCAL_MATCHES = 1


def _normalize(text: str) -> str:
    normalized = (text or "").lower()
    normalized = (
        normalized.replace("ä", "ae")
        .replace("ö", "oe")
        .replace("ü", "ue")
        .replace("ß", "ss")
    )
    return " " + normalized.replace("-", " ").replace("/", " ") + " "


def _find_matches(text: str, terms: tuple[str, ...]) -> list[str]:
    normalized_text = _normalize(text)
    matches = [term for term in terms if f" {term} " in normalized_text]
    return sorted(set(matches))


def _snippet_text(article: ArticleInput) -> str:
    return " ".join([article.title, article.description, article.link])


def snippet_local_keyword_pass(article: ArticleInput) -> bool | None:
    matches = _find_matches(_snippet_text(article), LOCAL_TERMS)
    if len(matches) >= MIN_LOCAL_MATCHES:
        return True
    return None
